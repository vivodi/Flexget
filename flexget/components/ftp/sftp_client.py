from __future__ import annotations

import asyncio
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from stat import S_ISDIR, S_ISLNK, S_ISREG
from urllib.parse import quote, urljoin

from loguru import logger

from flexget import plugin
from flexget.entry import Entry
from flexget.task import TaskAbort

# Retry configuration constants.
RETRY_INTERVAL_SEC: int = 15
RETRY_STEP_SEC: int = 5

# Supported host key types exposed to plugin schemas.
HOST_KEY_TYPES: dict[str, str] = {
    'ssh-rsa': 'ssh-rsa',
    'ssh-ed25519': 'ssh-ed25519',
}

try:
    import asyncssh
except ImportError:
    asyncssh = None

NodeHandler = Callable[[str], None]

logger = logger.bind(name='sftp_client')


@dataclass
class HostKey:
    """Host key used to connect to a SFTP server if not defined in known_hosts."""

    key_type: str
    public_key: str


@dataclass(frozen=True)
class RemoteNode:
    """Represent a discovered remote filesystem node."""

    path: str
    node_type: str


class SftpClient:
    """Sync SFTP client wrapper built on top of asyncssh.

    FlexGet SFTP plugins are synchronous, so this client owns a dedicated event loop and runs
    asyncssh coroutines on it while exposing a synchronous API.
    """

    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str | None = None,
        private_key: str | None = None,
        private_key_pass: str | None = None,
        host_key: HostKey | None = None,
        connection_tries: int = 3,
    ):
        """Create and connect an SFTP client.

        :param host: SFTP server host
        :param port: SFTP server port
        :param username: Username for authentication
        :param password: Password for authentication
        :param private_key: Optional private key path
        :param private_key_pass: Optional private key passphrase
        :param host_key: Optional host key pinning configuration
        :param connection_tries: Number of connect retries before aborting
        """
        if not asyncssh:
            raise plugin.DependencyError(
                issued_by='sftp_client',
                missing='asyncssh',
                message='sftp client requires the asyncssh Python module.',
            )

        self.host: str = host
        self.port: int = port
        self.username: str = username
        self.password: str | None = password
        self.private_key: str | None = private_key
        self.private_key_pass: str | None = private_key_pass
        self.host_key: HostKey | None = host_key

        self.prefix: str = self._get_prefix()
        self._socket_timeout_sec: int | None = None
        self._loop = asyncio.new_event_loop()
        try:
            self._conn, self._sftp = self._connect(connection_tries)
        except Exception:
            # Ensure the dedicated loop is always released when connect fails.
            self._loop.close()
            raise

    def list_directories(
        self,
        directories: list[str],
        recursive: bool,
        get_size: bool,
        files_only: bool,
        dirs_only: bool,
    ) -> list[Entry]:
        """Build a list of entries from a provided list of directories on an SFTP server.

        :param directories: list of directories to generate entries for
        :param recursive: boolean indicating whether to list recursively
        :param get_size: boolean indicating whether to compute size for each node (potentially slow for directories)
        :param files_only: boolean indicating whether to exclude directories
        :param dirs_only: boolean indicating whether to exclude files
        :return: a list of entries describing the contents of the provided directories
        """
        entries: list[Entry] = []
        for directory in directories:
            try:
                normalized_dir = self._run(self._sftp.realpath(directory))
                remote_nodes = self._run(self._collect_remote_nodes(normalized_dir, recursive))
                self._append_entries_from_nodes(
                    remote_nodes=remote_nodes,
                    get_size=get_size,
                    files_only=files_only,
                    dirs_only=dirs_only,
                    entry_accumulator=entries,
                )
            except OSError as e:
                logger.warning('Failed to open {} ({})', directory, str(e))
            except Exception as e:
                logger.warning('Failed to list {} ({})', directory, str(e))

        return entries

    def download(self, source: str, to: str, recursive: bool, delete_origin: bool) -> None:
        """Download the file specified in "source" to the destination specified in "to".

        :param source: path of the resource to download
        :param to: path of the directory to download to
        :param recursive: indicates whether to download the contents of "source" recursively
        :param delete_origin: indicates whether to delete the source resource upon download, is the source
                              is a symlink, only the symlink will be removed rather than it's target.
        """
        parsed_path = PurePosixPath(source)

        if not self.path_exists(source):
            raise SftpError(f'Remote path does not exist: {source}')

        is_symlink = self.is_link(source)
        if self.is_file(source):
            source_name = parsed_path.name
            destination = self._get_download_path(source_name, to)
            self._download_remote_file(source, destination)

            if delete_origin:
                self.remove_file(source)
            return

        if self.is_dir(source):
            self._download_remote_directory(source, to, recursive)

            if delete_origin:
                if is_symlink:
                    self.remove_file(source)
                else:
                    self.remove_dir(source)
            return

        logger.warning('Skipping unknown file: {}', source)

    def upload(self, source: Path, to: str) -> None:
        """Upload files or directories to an SFTP server.

        :param source: file or directory to upload
        :param to: destination
        """
        if source.is_dir():
            logger.verbose('Skipping directory {}', source)
            return

        self._upload_file(source, to)

    def remove_dir(self, path: str) -> None:
        """Remove a directory if it's empty.

        :param path: directory to remove
        """
        if self.path_exists(path) and not self._remote_listdir(path):
            logger.debug('Attempting to delete directory {}', path)
            try:
                self._run(self._sftp.rmdir(path))
            except Exception as e:
                logger.error('Failed to delete directory {} ({})', path, str(e))

    def remove_file(self, path: str) -> None:
        """Remove a file if it's empty.

        :param path: file to remove
        """
        logger.debug('Deleting remote file {}', path)
        try:
            self._run(self._sftp.remove(path))
        except Exception as e:
            logger.error('Failed to delete file {} ({})', path, str(e))

    def is_file(self, path: str) -> bool:
        """Check whether the remote path points to a file.

        :param path: path to check
        :return: boolean indicating if the path is a file
        """
        mode = self._get_target_mode(path)
        return mode is not None and S_ISREG(mode)

    def is_dir(self, path: str) -> bool:
        """Check whether the remote path points to a directory.

        :param path: path to check
        :return: boolean indicating if the path is a directory
        """
        mode = self._get_target_mode(path)
        return mode is not None and S_ISDIR(mode)

    def is_link(self, path: str) -> bool:
        """Check whether the remote path points to a symlink.

        :param path: path to check
        :return: boolean indicating if the path is a symlink
        """
        mode = self._get_lstat_mode(path)
        return mode is not None and S_ISLNK(mode)

    def path_exists(self, path: str) -> bool:
        """Check whether a remote path exists.

        :param path: Path to check
        :return: boolean indicating if the path exists
        """
        return self._get_lstat_mode(path) is not None

    def make_dirs(self, path: str) -> None:
        """Create remote directories recursively.

        :param path: path to create
        """
        if self.path_exists(path):
            return

        try:
            self._run(self._make_dirs_async(path))
        except Exception as e:
            raise SftpError(f'Failed to create remote directory {path} ({e!s})') from e

    def close(self) -> None:
        """Close SFTP and SSH connections."""
        try:
            self._run(self._sftp.exit(), use_timeout=False)
        except Exception as e:
            logger.debug('Ignoring SFTP session close error for {} ({}).', self.host, e)
        try:
            self._conn.close()
        except Exception as e:
            logger.debug('Ignoring SSH close error for {} ({}).', self.host, e)
        try:
            self._run(self._conn.wait_closed(), use_timeout=False)
        except Exception as e:
            logger.debug('Ignoring SSH wait_closed error for {} ({}).', self.host, e)
        if not self._loop.is_closed():
            self._loop.close()

    def set_socket_timeout(self, socket_timeout_sec: int) -> None:
        """Set operation timeout in seconds for subsequent SFTP operations.

        :param socket_timeout_sec: Socket timeout in seconds
        """
        self._socket_timeout_sec = socket_timeout_sec

    def _connect(self, connection_tries: int):
        """Connect to the remote SSH server with retries."""
        tries = connection_tries
        retry_interval = RETRY_INTERVAL_SEC

        logger.debug('Connecting to {}', self.host)

        while tries:
            try:
                conn = self._run(
                    asyncssh.connect(**self._build_connect_kwargs()), use_timeout=False
                )
                self._validate_host_key(conn)
                sftp = self._run(conn.start_sftp_client(), use_timeout=False)
            except Exception as e:
                tries -= 1
                logger.debug('Caught exception: {}', e)
                if not tries:
                    raise TaskAbort(f'Failed to connect to {self.host}') from e
                logger.warning(
                    'Failed to connect to {}; waiting {} seconds before retrying.',
                    self.host,
                    retry_interval,
                )
                time.sleep(retry_interval)
                retry_interval += RETRY_STEP_SEC
            else:
                logger.verbose('Connected to {}', self.host)
                return conn, sftp

        raise TaskAbort(f'Failed to connect to {self.host}')

    def _build_connect_kwargs(self) -> dict:
        """Build asyncssh connection kwargs from plugin config."""
        kwargs: dict = {
            'host': self.host,
            'port': self.port,
            'username': self.username,
            # Preserve legacy behavior where unknown hosts are accepted unless explicitly pinned.
            'known_hosts': None,
        }

        if self.password is not None:
            kwargs['password'] = self.password

        if self.private_key:
            kwargs['client_keys'] = [str(Path(self.private_key).expanduser())]

        if self.private_key_pass:
            kwargs['passphrase'] = self.private_key_pass

        # Restrict host key algorithm when host_key is configured.
        if self.host_key:
            kwargs['server_host_key_algs'] = [HOST_KEY_TYPES[self.host_key.key_type]]

        return kwargs

    def _validate_host_key(self, conn) -> None:
        """Validate the negotiated server host key when host_key is configured.

        asyncssh does not automatically pin to an inline key value when `known_hosts` is disabled,
        so we perform explicit verification against the configured key type and key body.
        """
        if not self.host_key:
            return

        key = conn.get_server_host_key()
        algorithm = key.get_algorithm()
        exported = key.export_public_key().decode().strip()
        # OpenSSH public key format: "<algorithm> <base64> [comment]".
        encoded_key = exported.split()[1]

        if algorithm != self.host_key.key_type or encoded_key != self.host_key.public_key:
            raise TaskAbort(f'Failed to connect to {self.host}')

    def _run(self, coro, *, use_timeout: bool = True):
        """Run a coroutine on the internal event loop.

        A timeout is applied when configured through :meth:`set_socket_timeout`.
        """
        if self._loop.is_closed():
            if asyncio.iscoroutine(coro):
                coro.close()
            elif isinstance(coro, asyncio.Future):
                coro.cancel()
            raise RuntimeError(
                f'SFTP event loop is closed for host {self.host}; create a new SftpClient instance.'
            )

        if use_timeout and self._socket_timeout_sec:
            coro = asyncio.wait_for(coro, timeout=self._socket_timeout_sec)

        return self._loop.run_until_complete(coro)

    async def _collect_remote_nodes(self, directory: str, recursive: bool) -> list[RemoteNode]:
        """Walk a remote directory and collect discovered nodes."""
        nodes: list[RemoteNode] = []

        def on_file(path: str) -> None:
            nodes.append(RemoteNode(path=path, node_type='file'))

        def on_dir(path: str) -> None:
            nodes.append(RemoteNode(path=path, node_type='dir'))

        def on_unknown(path: str) -> None:
            nodes.append(RemoteNode(path=path, node_type='unknown'))

        visited_dirs: set[str] = set()
        await self._walk_tree(
            directory,
            recursive=recursive,
            on_file=on_file,
            on_dir=on_dir,
            on_unknown=on_unknown,
            visited_dirs=visited_dirs,
        )

        return nodes

    def _append_entries_from_nodes(
        self,
        *,
        remote_nodes: list[RemoteNode],
        get_size: bool,
        files_only: bool,
        dirs_only: bool,
        entry_accumulator: list[Entry],
    ) -> None:
        """Convert discovered nodes into FlexGet entries."""
        for node in remote_nodes:
            if node.node_type == 'file':
                if dirs_only:
                    continue
                size = self._get_entry_size(node.path, is_directory=False) if get_size else None
                entry_accumulator.append(self._build_entry(node.path, size))
                continue

            if node.node_type == 'dir':
                if files_only:
                    continue
                size = self._get_entry_size(node.path, is_directory=True) if get_size else None
                entry_accumulator.append(self._build_entry(node.path, size))
                continue

            self._handle_unknown(node.path)

    async def _walk_tree(
        self,
        root: str,
        *,
        recursive: bool,
        on_file: NodeHandler,
        on_dir: NodeHandler,
        on_unknown: NodeHandler,
        visited_dirs: set[str],
    ) -> None:
        """Walk a remote directory and call handlers for discovered nodes.

        Symlinked directories are traversed when ``recursive`` is enabled. A visited set based on
        realpath is used to prevent recursion loops when symlinks point back to parent paths.
        """
        try:
            root_realpath = await self._sftp.realpath(root)
        except Exception:
            root_realpath = root

        if root_realpath in visited_dirs:
            return
        visited_dirs.add(root_realpath)

        for name in await self._remote_listdir_async(root):
            path = str(PurePosixPath(root) / name)
            node_type = await self._classify_remote_path(path)

            if node_type == 'file':
                on_file(path)
            elif node_type == 'dir':
                on_dir(path)
                if recursive:
                    await self._walk_tree(
                        path,
                        recursive=recursive,
                        on_file=on_file,
                        on_dir=on_dir,
                        on_unknown=on_unknown,
                        visited_dirs=visited_dirs,
                    )
            else:
                on_unknown(path)

    async def _classify_remote_path(self, path: str) -> str:
        """Classify a remote path as file, dir, or unknown."""
        mode = await self._get_target_mode_async(path)
        if mode is None:
            return 'unknown'
        if S_ISREG(mode):
            return 'file'
        if S_ISDIR(mode):
            return 'dir'
        return 'unknown'

    async def _remote_listdir_async(self, path: str) -> list[str]:
        """Return children names for a remote directory."""
        nodes = await self._sftp.listdir(path)
        names: list[str] = []
        for node in nodes:
            name = str(node)
            if name in {'.', '..'}:
                continue
            names.append(name)
        return names

    def _remote_listdir(self, path: str) -> list[str]:
        """Return children names for a remote directory synchronously."""
        return self._run(self._remote_listdir_async(path))

    @staticmethod
    def _handle_unknown(path: str) -> None:
        """Log unknown node types encountered during traversal."""
        logger.warning('Skipping unknown file: {}', path)

    def _build_entry(self, path: str, size: int | None) -> Entry:
        """Build a FlexGet entry from a remote path."""
        url = urljoin(self.prefix, quote(path))
        title = PurePosixPath(path).name

        entry = Entry(title, url)

        if size is not None:
            entry['content_size'] = size

        entry['private_key'] = self.private_key
        entry['private_key_pass'] = self.private_key_pass

        if self.host_key:
            entry['host_key'] = {
                'key_type': self.host_key.key_type,
                'public_key': self.host_key.public_key,
            }

        return entry

    def _get_entry_size(self, path: str, *, is_directory: bool) -> int:
        """Return node size while swallowing stat errors and returning -1."""
        try:
            if is_directory:
                return self._run(self._dir_size_async(path))
            return self._run(self._file_size_async(path))
        except Exception as e:
            logger.warning('Failed to get size for {} ({})', path, e)
            return -1

    async def _dir_size_async(self, path: str) -> int:
        """Calculate recursive directory size in bytes."""
        total_size = 0
        visited_dirs: set[str] = set()

        async def handle_file(file_path: str) -> None:
            nonlocal total_size
            total_size += await self._file_size_async(file_path)

        await self._walk_tree_for_size(path, handle_file, visited_dirs)
        return total_size

    async def _walk_tree_for_size(
        self,
        root: str,
        handle_file: Callable[[str], object],
        visited_dirs: set[str],
    ) -> None:
        """Walk a directory recursively and feed file paths to ``handle_file``."""
        try:
            root_realpath = await self._sftp.realpath(root)
        except Exception:
            root_realpath = root

        if root_realpath in visited_dirs:
            return
        visited_dirs.add(root_realpath)

        for name in await self._remote_listdir_async(root):
            path = str(PurePosixPath(root) / name)
            node_type = await self._classify_remote_path(path)

            if node_type == 'file':
                await handle_file(path)
            elif node_type == 'dir':
                await self._walk_tree_for_size(path, handle_file, visited_dirs)

    async def _file_size_async(self, path: str) -> int:
        """Return file size for a remote path."""
        return (await self._sftp.lstat(path)).size

    def _download_remote_directory(
        self, source: str, destination_root: str, recursive: bool
    ) -> None:
        """Download files from a remote directory preserving relative paths."""
        source_path = PurePosixPath(source)
        base = source_path.parent

        remote_files: list[str] = self._run(self._collect_download_files_async(source, recursive))
        for remote_file in remote_files:
            relative_path = str(PurePosixPath(remote_file).relative_to(base))
            local_destination = self._get_download_path(relative_path, destination_root)
            self._download_remote_file(remote_file, local_destination)

    async def _collect_download_files_async(self, source: str, recursive: bool) -> list[str]:
        """Collect remote files to download from a source directory."""
        files: list[str] = []
        visited_dirs: set[str] = set()

        await self._walk_tree(
            source,
            recursive=recursive,
            on_file=files.append,
            on_dir=self._noop_handler,
            on_unknown=self._handle_unknown,
            visited_dirs=visited_dirs,
        )

        return files

    @staticmethod
    def _noop_handler(path: str) -> None:
        """No-op callback used for traversal handlers."""
        logger.debug('null handler called for {}', path)

    def _download_remote_file(self, source: str, destination_path: str) -> None:
        """Download a single remote file and clean up partial local files on failure."""
        destination_dir = str(Path(destination_path).parent)

        if Path(destination_path).exists():
            logger.verbose(
                'Skipping {} because destination file {} already exists.', source, destination_path
            )
            return

        Path(destination_dir).mkdir(parents=True, exist_ok=True)
        logger.verbose('Downloading file {} to {}', source, destination_path)

        try:
            self._run(self._sftp.get(source, destination_path))
        except Exception as e:
            logger.error('Failed to download {} ({})', source, e)
            if Path(destination_path).exists():
                logger.debug('Removing partially downloaded file {}', destination_path)
                Path(destination_path).unlink()
            raise SftpError(f'Failed to download file {source} ({e!s})') from e

    def _upload_file(self, source: Path, to: str) -> None:
        """Upload a local file into a remote directory."""
        if not source.exists():
            logger.warning('File no longer exists: {}', source)
            return

        destination = self._get_upload_path(source, to)
        destination_url = urljoin(self.prefix, destination)

        if not self.path_exists(to):
            self.make_dirs(to)

        if not self.is_dir(to):
            raise SftpError(f'Not a directory: {to}')

        try:
            self._run(self._sftp.put(str(source), destination))
            logger.verbose('Successfully uploaded {} to {}', source, destination_url)
        except OSError as e:
            raise SftpError(f'Remote directory does not exist: {to}') from e
        except Exception as e:
            raise SftpError(f'Failed to upload {source} ({e!s})') from e

    async def _make_dirs_async(self, path: str) -> None:
        """Create nested directories on the remote server."""
        parts = PurePosixPath(path).parts
        if not parts:
            return

        current = PurePosixPath('/') if PurePosixPath(path).is_absolute() else PurePosixPath('.')
        for part in parts:
            if part in {'/', '.'}:
                continue
            current = current / part
            current_str = str(current)
            if await self._get_lstat_mode_async(current_str) is None:
                await self._sftp.mkdir(current_str)

    def _get_lstat_mode(self, path: str) -> int | None:
        """Return lstat mode for a path, or ``None`` when path is missing."""
        return self._run(self._get_lstat_mode_async(path))

    async def _get_lstat_mode_async(self, path: str) -> int | None:
        """Return lstat mode for a path, or ``None`` when path is missing."""
        try:
            attrs = await self._sftp.lstat(path)
        except asyncssh.SFTPNoSuchFile:
            return None
        else:
            return attrs.permissions

    def _get_target_mode(self, path: str) -> int | None:
        """Return stat mode for a path with symlinks resolved, or ``None`` if missing."""
        return self._run(self._get_target_mode_async(path))

    async def _get_target_mode_async(self, path: str) -> int | None:
        """Return stat mode for a path with symlinks resolved, or ``None`` if missing."""
        try:
            attrs = await self._sftp.stat(path)
        except asyncssh.SFTPNoSuchFile:
            return None
        else:
            return attrs.permissions

    def _get_prefix(self) -> str:
        """Generate SFTP URL prefix."""

        def get_login_string() -> str:
            if self.username and self.password:
                return f'{self.username}:{self.password}@'
            if self.username:
                return f'{self.username}@'
            return ''

        def get_port_string() -> str:
            if self.port and self.port != 22:
                return f':{self.port}'
            return ''

        login_string = get_login_string()
        port_string = get_port_string()

        return f'sftp://{login_string}{self.host}{port_string}/'

    @staticmethod
    def _get_download_path(path: str, destination: str) -> str:
        """Build the local destination path for a downloaded file."""
        return str(PurePosixPath(destination) / path)

    @staticmethod
    def _get_upload_path(source: Path, to: str) -> str:
        """Build the remote destination path for an uploaded file."""
        return str(PurePosixPath(to, source.name))


class SftpError(Exception):
    """Generic SFTP operation error."""

    def __getitem__(self, index):
        """Support string-like indexing/slicing for legacy reason formatting."""
        return str(self)[index]
