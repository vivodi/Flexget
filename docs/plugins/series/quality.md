# Quality

| **Name** | **Description** |
| --- | --- |
| quality | Accept only qualities that match this quality requirement. No other quality will be accepted. |
| [qualities](qualities.md) | Accept all given qualities, multiple downloads |

Values should all be specified as a valid [quality requirement](/guide/qualities.md#requirements) string.

**Example:**

```yaml
series:
  - name of series 1:
      quality: 720p+
  - name of series 2:
      quality: 1080p
  - name of series 3:
      quality: hdtv
```

Usually best way to specify quality for series is to use groups:

**Example:**

```yaml
series:
  720p:
    - name of series 1
    - name of series 2
  hdtv:
    - name of series 3
    - name of series 4
```

See [groups](plugin:series/per-group-settings) for more information.