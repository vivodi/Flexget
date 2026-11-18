# Bark
:::{tip}
Bark is a part of the [notifier](/plugins/index.md#notifier-services-output) plugin system.
:::

This plugin allows Flexget to send notifications to a [Bark](https://github.com/Finb/bark-server) client via the bark [API_V2](https://github.com/Finb/bark-server/blob/master/docs/API_V2.md).

## Configuration

| Option |Type|  Description | Default |
| --- | --- | --- | --- |
| **server** | string | URL of the Bark server. **Required**
| **device_key**| string | Key of the device. **Required**
| level | string | `'active'`, `'timeSensitive'`, or `'passive'`. |
| badge | integer | The number displayed next to App icon. ([Apple Developer](https://developer.apple.com/documentation/usernotifications/unnotificationcontent/1649864-badge)) |
| automatically_copy | boolean | Automatically copy to the clipboard. |
| copy | string |  The value to be copied. |
| sound | string | Value from [here](https://github.com/Finb/Bark/tree/master/Sounds). |
| icon | string | An url to the icon, available only on iOS 15 or later. |
| group | string | The group of the notification. |
| is_archive | boolean | Whether or not should be archived by the app. |
| url | string | Url that will jump when click notification. |



## Examples
:::{warning}
Examples show a specifc scenario usage of the <plugin:notify> plugin. See its wiki for a more detailed usage exaplantion.
:::

This example sends a notification by the default settings.

```yaml
notify:
  entries:
    title: |
          {{task}}
    message: |
          {% if series_name is defined %}{{series_name}}{% if series_id is defined %} - {{series_id}}{% endif %}{% if trakt_ep_name is defined %} - {{trakt_ep_name}}{% endif %}
          {% elif imdb_name is defined%}{{movie_name}}
          {% else %}{{title}}
          {% endif %}
    via:
      - bark:
          server: https://******
          device_key: ******
```