# Set torrent client download path from series name
When using a bittorrent client plugin as your output plugin, (<plugin:deluge> or <plugin:transmission>,) you can <plugin:set> the `path` field of an entry to control where the client will save the content (the set plugin is also available as a per series option). This, combined with [jinja formatting](/guide/jinja) allows all series to be easily downloaded to separate series and season folders. This recipe uses the transmission plugin, but that can easily be replaced with the deluge plugin.

```yaml
tasks:
  task-a:
    rss: http://example.com
    series:
      settings:
        seriesgroup:
          set:
            path: /series/location/{{series_name}}/Season {{series_season}}
      seriesgroup:    
        - Foo
        - Bar
        - CustomPathSeries:
            set:
              path: /series/location/CustomFolder/
    transmission: yes
```

Uses plugins: <plugin:rss>, <plugin:series>, <plugin:set>, <plugin:transmission>