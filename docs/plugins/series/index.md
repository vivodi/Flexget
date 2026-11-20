# Series
Intelligent filter for TV-series.

```{toctree}
:glob:
:hidden:
*
```

## Features
 * Episode history aware, no duplicate downloads - refer to <plugin:seen> plugin page for more information
 * Plenty of [quality](quality.md) options
 * [Timeframe](timeframe.md), when used with sort_by plugin, selects the entry best matching the criteria in given timeframe
 * [Proper & Repack](propers.md) aware
 * Specials aware (grabs episodes with the series title and the word 'special')
 * Tries to ignore season packs (if not configured explicitly to get them), you can use <plugin:content_size> for extra insurance against them.
 * Supports double episodes. i.e. S01E01-E02
 * [Series searching support](/cookbook/series/search) (via <plugin:discover> and <plugin:next_series_episodes> plugins)

**Simple configuration:**

```yaml
series:
  - some series
  - another series
```

If `some series` and `another series` have understandable episode
numbering any given episode is downloaded only once. FlexGet should support all known episode numbering schemes without any configuration, including dates.

So if we get same episode twice:

 * Some.Series.S2E10.720p.x264-FlexGet
 * Some.Series.S2E10.HR.x264-FooBar

Only one of them is downloaded, with default configuration the first entry matching quality requirements is chosen. In this example we have no spesific requirements. To get the best quality within current execution you can sort qualities with <plugin:sort_by> plugin.

```yaml
sort_by:
  field: quality
  reverse: yes
```

However there are much better options avaialble in the plugin. For example specifying desired [quality](quality.md) or [timeframe](timeframe.md) to wait for one.

## Settings
The series plugin supports a number of settings to customize it's behavior. Though the examples show the settings being applied to a single series, they can all be applied to a group of series as well.

[How to configure settings per series](per-series-settings)  
[How to configure settings with groups](per-group-settings)


| Option | Description |
| --- | --- |
| [alternate_name](alternate_name) | Define other names which this show is also released as. |
| [assume_special](assume_special) | Assume any entry with no series numbering detected is a special and treat it accordingly. |
| [begin](begin.md) | Manually specify first episode to start series on. |
| [ep_regexp](regexps.md#episode-numbering-matching) | Manually specify regexp(s) that matches to episode, season numbering. |
| [exact](exact) | Configure exact matching behavior. Needed for series which have similar named series. Uses 'auto' mode as default. |
| [from_group](from_group) | Accept series only from given groups. |
| [id_regexp](regexps.md#episode-numbering-matching) | Manually specify regexp(s) that matches to series identifier (numbering). |
| [identified_by](identified_by.md) | Configure how episode numbering is detected. Uses 'auto' mode as default. |
| [name_regexp](regexps.md) | Manually specify regexp(s) that matches to series name. |
| [parse_only](parse_only) | Series plugin will not accept or reject any entries, merely fill in all metadata fields. |
| [path](path.md) | Set *path* field for this series. |
| [prefer_specials](prefer_specials) | Flag entries matching both special and a normal ID type as specials. |
| [propers](propers.md) | Configure how propers are handled. |
| [qualities](qualities.md) | Download all listed qualities when they become available. |
| [quality](quality.md) | Required quality. |
| [set](set) | Use <plugin:set> plugin to set any fields for this series. |
| [special_ids](special_ids) | Defines other IDs which will cause entries to be flagged as specials. |
| [specials](specials.md) | Turn off specials support for series. (on by default) |
| [target](timeframe.md) | The target quality that should be downloaded without waiting for `timeframe` to complete. |
| [timeframe](timeframe.md) | Wait given amount of time for specified quality to become available, after that fall back to best so far. |
| [upgrade](upgrade.md) | Keeps getting the better qualities as they become available. |
| [season_packs](season_packs) | Enable downloading season packs. 

## Related plugins
These plugins are complementary to the series plugin.

| Name | Description |
| --- | --- |
| <plugin:all_series> | Grab all series in the task|
| <plugin:configure_series> | Automatically configures series by using another input, some examples: <plugin:trakt_list> and <plugin:filesystem>.<br> With this you don't need to maintain series configuration in the configuration file.  |
| <plugin:series_premiere> | Download all premieres| 
| <plugin:next_series_episodes> | Emit next episodes for <plugin:discover> | 
| <plugin:next_series_seasons> | Emit next seasons for <plugin:discover> | 


## Notes

* If the series appears in task(s) with slightly different naming conventions and spinoffs like FooBar and FooBar US read [this guide](closematch). 
* FlexGet respects *propers* which means that the same episode will be downloaded twice if the second one contains words such as `proper`, `repack`, `rerip`, or `real`.
* If series name is written in multiple different ways, don't add them as separate series. This will confuse episode tracking. 
* Check [series cookbook](/cookbook/series/index) for more complete examples and advanced uses.
* If using discover, existing collection can be imported with [this](/cookbook/series/seed-db) recipe.

## Commandline interface

### `series` Commandline Arguments
The series plugin has several features available at the command line via the [`flexget series` command](/cli/series).

### `execute` Commandline Arguments
There are also options to the `flexget execute` command which affect the series plugin:

Using `series begin` to set new starting point is recommended and should resolve any tracking issues. If you for some reason need to record episode into history it can be achieved with command `flexget inject "Pioneer One 05" --task <name> --learn`.

### \-\-stop-waiting \<name\>
Stops timeframe for given name, thus downloading any episode that is currently pending in the timeframe.