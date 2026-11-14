---
title: Plugins
description: 
published: true
date: 2026-04-25T01:23:20.567Z
tags: 
editor: markdown
dateCreated: 2022-09-18T04:51:15.647Z
---

# Plugins
Plugins provide most of the functionality in FlexGet. Plugins usually create, manipulate or download **[entries](/Entry)** but they can also change how FlexGet operates. Many plugins can use the **[Jinja2 ](/Jinja)** template system.

Most plugins are enabled by placing a keyword and required settings in a configuration file. All plugins listed below are included in the FlexGet package (with the exception of the third-party plugins section). 

This documentation is meant for the latest released version. If you are upgrading from an older version, see [upgrade actions](/UpgradeActions) and the [changelog](/ChangeLog) for help in migrating your configuration file.

## Indentation in examples
All configuration examples are assumed to be placed under the `tasks` (or `templates`) [top-level keys](/Configuration#top-level-keys). If the documentation has this example:

```yaml
series:
  - name
```

In a full configuration, this goes into:

```yaml
tasks:
  task_name:
    rss: http://example.com
    series:
      - name
```

This makes examples more compact and reduces unnecessary boilerplate.

For further help with YAML and indenting, see [configuration](/Configuration).

## Plugin Types
- [Input](project:#input)
- [Filter](project:#filter)
- [Output](#output)
- [Metadata](project:#metadata)
- [Modification](#modification)
- [Miscellaneous](#miscellaneous)
- [Managed List](#managed-list)
- [Search](#search)
- [Daemon](#daemon)
- [Third-Party Plugins](#third-party-plugins)

## Input
Produce **[entries](/Entry)** from external source.  
Most requests are cached so there is no penalty for using the same RSS URL multiple times in the configuration, for example.

**Note:** If you are looking for torrent search plugins, refer to [Search Plugins](/Plugins/Searches).

### Raw Input
Input plugins that directly parse data from a source based on its type.

```{toctable}
csv: Parse any CSV-file
filesystem: Search through a local directory looking for files as a input.
html: Parse any HTML-page. 
limit: Limit the amount of entries created by another input plugin. 
rss: Parse RSS-feed. 
sftp_list: List files from an SFTP server 
tail: Tail a log file (eg. irc logs) 
text: Parse any text data
regexp_parse: Use regular expressions to parse text from a web resource or file
ftp_list: Lists the content of a remote FTP server 
```

### 3rd party sites input
Input plugins designed to retrieve data from 3rd party web-sites, such as IMDB, trakt & etc.

```{toctable}
anidb_list: Create entries from your AniDB wishlist. 
anilist: Create entries from your AniList watchlist. 
apple_trailers: Get movie trailers from Apple.com
betaseries_list: Use series you follow on www.betaseries.com as an input
eztv: Use latest entries from EZTV 
from_emby: Creates entries from emby's watched list, favorites, libraries or playlists and filter based on some criteria
from_imdb: Produce entries based on an IMDB person, company or character  
from_piratebay: Produce entries based on piratebay api.
kitsu: Produce Entries based on your  [Kitsu.io](http://kitsu.io) libraries. 
lists/imdb_list: Use movies in your IMDb list as an input (eg. watchlist, rating history). [Managed List](/Plugins/List).<br> **Note:** This plugin does not currently work, look into [`imdb_watchlist`](/Plugins/imdb_watchlist) 
filmweb_watchlist: Use your Filmweb watchlist as an input
imdb_watchlist: Use you IMDB watchlist as an input
letterboxd: Create entries for movies on any public [Letterboxd](http://letterboxd.com) list 
my_anime_list: Create entries from MyAnimeList animelist. 
myepisodes_list: Create entries from the shows in your myepisodes.com account. 
npo_watchlist: Create entries for the shows and episodes in your npo.nl account (Dutch public television). 
pogcal: Produce entries for shows marked on your [pogdesign calendar](http://www.pogdesign.co.uk/cat/). 
rottentomatoes_list: Use movies from [Rotten Tomatoes](http://www.rottentomatoes.com) lists. 
sceper: Parse [http://sceper.ws](http://sceper.ws). 
lists/thetvdb_list: Produce an entry for all shows you have marked as favorites at http://thetvdb.com. [Managed List](/Plugins/List)
next_trakt_episodes: Create entries for the latest or the next episode to watch or collect by your trakt.tv activity. 
lists/trakt_list: Create entries from one of your trakt.tv lists. [Managed List](/Plugins/List) 
twitterfeed: Create entries from a twitter account. 
lostfilm: Create entries from lostfilm.tv 
```

### 3rd party software input
Input plugins designed to retrieve data from 3rd party software, such as Sonarr, couchpotato, deluge & etc.

```{toctable}
lists/couchpotato_list: Produce entries from couchpotato wanted movies list. [Managed List](/Plugins/List) 
from_deluge: Use torrents loaded in a Deluge daemon as input. 
from_rtorrent: Use torrents loaded in a rTorrent as input. 
from_telegram: Use telegram messages as input.
from_transmission: Use torrents loaded in Transmission as input. 
from_qbittorrent: Use torrents loaded in QBittorrent as input. 
lists/ombi_list: Add or remove entries from ombi. 
plex: Produce entries for shows present in a [Plex Media Server](http://www.plexapp.com) section. 
lists/plex_watchlist: Plex watchlist [Managed List](/Plugins/List) 
lists/radarr_list: Produce entries from or to radarr_list. [Managed List](/Plugins/List) 
sickbeard: Produce entries from Sickbeard's show list 
lists/sonarr_list: Produce entries from Sonarr's show list. [Managed List](/Plugins/List) 
next_sonarr_episodes: Produce entries for missing episodes from Sonarr 
medusa: Produce entries from Medusa's show list 
```

### Internal Input
Input plugins that will generate entries based on preexisting data in FlexGet.

```{toctable}
configure_series: Configures the series plugin with all the shows given by any input plugin (eg. filesystem, rss).  
discover: Produce entries from search results. 
from_digest: Outputs entries which have been collected by the [digest](/Plugins/digest) plugin. 
from_task: Runs another task and outputs accepted entries from that task. 
mock: Generates simulated entries from predefined titles and fields to debug and test task pipelines without fetching external sources.
next_series_episodes: Emits the next episode needed for each series configured in the series plugin. Useful for example with [discover](/Plugins/discover). 
next_series_seasons: Emits the next season needed for each series configured in the series plugin. Useful for example with [discover](/Plugins/discover). 
inputs: Configure the same input plugin multiple times in one task. 
lists/entry_list: Use or add entries to a custom made entry list. [Managed List](/Plugins/List) 
lists/movie_list: Use or add entries to a custom made movie list. [Managed List](/Plugins/List) 
lists/subtitle_list: Use or add entries to a custom made subtitle list. [Managed List](/Plugins/List) 
lists/pending_list: Manually approve entries. [Managed List](/Plugins/List) 
```

## Filter
Reject or Accept **[entries](/Entry)** based on given rules. A single task may have any number of filters.  
If you plan to use multiple filters per task, you should look at **[filtering operations](/Filtering)** to understand how they work.

### Content based filters
Filters based on the nature of the input content (such as movie, series, series premiere & etc.)

```{toctable}
all_series: Accepts any entry that appears to be an episode of a series. 
proper_movies: Keep track of downloaded movies and force re-download proper versions. 
series/index: Accept TV-series episodes. Quality and episode number aware. 
series_premiere: Accept any entry that appears to be the first episode of a series. 
lists/list_match: Use this plugin to filter entries based on another list plugin. 
```

### Metadata filters
Filters based on content's metadata such as size and quality

```{toctable}
best_quality: Group entries by identifier and accept/reject best/worse qualities within these groups. 
content_size: Reject torrents and nzb's that do not meet size requirements. 
quality: Reject entries not of the specified quality. 
```

### FlexGet internal filters
Filters based on preexisting data or operations within FlexGet

```{toctable}
upgrade: Accept/Reject better qualities of an entry (tracked by a unique identifier) 
timeframe: Timeframe in which FlexGet waits for the chosen quality. 
duplicates: Perform action based on duplicate entries by a field. 
limit_new: Allow only given number of entries to pass per execution. 
only_new: Causes all entries that were in the task on the previous run to be rejected at the input phase. 
remember_rejected: Remember rejections and reject them in future runs. 
require_field: Reject entries that do not have the specified fields. 
seen_movies: Rejects already downloaded movies (detected by imdb-link). 
seen: Reject already downloaded entries. [Builtin](/Builtin) 
unique: Accept/Reject entries with duplicate fields, except for the first item.
```

### Torrent specific filters
Filters based specifically for torrents

```{toctable}
content_filter: Reject based on filenames within torrents. 
magnets: Rejects entries with only magnet links. 
private_torrents: Reject private or public torrents. 
seen_info_hash: Rejects already downloaded torrents (detected by torrent info hash). [Builtin](/Builtin) 
torrent_alive: Reject any torrents that do not have an active tracker with seeds. 
```

### Logical and operational filters
Filters that will accept/reject entries based on logical statements or simple file operations

```{toctable}
accept_all: Accept all entries. 
age: Reject, Accept entries based on age by looking at a date in a specified entry field. 
archives: Accept, reject entries based on if they're valid ZIP/RAR archives. 
crossmatch: Accept/reject based on other inputs (eg. imdb_list watchlist, ratings history). 
exists: Reject entries based on existing files in filesystem. 
exists_movie: Reject entries based on existing movies in filesystem. 
exists_series: Reject entries based on existing series in filesystem. 
if: Filter based on simple python statements. 
regexp: Reject, Accept entries by using regular expression. 
```

### 3rd party sites filters
Filters based on data retrieved from 3rd party sites

```{toctable}
imdb: Accept movie entries based on imdb details. 
rottentomatoes: Accept movie entries based on Rotten Tomatoes details. 
```

## Output
Execute operation(s) on accepted entries.

### 3rd party software output
Send accepted entries to 3rd party software, usually downloaders.

```{toctable}
aria2: Pass URIs to be downloaded to the aria2 downloader. 
deluge: Pass torrents directly to deluge bittorrent client, supporting magnet links. 
nzbget: Download nzbs with nzbget. 
periscope: Download subtitles with Periscope. 
pyload: http://pyload.net/. 
qbittorrent: Pass torrents directly to the qBittorrent client, supporting magnet links. 
rtorrent: Pass torrents directly to rtorrent 
rtorrent_magnet: Handles magnet URI's and produces rTorrent compatible torrent files (0.8.9+) 
sabnzbd: Download nzbs with SABnzbd. 
subliminal: Download subtitles with Subliminal. 
transmission: Pass torrents directly to transmission, supporting magnet links. 
utorrent: Pass torrents directly to uTorrent. 
```

### 3rd party sites output
Send accepted entries to 3rd party sites, usually for tracking purposes. 

```{toctable}
kodi_library: Send clean/scan requests to a remote/local Kodi server. 
myepisodes: Mark accepted episodes as acquired on MyEpisodes. 
pogcal_acquired: Mark accepted episodes on [pogdesign TV calendar](http://pogdesign.co.uk/cat) 
subtitles: Download subtitles from opensubtitles.org.
```

### Notifier services output
Send notifications for accepted entries via various notification services. To allow any service to be used for any type of notification, FlexGet separates the plugins that generate messages from those that deliver them.

First, configure what notifications should be sent for a given task:

```{toctable}
notify: Configure what notifications should be sent for a given task.
```

Then, choose one or more of the following notifier plugins in the `via` configuration option of the [notify](/Plugins/notify) plugin to deliver the messages:

```{toctable}
notifiers/bark: Send a [Bark](https://github.com/Finb/Bark/blob/master/README.en.md) notification 
notifiers/discord: Send a [Discord](https://discordapp.com/) notification 
notifiers/email: Send an email message 
notifiers/gotify: Send a [Gotify](https://gotify.net) notification 
notifiers/join: Send a [Join](https://joaoapps.com/join/) notification 
notifiers/notifymyandroid: Send a [NMA](http://www.notifymyandroid.com/) notification 
notifiers/mqtt: Send MQTT notification 
notifiers/matrix: Send [matrix](https://matrix.org) notification 
notifiers/ntfysh: Send ntfy.sh notification
notifiers/prowl: Send a [Prowl](https://www.prowlapp.com/) notification 
notifiers/pushalot: Send a [Pushalot](https://pushalot.com/) notification 
notifiers/pushbullet: Send a [Pushbullet](https://www.pushbullet.com/) notification 
notifiers/pushover: Send a [Pushover](https://pushover.net/apps/clone/Flexget) notification 
notifiers/pushsafer: Send a [Pushsafer](https://www.pushsafer.com/en/FlexGet) notification 
notifiers/rapidpush: Send a [Rapidpush](https://rapidpush.net/) notification 
notifiers/slack: Send a [Slack](https://slack.com/) notification 
notifiers/sms_ru: Send a [SMS.RU](http://sms.ru/) notification 
notifiers/telegram: Send a [Telegram](https://telegram.org/) notification 
notifiers/toast: Send a notification to your system's notification center
notifiers/xmpp: Send an [XMPP](https://xmpp.org/) notification 
notifiers/ms_teams: Send a [Microsoft Teams](https://products.office.com/en-us/microsoft-teams/group-chat-software) notification
```

There is also a plugin that does not use the `notifier` interface, but is instead used as a regular output plugin:

```{toctable}
sns: Send notifications via [Amazon SNS](https://aws.amazon.com/sns/)
```

### FlexGet internal output
Use accepted entries as an input for various FlexGet plugins such as add to movie queue, set series begin & etc.

```{toctable}
digest: Collects entries from tasks to be combined into another task (usually for notification.) 
series_remove: Remove accepted series \ episodes from the <plugin:series> plugin 
set_series_begin: Set the first episode to download for series. 
lists/list_add: Use this plugin to add accepted entries to another list plugin. 
lists/list_remove: Use this plugin to remove accepted entries from another list plugin.
```

### File operations output
Perform different file operations using accepted entries.

```{toctable}
copy: Copy local files. 
decompress: Extract Zip and RAR files. 
delete: Delete local files. 
download: Download passed entries into given path. 
exec: Executes commands on entries. 
ftp_download: Download entries retrieved from [ftp_list](/Plugins/ftp_list) 
move: Move local files. 
sftp_download: Download files from an SFTP server 
sftp_upload: Upload files to an SFTP server 
symlink: Symlink local files. 
```

### Generators output
Generate custom output using accepted entries.

```{toctable}
make_html: Generate HTML file from passed entries. 
make_rss: Generate RSS-feed file from passed entries. 
```

## Metadata
Retrieve additional data from internal parsers or 3rd party sites. Used for population of more fields than default or to actively perform data retrieval for specific input types.

These provide metainfo (i.e. fields) to [Entry](/Entry).

```{toctable}
emby_lookup: Performs [Emby](https://emby.media/) search and populates several entry fields that can be used in other plugins.
imdb_lookup: Enable imdb parsing for imdb fields on-demand. 
rottentomatoes_lookup: Enable Rotten Tomatoes parsing for Rotten Tomatoes fields on-demand. 
thetvdb_lookup: Fetch series information from http://thetvdb.com/ 
tmdb_lookup: Enable http://www.themoviedb.org/ parsing for tmdb fields on-demand. 
torrent_files: Builtin. Parse torrent files for metadata 
trakt_lookup: Enable http://trakt.tv/ parsing for trakt fields on-demand. 
tvmaze_lookup: Enable http://tvmaze.com/ parsing for tvmaze fields on-demand. 
bluray_lookup: Enable http://m.blu-ray.com/ parsing for bluray fields on-demand. 
nfo_lookup: Read movie information from an [nfo file](http://kodi.wiki/view/NFO_files) (specially useful for [Kodi](https://kodi.tv/) libraries).
anime_relations: Populate IDs for different anime databases, TVDB, TMDB and IMDB 
check_subtitles: Check subtitles presence for local files. 
metainfo_movie: Call internal movie parser to parse task entries and generated movie related data. 
metainfo_series: Use internal series parser to parse task entries and generated series related data. 
```

## Modification
Plugins that can manipulate entry field.

### Request operations
```{toctable}
download_auth: Add a `download_auth` field to entry with a value of <inv:#*HTTPBasicAuth> or <inv:#*HTTPDigestAuth> for use by other plugins.
```

### File operations
Perform file oriented operations.

```{toctable}
add_trackers: Add trackers to torrents. 
extension: Force a file extension. 
path_by_ext: Change (download) path based on file-type (extension). 
path_by_space: Select a path based on disk stats 
remove_trackers: Remove trackers from a torrent. 
set: Set 'path' or other info per task. Can be dynamic per entry. 
```

### Data operations
Manipulate relevant data based on input.

```{toctable}
assume_quality: Make assumptions about the qualities of releases. 
manipulate: Allows regexp manipulation for entries.   
torrent_scrub: Removes non-standard keys like libtorrent resume information from downloads (which prevents the torrent from properly starting in Rtorrent). 
rmz: URL rewrite plugin for rmz.cr rss feed. Filehoster links to be grabbed can be configured.
rlsbb: URL rewrite plugin for rlsbb.ru rss feed. Filehoster links to be grabbed and comment parsing can be configured.
torrent_cache: Adds torrent cache service (torcache, torrage, etc) links for entries which have either magnet link as URL or have torrent_info_hash field defined
```

## Miscellaneous
Plugins that can perform various operations and do not readily fit into any categories.

### Request operations
Perform various operations on request that are being sent and received. 

```{toctable}
cfscraper: Enables cloudflare scraping in a task. 
convert_magnet: Converts magnet uris to torrent files using libtorrent 
cookies: Use FireFox3 cookies. 
domain_delay: Sets a minimum interval between requests to specific domains. 
formlogin: Log in to web site via login form. 
headers: Modify HTTP headers. 
proxy: Use a proxy to access resources. 
urlrewrite_search: Search for download URL from supported sites by using entry title. 
```

### 3rd Party Site Request Operations

```{toctable}
emby_refresh: Triggers a emby refresh.
rutracker: Supports downloading torrents from rutracker. 
wp_auth: Access WordPress [s2Member](https://s2member.com/) protected RSS feeds.
```

### File operations
Perform file oriented operations.

```{toctable}
free_space: Abort task when drive space is low. 
```

### Data operations

```{toctable}
parsing: Configure another parser for series and movie titles. (can help if IMDB/TMDB/TVDB lookup fails too often)
pathscrub: Cleans invalid characters from generated path/file names. (Used by other plugins that generate files.)
urlrewrite: User regexp for URL Rewriting. 
```

### FlexGet internal operations
Perform various FlexGet operations.

```{toctable}
abort_if_exists: Aborts a task if an entry field matches the regexp.
archive: Archive all seen entries for searchable database for later retrieval. 
delay: Adds artificial delay into a task. 
disable: Disable builtin plugin(s) from a task, or plugins included from a template. 
include: Include configuration from another yaml file. 
interval: Maintain minimum poll interval for the task. 
log_filter: Filter prevent certain messages from being logged. 
manual: Only run the task when explicitly specified. 
max_reruns: Limit the maximum number of task reruns. 
no_entries_ok: Silence warnings about task not producing entries, for tasks where that is normal. 
parameterize: Allows the config for an input plugin to be parameterized using another input plugin.
priority: Change task execution order. 
plugin_priority: Change plugin priorities.
reorder_quality: Reorder [qualities](/Qualities) to make one quality better or worse than another. 
retry_failed: Save failed entries so they can be retried. [Builtin](/Builtin) 
run_task: Trigger exectution of another task.
variables: Replace specific jinja2 values in config before executing tasks. 
sequence: Allows the same plugin to be configured multiple times in a task. 
sleep: Causes a pause to occur at a specified point during task execution. 
sort_by: Sort entries in a task. 
template: Provides global configuration and named templates. 
verify_ssl_certificates: Can turn off SSL certificate verification on a task. 
version_checker: Checks if user is running latest Flexget version on a given interval. 
```

## Managed List

### Managed list plugins

Managed list plugins are a specialized class of plugins that primarily function as input plugins, but can also serve as dynamic targets for list action plugins to add, remove, or match entries across different task phases.

```{toctable}
lists/couchpotato_list: Use or add entries from one of your couchpotato watch list. 
lists/emby_list: Allows list management in emby server 
lists/entry_list: Use or add entries to a custom made entry list. 
lists/imdb_list: Use or add entries from one of your IMDB lists. 
lists/movie_list: Use or add entries to a custom made movie list. 
lists/ombi_list: Use or add entries from ombi. 
lists/pending_list: Manually approve entries to be accepted 
lists/plex_watchlist: Use or add entries from plex 
lists/radarr_list: Use or add entries from Radarr. 
lists/regexp_list: Use or add entries to a custom made regexp list. 
lists/sonarr_list: Use or add entries from Sonarr shows. 
lists/subtitle_list: Use or add entries to a custom made subtitle list. 
lists/thetvdb_list: Use or add entries from your TheTVDB favorites list. 
lists/trakt_list: Use or add entries from one of your trakt.tv lists. 
```

### List action plugins

These plugins allow you to manipulate or filter entries against any managed list plugin:

```{toctable}
lists/list_add: Use this plugin to add accepted entries to a list plugin. 
lists/list_remove: Use this plugin to remove accepted entries from a list plugin. 
lists/list_match: Use this plugin to filter entries based on the contents of a list. 
lists/list_clear: Use this plugin to clear all items from a list plugin. 
```

All of the list action plugins take a list of managed list plugins in their schema, so all operation can be used on multiple plugins at the same time:

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
  - imdb_list:
      login: 'email@123.com'
      password: flexget
      list: watchlist
```

:::{seealso}
Want to create or convert an existing plugin to a managed list plugin? See [developer guide](/dev/list-interface).
:::

## Search

FlexGet provides framework for querying searches from supported sites. These cannot be used directly in a task, but can be used with the [urlrewrite_search](/Plugins/urlrewrite_search) & [discover](/Plugins/discover) plugins where they act like options for their parent plugins. This section lists these options and gives a brief description of their function.

:::{warning}
This list is very possibly out of date, it is maintained infrequently.

You can always get an up-to-date overview of the available search plugins by using the command line with command `flexget plugins --interface search`. Short documentation for a plugin can be obtained with [`flexget doc <plugin-name>`](https://flexget.com/CLI/doc) if included within source file.
:::

### Internal

```{toctable}
lists/entry_list: Search in an `entry_list`
searches/flexget_archive: Searches within previously archived entries
```

### General

```{toctable}
searches/search_rss: Generates query based rss feeds
searches/torznab: Generates query based torznab
```

### Public

```{toctable}
searches/1337x: Search [1337x.to](https://1337x.to/)
searches/argenteam: Generates entries from [www.argenteam.net](http://www.argenteam.net/)
searches/descargas2020: Generates entries from [descargas2020.com](http://descargas2020.com) 
searches/divxatope: Generates entries from [divxatope.com](http://divxatope.com/) 
eztv: Searches EZTV by IMDB ID 
searches/gazelle: Generates entries from gazelle-based websites like the now-defunct what.cd 
searches/nyaa: Generates entries from [nyaa.si](http://nyaa.si/) 
searches/limetorrents: Generates entries from limetorrents.cc 
searches/piratebay: Generates entries from [thepiratebay](http://thepiratebay.gl/) 
searches/solidtorrents: Generates entries from [solidtorrents](http://solidtorrents.net/) 
```

### Private

```{toctable}
searches/alpharatio: Searches torrent site AlphaRatio
searches/awesomehd: Searches torrent site AwesomeHD 
searches/btn: Searches torrent site BTN 
searches/cpasbien: Generates entries from [cpasbien.pw](http://www.cpasbien.pw/) 
searches/filelist: Generates entries from [filelist.ro](https://filelist.ro) 
searches/fuzer: Searches torrent site [Fuzer](https://www.fuzer.me/) 
searches/iptorrents: Generates entries from [iptorrents.com](http://iptorrents.com) 
searches/filelist_api: Searches torrent site Filelist
searches/morethantv: Generates entries from [morethan.tv](http://morethan.tv) (mtv) 
searches/newznab: Generates entries from [newznab.com](http://newznab.com) 
searches/gazelle: Generates entries from [NWCD](https://notwhat.cd/) and [RED](https://redacted.ch/)
searches/passthepopcorn: Searches torrent site PassThePopcorn 
searches/ptn: Searches torrent site PtN 
searches/torrentday: Generates entries from torrentday.com
searches/torrentleech: Generates entries from [torrentleech.org](http://torrentleech.org/) 
```

## Daemon
These plugins are specifically for when FlexGet is being used in daemon mode. They differ from the other plugins documented here, in that they should be configured at the root of your config. Not inside any tasks or templates.

```{toctable}
daemon/scheduler: Executes tasks with a given interval or schedule while daemon is running. 
daemon/irc: Connect a bot to an IRC channel and act on tracker announcements.
```

## Command Line Interface
Use `flexget --help` for full list of subcommands. `--help` can also be used with any of the subcommands for further help text.

| Command | Description |
| --- | --- |
| [inject](/Plugins/cli/inject) | Inject entries into tasks from the CLI. |
| [service](/Plugins/cli/service) | **`EXPERIMENTAL`** A Windows service installer for the FlexGet daemon. |

### `execute` command options
Use `flexget execute --help` for full option list.

| Argument | Description |
| --- | --- |
| [--cli-config](/Plugins/--cli-config) | Allow using values from commandline in YML-configuration file. |
| [--dump](/Plugins/--dump) | Display all entries after task execution. |
| [--tasks](/Plugins/--tasks) | Executes only the specified task(s) |
| [--inject](/Plugins/--inject) | Injects custom entry into task(s). |
| [--try-regexp](/Plugins/try_regexp) | Test how regexps work on task(s) interactively. |

## Third-party plugins

```{toctree}
:hidden:
ThirdPartyExtras
```

Plugins can be installed by simply placing them in a `plugins` folder alongside your configuration file. (This would usually be `~/.flexget/plugins/`, however it may be different if your config is in a different [location](https://www.flexget.com/Configuration#location).) It is also possible to package plugins in a separate Python package like [FlexGet extras](https://github.com/Flexget/extras).

There is a list of [third-party and extra plugins](/Plugins/ThirdPartyExtras) available, which are plugins that are not common, actively maintained or are otherwise unsuitable for main distribution.
