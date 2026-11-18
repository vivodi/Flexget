# Disable
This plugin can be used to disable a plugin which you have included via the <plugin:template> or <plugin:include> plugin, as well as to disable [builtin](/Builtin) plugins.

## Configuration
This plugin should be configured with either the name of the plugin you wish to disable, or a list of plugins you wish to disable. You can also use the special term `builtins` to disable all builtin plugins.

## Example (disabling plugins from a template)
```
movies:
  download: ~/torrents/movies/
  imdb:
    min_score: 6.2
    .
    .

tasks:
  nzbs:
    template: movies
    disable: download
    sabnzbd:
      .
      .
```

Task nzbs uses all other configuration from template movies but removes the download plugin and instead uses <plugin:sabnzbd>.

## Example (disabling builtin plugins)
Disables all builtins:

```
disable: builtins
```

Disables the <plugin:seen> and <plugin:seen_info_hash> builtins:

```
disable:
  - seen
  - seen_info_hash
```