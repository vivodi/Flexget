# Fill movie_list from 3rd party input
This task will add movies from [trakt.tv](http://trakt.tv) watchlist to your <plugin:movie_list>. This is not intended to download anything, just fill the FlexGet movie list from there. You will have to have another task to do the actual downloading with the <plugin:list_match> to accept entries. You can remove <plugin:trakt_list> plugin from this recipe if you do not want to use that particular site and use another eg. <plugin:imdb_list>, <plugin:couchpotato_list>.

```yaml
tasks:
  watchlist:
    priority: 1
    trakt_list:
      account: my_acc_name
      list: watchlist
      type: movies
    accept_all: yes
    seen: local  # We don't want accepted movies on this feed to affect actual download feed
    list_add:
      - movie_list: watchlist  # you can call this whatever you want
```

**NOTE:** Make sure you don't have download/deluge/transmission plugin in this task, (or in a global template,) you aren't actually downloading anything here.

## Plugins used

| Plugin | Reason |
| --- | --- |
| <plugin:priority> | Run the task early, before other tasks that may do downloading |
| <plugin:trakt_list> | Watch list source |
| <plugin:accept_all> | We want to add all items to the queue |
| <plugin:list_add> | Add accepted entries to specified list|