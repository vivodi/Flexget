# Magnets
This plugin will remove any magnet links from the entry urls list, and reject any entries that only have magnet links. 

Since <plugin:torrent_cache> is a built-in plugin, this will mean that most entries fall back to a torrent cache link rather than being rejected. 

This is useful if you are using the <plugin:download> plugin as output, or if you are using the 
<plugin:content_filter> or <plugin:content_size> plugins, which cannot get the required information from magnets.

## Usage
```yaml
magnets: no
``` 