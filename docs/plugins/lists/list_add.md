## List Add
> This is part of [managed list](/Plugins/List) plugin system.
{.is-success}

List plugins can have entries added to them by using the `list_add` plugin:
```
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