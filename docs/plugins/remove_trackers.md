# Remove Trackers
Removes trackers from torrent files using regexp matching. Also works on magnet urls.

## Example
```yaml
remove_trackers:
  - moviex
```

This will remove all trackers that contain text moviex in their url.  
TIP: You can use global <plugin:template> in configuration to make this enabled on all tasks.