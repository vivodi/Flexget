# Notify My Android
:::{tip}
Notify My Android can be used as a part of [notifier](/plugins/index.md#notifier-services-output) plugin system.
:::


Now defunct May 2018 - This plugin provides the ability to send flexget notifications via the  notification system called [Notify My Android](http://www.notifymyandroid.com/).

## Configuration

| Option |Type|  Description | Default |
| --- | ---| --- |---|
| **api_key**| text| User's API key. **Required.**| 
|application|text|Applicaiton name to display|`FlexGet`
|url|URL|Notification URL | Gets default from <plugin:notify> plugin
|priority|numeric|Sets notification priority. Can be between -2 and 2.
|html|yes/no|Parse message as HTML
|developer_key|text|Optional developer key


#### Examples
:::{warning}
Examples show a specifc scenario usage of the <plugin:notify> plugin. See its wiki for a more detailed usage exaplantion.
:::

```yaml
notify:
  entries:
    via:
      - notifymyandroid:
          api_key: API_KEY
```

#### Advanced Example
```yaml
notify:
  entries:
    via:
      - notifymyandroid:
          api_key: API_KEY
          application: Application name
          priority: 2
          url: http://server.example.com/path/to/downloader/ui
          html: yes
```
