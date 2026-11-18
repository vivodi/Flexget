# Microsoft Teams
> Microsoft Teams is a part of the [notifier](/plugins/index.md#notifier-services-output) plugin system.
{.is-success}

This plugin allows Flexget to send notifications to a [Microsoft Teams](https://products.office.com/en-us/microsoft-teams/group-chat-software) channel via the [Incoming Webhooks](https://msdn.microsoft.com/en-us/microsoft-teams/connectors) functionality.

## Configuration

| Option |Type|  Description | Default |
| --- | ---| --- |---|
|**web_hook_url**|URL|Web hook URL. **Required**
|title|text|Message title
|message|text|Message to be sent
|theme_color|text|Set message color



## Examples
> Examples show a specifc scenario usage of the <plugin:notify> plugin. See its wiki for a more detailed usage exaplantion.
{.is-warning}

This example sends a Slack notification and overrides the default username and icon settings.

```yaml
notify:
  entries:
    via:
      - ms_teams:
          web_hook_url:  https://outlook.office.com/webhook/XXXXXXXXXXXXXXXXXZZZZZZZZZZZZZ
          title: Flexget
          message: Accepted title {{title}}
```