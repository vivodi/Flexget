# List Clear
> This is part of [managed list](/Plugins/List) plugin system.
{.is-success}

This is a list plugin that clears the contents of the given lists.

## Syntax
```yaml
list_clear:
  what:
    - <list_type>: <list name>
  phase: <task phase>
```

Supported phases are `start, input, metainfo, filter, download, modify, output, learn, exit`.

By default, it will run in `start` phase.


## Examples
### Sync trakt to entry_list
This example shows you how to sync a list from Trakt in Flexget into an entry list, clearing it before filling.

```yaml
fill-series-list:
  list_clear:
    what:
      - entry_list: trakt
  trakt_list:
      account: '{? trakt.account ?}'
      list: '{? trakt.series ?}'
      type: shows
  list_add:
    - entry_list: trakt
  accept_all: yes
```

Realistically you'd probably want to use <plugin:trakt_list> instead of this.