# Max Reruns

Simple plugin that limits the number of reruns a specific task is allowed to perform consecutively. Useful for limiting the number of reruns <plugin:discover> performs.

## Example

```yaml
  download-task:
    series:
      - Some Awesome Show
    discover:
      what:
        - next_series_episodes: yes
      from:
        - some_search_plugin: yes
    max_reruns: 3
```