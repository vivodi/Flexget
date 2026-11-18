# XMPP
:::{tip}
XMPP is a part of the [notifier](/plugins/index.md#notifier-services-output) plugin system.
:::

This plugin sends messages via XMPP, has been tested on Windows 7/64 so far, sending messages to Google Hangouts recipients.

## Preparations

The `sleekxmpp` library is required to be installed. Install it with: `pip install sleekxmpp`.

## Configuration

| Option |Type|  Description | Default |
| --- | ---| --- |---|
|**sender**|email|Sender's JID. **Required**
|**password**|text|Sender's password. **Required**
|**recipients**|email|Recipients JID. Can also be a list. **Required**

:::{warning}
Examples show a specifc scenario usage of the <plugin:notify> plugin. See its wiki for a more detailed usage exaplantion.
:::

```yaml
notify:
  entries:
    via:
      - xmpp:
          sender: from_jid@whatever.com
          password: mypassword
          recipients: to_jid@whatever.com
```
