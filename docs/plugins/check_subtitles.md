# Check subtitles
Set the **subtitles** field on all [entries](/guide/entry) about local files having subtitles. The field is a list of available languages.

## Example
```yaml
check_subs:
    filesystem:
      path:
        - D:\Media\Incoming\series
      regexp: '.*\.(avi|mkv|mp4)$'
      recursive: yes
    check_subtitles: yes
    if:
      - "subtitles and 'ita' in subtitles": accept
```