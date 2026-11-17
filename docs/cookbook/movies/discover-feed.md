# Dowload movies using movie_list and discover
This recipe aims to allow adding of movies as simple as adding a movie to your trakt.tv watchlist.

This recipe goes one step further and also uses the <plugin:discover> plugin to dynamically search for the desired movies. The <plugin:torrent_alive> plugin is used to reject results that do not have at least a minimum number of seeds, which usually improves the quality of the results.

```yaml
tasks:
  # task to pull movies from trakt.tv watchlist and add to the movie list
  sync-watchlist:
    priority: 1
    trakt_list:  # You could also use imdb_watchlist
      account: <<account name>>
      list: watchlist
    accept_all: yes
    seen: local  # We don't want accepted movies on this feed to affect actual download task
    list_add:
      - movie_list: movies  # you can call this whatever you want

  # task that automatically downloads movies from the movie_list
  search-movies:
    trakt_lookup: yes  # can also use imdb_lookup or tmdb_lookup
    priority: 10 # run after the movie queue fill task
    discover:
      what:
        - movie_list: movies
      from:
        - piratebay: yes
      interval: 7 days
    torrent_alive: 10 # Will reject results with less than 10 seeds
    quality: dvdrip+ # Make sure no screeners or cams are downloaded
    list_match:
      from:
        - movie_list: movies
    transmission: yes # You could use another output plugin instead of this (deluge, qbittorrent, download)
```
Plugins used: <plugin:priority>, <plugin:transmission>, <plugin:trakt_list>,<plugin:trakt_lookup>, <plugin:accept_all>, <plugin:movie_list>, <plugin:list_match>, <plugin:seen>, <plugin:torrent_alive>, <plugin:discover> using [search plugin](/Searches) [piratebay](/Searches/piratebay).