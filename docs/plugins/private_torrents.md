# Private Torrents
Uses private flag in torrent file to determine what to do with private torrents.

**Syntax:**

```
private_torrents: yes|no
```

## Example 1
```
private_torrents: no
```

This would reject all torrent entries with private flag.

## Example 2
```
private_torrents: yes
```

This would reject all public torrents.

Non-torrent content is not intervened.