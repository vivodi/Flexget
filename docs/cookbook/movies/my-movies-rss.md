## Generate my (unwatched) movies list with Imdb details
Generates RSS with Imdb details, ordered by imdb score. Throw in <plugin:imdb_rated> and you get list of unwatched movies!

```yaml
templates:
  generate:
    interval: 4 hours
    accept_all: yes
    imdb_lookup: yes
    disable_builtins: yes
    sort_by:
      field: imdb_score
      reverse: yes

tasks:

  rss-unwatched:
    template: generate
    filesystem: /storage/movies/
    make_rss:
      file: ~/public_html/movies.rss
      history: no
```

Uses plugins: <plugin:template>, <plugin:imdb_lookup>, <plugin:make_rss>, <plugin:filesystem>