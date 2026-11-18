# from_rtorrent

This plugin creates entries from rTorrent for further automation.

## Options

| **Name** | **Info** | **Description** |
| --- | --- | --- |
| uri | Text | rTorrent URI. IE: scgi://localhost:5000, http://localhost:80/RPC2, /home/rtorrent/rtorrent.sock  |
| username | Text | Username when using HTTP for basic auth |
| password | Text | Password when using HTTP for basic auth |
| digest_auth | [yes\|no] | Use HTTP Digest authentication |
| view | Text | View to use as input (default main) |
| fields | list | Specify which fields to get from rTorrent. See below for default fields |
| custom_fields | list | Specify which named custom fields to get from rTorrent |

The following entry fields are set by default on input.

- torrent_info_hash
- title
- up_total
- down_total
- down_rate
- is_open
- is_active
- custom1
- custom2
- custom3
- custom4
- custom5
- state
- complete
- bytes_done
- down_rate
- left_bytes
- ratio
- path

:::{seealso}
This plugin is almost always used in conjunction with <plugin:rtorrent>.
:::
