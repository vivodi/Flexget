# Convert Magnet

Simple plugin for converting magnet links to torrent files without the use of torrent caches.

## Prerequisites
- `libtorrent` is installed.
  ```console
  $ pip install libtorrent
  ```

## Usage

By default, the plugin will not fail entries if the conversion is unsuccessful, but setting `fail_entry_on_error: yes` will do so.

**Simple configuration**
```yaml
convert_magnet: yes|no
```

**With options**

```yaml
convert_magnet:
  timeout: n seconds|minutes
  fail_entry_on_error: yes|no
```