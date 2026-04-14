from __future__ import annotations

import asyncio
import shutil
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath
from typing import TYPE_CHECKING

import asyncssh
from asyncssh import ConnectionLost, SFTPConnectionLost
from loguru import logger

from flexget import plugin
from flexget.components.sftp.base import (
    DEFAULT_CONNECT_TRIES,
    DEFAULT_SFTP_PORT,
    DEFAULT_SOCKET_TIMEOUT_SEC,
)
from flexget.components.sftp.sftp_client import HOST_KEY_TYPES
from flexget.event import event
from flexget.utils.template import RenderError, render_from_entry

if TYPE_CHECKING:
    from asyncssh import SFTPClient, SSHClientConnection

    from flexget.task import Task

logger = logger.bind(name='sftp_upload')


class SFTPUpload:
    """Upload files to a SFTP server. This plugin requires the asyncssh Python module and its dependencies.

    ==================    ======================================================================================
    Option                Description
    ==================    ======================================================================================
    host                  Host to connect to
    port                  Port the remote SSH server is listening on. Defaults to port 22.
    username              Username to log in as
    password              The password to use. Optional if a private key is provided.
    private_key           Path to the private key (if any) to log into the SSH server
    private_key_pass      Password for the private key (if needed)
    to                    Path to upload the file to; supports Jinja2 templating on the input entry. Fields such
                          as series_name must be populated prior to input into this plugin using
                          metainfo_series or similar.
    delete_origin         Indicates whether to delete the original file after a successful
                          upload.
    socket_timeout_sec    Socket timeout in seconds
    connection_tries      Number of times to attempt to connect before failing (default 3).
    host_key              Specifies a host key not already in known_hosts
    ==================    ======================================================================================

    Example::

      sftp_list:
          host: example.com
          username: Username
          private_key: /Users/username/.ssh/id_rsa
          to: /TV/{{series_name}}/Series {{series_season}}
          delete_origin: False

    """

    schema = {
        'type': 'object',
        'properties': {
            'host': {'type': 'string'},
            'username': {'type': 'string'},
            'password': {'type': 'string'},
            'port': {'type': 'integer', 'default': DEFAULT_SFTP_PORT},
            'private_key': {'type': 'string'},
            'private_key_pass': {'type': 'string'},
            'to': {'type': 'string', 'default': '/'},
            'delete_origin': {'type': 'boolean', 'default': False},
            'host_key': {
                'type': 'object',
                'properties': {
                    'key_type': {'type': 'string', 'enum': list(HOST_KEY_TYPES.keys())},
                    'public_key': {'type': 'string'},
                },
                'required': ['key_type', 'public_key'],
                'additionalProperties': False,
            },
            'socket_timeout_sec': {'type': 'integer', 'default': DEFAULT_SOCKET_TIMEOUT_SEC},
            'connection_tries': {'type': 'integer', 'default': DEFAULT_CONNECT_TRIES},
        },
        'additionalProperties': False,
        'required': ['host', 'username'],
    }

    @staticmethod
    def prepare_config(config: dict) -> dict:
        """Set defaults for the provided configuration."""
        config.setdefault('password', None)
        config.setdefault('private_key', None)
        config.setdefault('private_key_pass', None)
        config.setdefault('to', None)

        return config

    @classmethod
    def on_task_output(cls, task: Task, config: dict) -> None:
        """Upload accepted entries to the specified SFTP server."""
        if task.accepted:
            host_key = config.get('host_key')
            sftp_config = SFTPConfig(
                host=config['host'],
                port=config['port'],
                username=config['username'],
                password=config.get('password'),
                client_keys=config.get('private_key'),
                passphrase=config.get('private_key_pass'),
                known_hosts=f'{config["host"]} {host_key["key_type"]} {host_key["public_key"]}'.encode()
                if host_key
                else None,
                login_timeout=config['socket_timeout_sec'],
            )
            sftp_manager = SFTPManager(
                sftp_config=sftp_config,
                entries=task.accepted,
                to=config['to'],
                delete_origin=config['delete_origin'],
                connection_tries=config['connection_tries'],
            )
            asyncio.run(sftp_manager.run())


@dataclass(frozen=True)
class SFTPConfig:
    host: str
    port: int
    username: str
    password: str | None
    client_keys: str | None
    passphrase: str | None
    login_timeout: float | int | str | None
    known_hosts: bytes | None


class SFTPManager:
    def __init__(
        self,
        *,
        sftp_config: SFTPConfig,
        entries,
        to,
        delete_origin,
        connection_tries,
        concurrency=5,
    ):
        self.sftp_config = sftp_config
        self.queue = asyncio.Queue()
        for item in entries:
            self.queue.put_nowait(item)
        self.to = to
        self.delete_origin = delete_origin
        self.connection_tries = connection_tries
        self.concurrency = concurrency

        self.sftp: SFTPClient | None = None
        self.conn: SSHClientConnection | None = None
        self.connection_version = 0
        self.lock = asyncio.Lock()  # Ensure only one worker is reconnecting
        self.ready = asyncio.Event()  # Ensure the connection is not used while reconnecting
        self.reconnect_failed = False

    async def close(self):
        if self.sftp:
            self.sftp.exit()
            await self.sftp.wait_closed()
        if self.conn:
            self.conn.close()
            await self.conn.wait_closed()

    async def _ensure_connection(self, last_version):
        """Ensure the connection is available.

        If the version is outdated, it indicates another worker is already reconnecting; in this case, simply wait.
        """
        async with self.lock:
            # Double-checked locking: A version update implies the reconnection process has already concluded.
            if self.connection_version > last_version:
                return

            logger.debug(
                '--- Executing connection repair (Old Version V{} -> New Version V{}) ---',
                last_version,
                self.connection_version + 1,
            )
            self.ready.clear()  # Clear the event to pause all workers.

            await self.close()

            retry_count = 0
            # Establish connection with exponential backoff retries
            while retry_count < self.connection_tries:
                try:
                    self.conn = await asyncssh.connect(**asdict(self.sftp_config))
                    self.sftp = await self.conn.start_sftp_client()

                    self.connection_version += 1
                    logger.debug(
                        'Connection repaired successfully; current version: V{}',
                        self.connection_version,
                    )
                    break
                except (ConnectionLost, SFTPConnectionLost) as e:
                    retry_count += 1
                    wait = min(2**retry_count, 10)
                    logger.debug('Reconnection failed: {}. Retrying in {}s...', e, wait)
                    await asyncio.sleep(wait)
            else:
                self.reconnect_failed = True
            self.ready.set()  # Resume all workers

    async def worker(self):
        while not self.queue.empty():
            await self.ready.wait()

            try:
                entry = self.queue.get_nowait()
            except asyncio.QueueEmpty:
                break
            if self.reconnect_failed:
                entry.fail('All connection attempts failed')
                break

            local_path = entry.get('location')
            if not local_path:
                logger.error(
                    'Entry {} does not have a "location" field, skipping.', entry['title']
                )
                entry.fail('Missing location field')
                continue

            logger.debug('Uploading file: {}', local_path)
            try:
                to = render_from_entry(self.to, entry)
            except RenderError as e:
                logger.error('Could not render path: {}', self.to)
                entry.fail(str(e))
                continue

            worker_version = self.connection_version
            sftp = self.sftp
            try:
                await sftp.makedirs(to, exist_ok=True)
                await sftp.put(
                    local_path,
                    PurePosixPath(to, Path(local_path).name),
                    preserve=True,
                    recurse=True,
                    follow_symlinks=True,
                )
            except (ConnectionLost, SFTPConnectionLost):
                self.queue.put_nowait(entry)
                await self._ensure_connection(worker_version)
            except (OSError, asyncssh.Error) as e:
                entry.fail(str(e))
            else:
                if self.delete_origin:
                    delete(local_path)

    async def run(self):
        # First-time connection
        await self._ensure_connection(0)

        workers = [self.worker() for _ in range(self.concurrency)]
        await asyncio.gather(*workers)
        await self.close()


def delete(path: str | Path) -> None:
    path = Path(path)
    if path.is_symlink():
        delete(path.resolve(strict=True))
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)
    elif path.is_file():
        path.unlink()


@event('plugin.register')
def register_plugin() -> None:
    plugin.register(SFTPUpload, 'sftp_upload', api_ver=2)
