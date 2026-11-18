# List Remove
> This is part of [managed list](/Plugins/List) plugin system.
{.is-success}

List plugins can have entries removed from them by using the `list_remove` plugin.

## Examples

Move items from account to another.

```yaml
trakt_list:
  username: <USER A>
  list: watchlist
  type: movies
accept_all: yes
list_remove:
  - trakt_list:
      username: <USER B>
      account: traktusername # required if list is not public
      list: watchlist
      type: movies
```

Uses: [trakt_list](/Plugins/List/trakt_list), [accept_all](/Plugins/accept_all)