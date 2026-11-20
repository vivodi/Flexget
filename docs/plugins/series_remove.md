# Series Remove
Removes accepted entries for series, season or episode from the <plugin:series> plugin database.

Similar to the CLI command [`flexget series remove`](/cli/series)
```yaml
series_remove: yes
```

## Options
The optional `forget` parameter will remove the entries from the *entire database* (including <plugin:seen> plugin).

Similar to the CLI command [`flexget series forget`](/cli/series)
```yaml
series_remove:
  forget: yes
```