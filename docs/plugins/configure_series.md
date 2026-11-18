# Configure series
Generates <plugin:series> plugin configuration from titles produced by any input. Using this doesn't prevent configuring <plugin:series> plugin additionally. 

Commonly used with:

* <plugin:trakt_list>
* <plugin:thetvdb_list>
* <plugin:filesystem>
* <plugin:my_anime_list>

## Syntax
```yaml
configure_series:
  [settings]:
    # any series option
    # e.g. quality, timeframe etc
  from:
    # any input(s)
```

### Settings
You can use any of the [settings for the series plugin](plugin:series#settings) within the 'settings' block in configure_series. This section is optional, but if included, the settings will be applied to every show configured.

**NOTE:** If you need to set different options for individual series, you can do so using the <plugin:series> plugin alongside configure_series as shown in this [recipe.](/Cookbook/ForceStrictMatching)

### From
In this section you must include one or more configured [input plugins](/plugins/index.md#input). The titles of the entries created by this plugin will be used as the names of the series that you desire.

## Examples 
### Filesystem
Let's say you have a directory where all your series are stored in each in the own folder. Something like:

```text
/media/series/pioneer one/
/media/series/south park/
```

To automatically configure series plugin with all these you could do following:

```yaml
configure_series:
  settings:
    quality: 720p
  from:
    filesystem:
      - /media/series/
```

This will make adding new series easy too, just create new directory there :)

### TheTVDB list

```yaml
configure_series:
  from:
    thetvdb_list:
      username: <username>
      account_id: <account identifier>
  settings:
    timeframe: 12 hours
    target: 720p
    propers: 3 days
```

### Cross-task settings
You can store settings with <plugin:set> and `configure_series_<option>` to be reused on other tasks
```yaml
task1:
  trakt_list:
    account: <trakt account>
    list: <trakt list>
    type: shows
    strip_dates: yes
  set:
    # Strip non-alphanumeric characters from title and add as an alternate_title during configure_series
    configure_series_alternate_name: "{{trakt_series_name|d(title)|re_replace('[^\\w\\s]',''}}"
  list_add:
    - entry-list: my-list

task2:
  configure_series:
    # Series will be configured with a symbol-less alternate_title defined
    from: my-list