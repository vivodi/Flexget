# Newznab plugin
> This plugin is part of [search](/Plugins/Searches) plugin system
{.is-success}

The newznab plugins is used in conjunction with the <plugin:discover> plugins.

With the <plugin:next_series_episodes>
```
discover:
  what:
    - next_series_episodes: yes
  from: 
    - newznab:
        website: <value>
        apikey: <value>
        category: <value>
```

or the <plugin:movie_list>

```
discover:
  what:
    - movie_list: movies
  from: 
    - newznab:
        website: <value>
        apikey: <value>
        category: <value>
```


You need then to configure the newznab plugins, which take 3 parameters:


| **Option** | **Description** |
| --- | --- |
| website | website of the newznab server |
| apikey | most newznab requires this key in order to make search on their website |
| category | type of search to do on newznab tv or movie |
