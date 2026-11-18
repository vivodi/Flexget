# SMS RU

:::{tip}
SMS RU can be is a part of the [notifier](/plugins/index.md#notifier-services-output) plugin system.
:::

This plugin provides the ability to send flexget notifications via the cross-platform notification system called [SMS RU](http://sms.ru/).

## Configuration

| Option |Type|  Description | Default |
| --- | ---| --- |---|
|**phone_number**|text|Phone number to SMS. **Required**
|**password**|text|Service password. **Required**

#### Example:
:::{warning}
Examples show a specifc scenario usage of the <plugin:notify> plugin. See its wiki for a more detailed usage exaplantion.
:::

```yaml
notify:
  entries:
    via:
      - sms_ru:
          phone_number: 6534563456345
          password: PASSWORD
```

