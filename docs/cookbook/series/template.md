# Manage series and multiple feeds easily with a template
With <plugin:template> plugin you can avoid having to duplicate configuration in multiple tasks. This can be adapted for movies, comics etc. easily. See <plugin:template> documentation for more tips.

```yaml
templates:
  tv:
    download: ~/torrents/series/
    exists_series: ~/storage/series/
    series:
      - pioneer one
      - south park

tasks:
  some-feed:
    rss: http://example.com/feed.xml
    template: tv

  another-feed:
    rss: http://foobar.com/feed.xml
    template: tv
```  

Uses plugins: <plugin:template>, <plugin:rss>, <plugin:series>, <plugin:exists_series>, <plugin:download>

[Back to The Cookbook](/cookbook/index)