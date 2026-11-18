# Entry
Entry represents a single item created by input(s), usually a downloadable content.
It contains all the information necessary for [plugins](/plugins/index) to perform their job . Usually some [action](/FilterOperations) like accept or reject on the entry.

For example, the <plugin:regexp> plugin checks whether the given regular expression matches the entry's **title** or **url** and acts accordingly.

### Example of an entry

These are mandatory fields. You don't necessarily need to deal with anything more complicated for simple use cases.


| **Name** | **Value** |
| --- | --- |
| title | Linux Mint 17.3 cinnamon |
| url | http://torrents.linuxmint.com/torrents/linuxmint-17.3-cinnamon-64bit.iso.torrent |

### Known fields
Entry *may* have any of these fields, but is not *guaranteed* to have any of them. It may have other fields as well depending on configuration. 

>Use `--dump` option to see your task content as this list is not complete or always up-to-date.
{.is-warning}


| **Name** | **Created by** | **Description** |
| --- | --- | --- |
| id | multiple plugins | Set by metainfo plugins to the unique identifer for this entry. IE: "movie 2010" or "series S01E01" |
| path | multiple plugins | Path where this entry content should be saved |
| description | <plugin:rss> | Item description |
| rss_pubdate | <plugin:rss> | Date the RSS item was published |
| task | metainfo_task | Task name which this entry belongs to |
| quality | metainfo_quality, <plugin:series> | Detected quality, ie. `720p` |
| quality_req | <plugin:couchpotato_list> | A quality requirement string, can hold several qualities. Used by `movie_queue` |
| accessed | <plugin:filesystem> | Last accessed time for the local file. Stored as a datetime object. |
| modified | <plugin:filesystem> | Last modified time for the local file. Stored as a datetime object. |
| created | <plugin:filesystem> | Creation time for the local file (only on Windows). Stored as a datetime object. |
| series_name | <plugin:series>, metainfo_series | Series name |
| series_season | <plugin:series>, metainfo_series | Series season |
| series_episode | <plugin:series>, metainfo_series | Series episode |
| series_id | <plugin:series> | Series episode identifier, ie. `S01E02` or `2009-12-1` |
| series_date | <plugin:series> | The date of the episode. (only available for date based series) |
| proper | <plugin:series> | Whether this entry is a proper or repack release |
| argenteam_subtitle | [argenteam](/Searches/argenteam) | aRGENTeaM subtitle's url |
| imdb_url | <plugin:imdb_lookup>+others | Imdb url |
| imdb_id | <plugin:imdb_lookup>* | Imdb identifier |
| imdb_name | <plugin:imdb_lookup>* | Imdb name |
| imdb_original_name | <plugin:imdb_lookup>* | Imdb original name |
| imdb_year | <plugin:imdb_lookup>* | Imdb year |
| imdb_score | <plugin:imdb_lookup>* | Imdb score |
| imdb_votes | <plugin:imdb_lookup>* | Imdb votes |
| imdb_genres | <plugin:imdb_lookup>* | List of imdb genres |
| imdb_languages | <plugin:imdb_lookup>* | List of imdb languages |
| imdb_photo | <plugin:imdb_lookup>* | Url for photo (hotlinking prevented) |
| imdb_plot_outline | <plugin:imdb_lookup>* | Plot outline |
| imdb_actors | <plugin:imdb_lookup>* | Actors dictionary (key: imdbid, value: name) |
| imdb_directors | <plugin:imdb_lookup>* | Directors dictionary (imdbid, name) |
| imdb_writers | <plugin:imdb_lookup>* | Writers dictionary (imdbid, name) |
| movie_name | <plugin:imdb_lookup>* | Movie title |
| movie_year | <plugin:imdb_lookup>* | Movie release year |
| output | <plugin:download> | Downloaded file |
| torrent | modify_torrent | When entry is a torrent this contains [Torrent class](/TorrentObject) |
| data | <plugin:download> | Internal. Binary content. |
| content_size | <plugin:content_size> | Parsed size of torrents or NZBs. |
| location | <plugin:filesystem> | The local filename of the entry. |
| timestamp | <plugin:filesystem> | The local file update time of the entry. |
| subtitles | <plugin:check_subtitles> | A list of languages about subtitles founds on disk (local files only) |
| plex_server | <plugin:plex> | If set, PMS hostname. Otherwise PMS IP. |
| plex_server_ip | <plugin:plex> | PMS IP. |
| plex_port | <plugin:plex> | PMS port. |
| plex_section | <plugin:plex> | Section number. |
| plex_section_name | <plugin:plex> | Section name. |
| plex_path | <plugin:plex> | Entry path on PMS. |
| plex_duration | <plugin:plex> | Entry length in seconds. |
| plex_thumb | <plugin:plex> | Episode thumbnail, series only. |
| plex_art | <plugin:plex> | Series or movie art as configured in PMS |
| plex_cover | <plugin:plex> | Series cover for series, movie cover for movies. |
| plex_season_cover | <plugin:plex> | Season cover, series only. If used in movies, movie cover will be set. |
| plex_title | <plugin:plex> | Episode name as indexed on PMS. |
| plex_summary | <plugin:plex> | Entry summary. |
| plex_status | <plugin:plex> | Entry status: seen, inprogress or unwatched. |
| plex_url | <plugin:plex> | Original plex url. |
| plex_userrating | <plugin:plex> | Rating given by the user. From 1 to 10 |
| plex_key | <plugin:plex> | Internal Plex identificator for the Media |
| tvdb_series_name | <plugin:thetvdb_lookup> | Series name provided by thetvdb |
| tvdb_rating | <plugin:thetvdb_lookup> | Series rating |
| tvdb_status | <plugin:thetvdb_lookup> | Series status(Continuing or Ended) |
| tvdb_runtime | <plugin:thetvdb_lookup> | Series runtime in minutes) |
| tvdb_first_air_date | <plugin:thetvdb_lookup> | Series premier date |
| tvdb_air_time | <plugin:thetvdb_lookup> | Series air time |
| tvdb_content_rating | <plugin:thetvdb_lookup> | Series content ration |
| tvdb_genres | <plugin:thetvdb_lookup> | Series genres |
| tvdb_network | <plugin:thetvdb_lookup> | Series network |
| tvdb_banner_url | <plugin:thetvdb_lookup> | Series banner url |
| tvdb_fanart_url | <plugin:thetvdb_lookup> | Series fanart url |
| tvdb_poster_url | <plugin:thetvdb_lookup> | Series poster url |
| tvdb_airs_day_of_week | <plugin:thetvdb_lookup> | Series airs date of the week |
| tvdb_actors | <plugin:thetvdb_lookup> | List of series actors |
| tvdb_language | <plugin:thetvdb_lookup> | Series language(en, fr, etc.) |
| imdb_url | <plugin:thetvdb_lookup> | Series imdb url |
| zap2it_id | <plugin:thetvdb_lookup> |  |
| tvdb_ep_name | <plugin:thetvdb_lookup> | Episode name |
| tvdb_ep_overview | <plugin:thetvdb_lookup> | Episode plot |
| tvdb_ep_directors | <plugin:thetvdb_lookup> | List of episode directors |
| tvdb_ep_writers | <plugin:thetvdb_lookup> | List of episode writers |
| tvdb_ep_air_date | <plugin:thetvdb_lookup> | Episode air date |
| tvdb_ep_rating | <plugin:thetvdb_lookup> | Episode rating |
| tvdb_ep_guest_stars | <plugin:thetvdb_lookup> | List of episode guest stars |
| tvdb_ep_image_url | <plugin:thetvdb_lookup> | Episode image url |
| tvdb_ep_id | <plugin:thetvdb_lookup> | Episode season and number ie. S01E02 |
| tvdb_season | <plugin:thetvdb_lookup> | Episode season |
| tvdb_episode | <plugin:thetvdb_lookup> | Episode number |
| trakt_series_name | <plugin:trakt_lookup> | Series name provided by trakt |
| trakt_series_runtime | <plugin:trakt_lookup> | Series runtime in minutes |
| trakt_series_first_aired_epoch | <plugin:trakt_lookup> | Series premier data in epoch time |
| trakt_series_first_aired_iso | <plugin:trakt_lookup> | Time stamp of premier date |
| trakt_series_air_time | <plugin:trakt_lookup> | Time the series ran |
| trakt_series_content_rating | <plugin:trakt_lookup> | Content rating ex: TV-14 |
| trakt_series_genres | <plugin:trakt_lookup> | Series genres |
| trakt_series_network | <plugin:trakt_lookup> | Series network |
| trakt_series_imdb_id | <plugin:trakt_lookup> | Series IMDB ID |
| trakt_series_tvdb_id | <plugin:trakt_lookup> | Series TVDB ID |
| trakt_series_tvrage_id | <plugin:trakt_lookup> | Series TVRage ID |
| trakt_series_actors | <plugin:trakt_lookup> | Series actors |
| trakt_series_country | <plugin:trakt_lookup> | Production Country |
| trakt_series_year | <plugin:trakt_lookup> | Series release year |
| trakt_series_status | <plugin:trakt_lookup> | Series status(ex: Airing) |
| trakt_series_overview | <plugin:trakt_lookup> | Series overview |
| trakt_ep_name | <plugin:trakt_lookup> | Episode name |
| trakt_ep_first_aired_epoch | <plugin:trakt_lookup> | Episode premier date in epoch |
| trakt_ep_first_aired_iso | <plugin:trakt_lookup> | Episode premier date time stamp |
| trakt_ep_overview | <plugin:trakt_lookup> | Episode overview |
| trakt_season | <plugin:trakt_lookup> | Episode season |
| trakt_episode | <plugin:trakt_lookup> | Episode Number |
| trakt_ep_id | <plugin:trakt_lookup> | Episode id string 'S01E01' |
| trakt_ep_tvdb_id | <plugin:trakt_lookup> | TVDB ID of episode |
| trakt_watched | <plugin:trakt_lookup> | Episode marked seen (true/false) |
| trakt_list | <plugin:trakt_list> | Names the originating list from which trakt_emit sourced this entry |
| tvmaze_series_weight | <plugin:tvmaze_lookup> | Series popularity |
| tvmaze_series_update_date | <plugin:tvmaze_lookup> | When series was last updated |
| tvmaze_series_webchannel | <plugin:tvmaze_lookup> | Series web channel (Netflix, Amazon, etc..) |
| tvmaze_series_show_type | <plugin:tvmaze_lookup> | Series type (scripted, reality, etc..) |
| tvmaze_series_episodes | <plugin:tvmaze_lookup> | List of episodes |
| tvmaze_series_id | <plugin:tvmaze_lookup> | Series ID provided by TVMaze |
| tvmaze_series_show_id | <plugin:tvmaze_lookup> | Series ID provided by TVMaze |
| tvmaze_series_name | <plugin:tvmaze_lookup> | Series name provided by TVMaze |
| tvmaze_series_year | <plugin:tvmaze_lookup> | Series year |
| tvmaze_series_rating | <plugin:tvmaze_lookup> | Series rating |
| tvmaze_series_status | <plugin:tvmaze_lookup> | Series status(Continuing or Ended) |
| tvmaze_series_summary | <plugin:tvmaze_lookup> | Series summary |
| tvmaze_series_runtime | <plugin:tvmaze_lookup> | Series runtime (in minutes) |
| tvmaze_series_premiered | <plugin:tvmaze_lookup> | Series premier date |
| tvmaze_genres | <plugin:tvmaze_lookup> | Series genres (list) |
| tvmaze_series_network | <plugin:tvmaze_lookup> | Series network |
| tvmaze_series_url | <plugin:tvmaze_lookup> | Series url |
| tvmaze_series_original_image | <plugin:tvmaze_lookup> | Series image url (large) |
| tvmaze_series_medium_image | <plugin:tvmaze_lookup> | Series image url (medium) |
| tvmaze_series_airdays | <plugin:tvmaze_lookup> | Series airs day of the week |
| tvmaze_series_language | <plugin:tvmaze_lookup> | Series language(en, fr, etc.) |
| tvmaze_series_tvrage | <plugin:tvmaze_lookup> | tvrage ID as provided by TVMaze |
| tvmaze_episode_name | <plugin:tvmaze_lookup> | Episode name |
| tvmaze_episode_airdate | <plugin:tvmaze_lookup> | Episode air date |
| tvmaze_ep_runtime | <plugin:tvmaze_lookup> | Episode runtime (in minutes) |
| tvmaze_episode_url | <plugin:tvmaze_lookup> | Episode url |
| tvmaze_episode_original_image | <plugin:tvmaze_lookup> | Episode image url (large) |
| tvmaze_episode_medium_image | <plugin:tvmaze_lookup> | Episode image url (medium) |
| tvmaze_episode_season | <plugin:tvmaze_lookup> | Season number of this episode. |
| tvmaze_episode_number | <plugin:tvmaze_lookup> | Episode number. |
| tvmaze_episode_id | <plugin:tvmaze_lookup> | Episode's TVMaze ID. |
| tvmaze_episode_airstamp | <plugin:tvmaze_lookup> | Date and Time Episode aired |
| tvmaze_series_actors | <plugin:tvmaze_lookup> | A list of the cast of the show. |

^* = and other plugins that utilize this plugin^