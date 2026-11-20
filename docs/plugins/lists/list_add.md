# List Add
:::{tip}
This is part of [managed list](/plugins/index.md#managed-list) plugin system.
:::

List plugins can have entries added to them by using the `list_add` plugin:
```yaml
trakt_list:
  username: traktusername
  list: watchlist
  type: movies
accept_all: yes
list_add:
  - trakt_list:
      username: a_different_username
      list: watchlist
      type: movies
```