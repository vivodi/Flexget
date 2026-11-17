# Sequence

Mainly for advanced usecases. Run any plugins in order. 

### Simple Example

```yaml
sequence:
  - rss: http://example1.com
  - rss: http://example2.com
```
Note: Using <plugin:inputs> plugin would be more appropriate use for this usecase.

### Advanced Example

Here we using the <plugin:configure_series> plugin using two separate Trakt lists, and applying a different set of settings to each list. This could then be used with the <plugin:discover> plugin in a task

```yaml
    sequence:
      - configure_series:
          from:
            <<: *trakt_tv_list
          settings:
            target: 1080p hdtv+
            quality: 1080p webrip+
            timeframe: 18 hours
      - configure_series:
          from:
            <<: *trakt_tv4k_list
          settings:
            quality: 2160p webrip+ !dolbyvision
```
