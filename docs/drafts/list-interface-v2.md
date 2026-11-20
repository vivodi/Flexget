# Refactor list usage
Just some ideas ...

Alternative to add_list, remove_list

```yaml
manage_list:
  add:
    - movie_list: foobar
```

```yaml
manage_list
  remove:
    - trakt_list:
        username: a_different_username
        list: watchlist
        type: movies
```


## list_accept, list_reject, list_queue mess
```yaml
match_list:
  from:
    - [list](/list)
  [action](/action): [*accept*|reject](/*accept*|reject)
  [remove_on_match](/remove_on_match): [*yes*|no](/*yes*|no)
  [multiple_matches](/multiple_matches): [yes|*no*](/yes|*no*)
```

default marked with *

examples:

```yaml
match_list:
  from:
    - trakt_list:
        username: traktusername
        list: watchlist
        type: movies
  action: accept
```
