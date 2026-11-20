# Pending List
:::{tip}
This is part of [managed list](/plugins/index.md#managed-list) plugin system.
:::

Stores a copy of any entry that was added to it, and can be used in a variety of ways. Will only emit the entry after it has been approved via [CLI](/cli/pending-list)/[API](/guide/api). Very useful in creating a broad scoped task where you can cherry pick entries.  
See [managed list](/plugins/index.md#managed-list) how to use lists in general. 

## Configuration

```yaml
pending_list: <NAME>
```

Or:

```yaml
pending_list: 
  list_name: <name>
  [include]: [pending|approved|all]
```


## Examples


### Series premieres suggestions

```yaml
task:
  pending_new_shows:
    priority: 1
    rss: http://rss.site.com
    seen: local
    regexp:
      accept:
      - s01e01
    list_add:
    - pending_list: new_shows
    metainfo_series: yes
    trakt_lookup: yes
    notify:
      entries:
        title: 'New show detected'
        message: |+
          {{ trakt_series_name }} - {{ trakt_series_year }}
          {{ title }} 
        via:
        - pushover:
            user_key: KEY
    
  download_new_shows:
    priority: 2
    pending_list: new_shows
    list_match:
      from:
      - pending_list: new_shows
    notify:
      task:
        via:
          email: ...
```

First task `pending_new_shows` will add all accepted entries to an `pending_list` with the name `new_shows`. It then later be used as an input itself in a `download_new_shows` task. **Only** entries that have been marked as approved in that specific list will appear as input in the `download_new_shows` task.


## Command line interface

Please see [commandline documentation](/cli/pending-list)

## Entry List API
`pending_list` plugin has full JSON API support. See [API page](/guide/api) for details.