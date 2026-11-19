# Entry List
:::{tip}
This is part of [managed list](/plugins/index.md#managed-list) plugin system.
:::

Stores a copy of any entry that was added to it, and can be used in a variety of ways. 
See [managed list](/plugins/index.md#managed-list) how to use lists in general. 

## Configuration

```
entry_list: <NAME>
```

## Examples


### Digest replacement

```yaml
task:
  get-movies:
    priority: 1
    rss: ...
    accept_all: yes
    list_add:
      - entry_list: downloaded movies
    download: ...

  email-report:
    priority: 2
    entry_list: downloaded movies
    accept_all: yes
    notify:
      task:
        via:
          email: ...
```

First task `get-movies` will add all accepted entries to an `entry_list` with the name `downloaded movies`. It then later be used as an input itself in a `email-report` task. Effectively this can replace the <plugin:digest> plugin.


### Search in entry list:

You can use `entry_list` as a [search](/plugins/index.md#search) plugin to use with <plugin:discover>:

```yaml
tasks:
  discover-series:
    discover:
      release_estimations: ignore
      what:
        - next_series_episodes: yes
      from:
        - entry_list: series list
    series:
      - foo:
          begin: s01e01
```

## Command line interface

Please see [commandline documentation](/cli/entry-list)

## Entry List API
`entry_list` plugin has full JSON API support. See [API post](http://discuss.flexget.com/t/flexget-rest-api/) for details.