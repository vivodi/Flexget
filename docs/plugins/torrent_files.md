# torrent_files

Extracts the file list from `.torrent` metadata and populates the `content_files` entry field. This allows downstream plugins (such as `content_filter`) to inspect or filter entries based on their internal files before downloading the torrent payload.

:::{note}
This is a **built-in** plugin and requires no configuration. It runs automatically during the `modify` phase (priority `200`) for any entry that has a `torrent` field populated.
:::

## Populated Entry Fields

- **`content_files`** (`list[str]`): POSIX-formatted relative file paths (`path/name`) of all files inside the torrent. Omitted if the torrent contains no files.

## Example

Because `torrent_files` runs automatically on `.torrent` entries, plugins that rely on `content_files` work out of the box:

```yaml
tasks:
  filter_torrents:
    rss: https://example.com/torrents.xml
    content_filter:
      require:
        - '*.mkv'
        - '*.mp4'
      reject:
        - '*.exe'
```
