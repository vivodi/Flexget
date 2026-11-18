# Join
> Join is a part of the [notifier](/plugins/index.md#notifier-services-output) plugin system.
{.is-success}



This plugin provides the ability to send flexget notifications via the cross-platform notification system called [Join](https://joaoapps.com/join/).

## Configuration

| Option |Type|  Description | Default |
| --- | ---| --- |---|
| **api_key**| text| User's API key. **Required.**| 
| device| text| Device ID. Can also be a list. Can not select together with `group`|
| device_name| text| Device name. Can also be a list. |
|group|text|Sepcifed device group to send notification to. One of `all`, `android`, `chrome`, `windows10`, `phone`, `tablet` or `pc`. can not select together with `device`|`all`
|url|URL|Notification URL | Gets default from <plugin:notify> plugin
|icon|URL|Notification icon
|sms_number|text|Send an SMS to this nubmer using device (in addition to regular notification). Will use `message` as SMS body
|priority|numeric|Sets notification priority. Can be between -2 and 2.


#### Examples
> Examples show a specifc scenario usage of the <plugin:notify> plugin. See its wiki for a more detailed usage exaplantion.
{.is-warning}

```yaml
notify:
  entries:
    via:
      - join:
          api_key: API_LEY
```


#### Advanced Example
```yaml
notify:
  entries:
    via:
      - join:
          api_key: KEY
          device: 
            - DEVICE1
            - DEVICE2
          group: windows10
          priority: 2
          url: http://server.example.com/path/to/downloader/ui
          icon: http://bla.com/image.jpg
          sms_number: '1800555555'
```
