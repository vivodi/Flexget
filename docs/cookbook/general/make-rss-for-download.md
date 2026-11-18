# Generate download RSS for other clients
This will produce rss-feed containing all matches with direct downloadable urls (resolved). This is useful if you wish to hook up FlexGet with a client that does not have a [watch directory](#watch-directory) support, or if you wish to perform downloading in a another computer. Only downside is that you need a HTTP server like Apache to host the RSS-feed.

:::{admonition} What is a watch directory
:class: tip
:name: watch-directory
Many applications support checking certain directory for new files. When new file (e.g. torrent, nzb) is placed in there they start downloading them automatically. These work excellently with FlexGet.
:::

```
templates:
  global:
    make_rss:
      link: url
      file: ~/public_html/flexget.rss

feeds:
  some feed:
    regexp:
      accept:
        - example

  another feed:
    series:
      - some series
```

Uses plugins: <plugin:template>, <plugin:make_rss>

[Back to The Cookbook](/Cookbook)

