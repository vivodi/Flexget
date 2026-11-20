# A simple ebook recipe
## Using download plugin
This recipe uses the regexp plugin to download torrents from an rss feed to a specified path.

```yaml
tasks:
  books:
    rss: http://example.com
    regexp:
      accept:
        - Some Publisher
        - Some Magazine
    download: /path/to/torrents/
```

Uses plugins:  <plugin:regexp>,<plugin:download>