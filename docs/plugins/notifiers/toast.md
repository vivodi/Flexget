# Toast
:::{tip}
Toast is a part of the [notifier](/plugins/index.md#notifier-services-output) plugin system.
:::

**`Requirement:`**
Either:
- Must have a notification system like dbus for linux operating systems. Has been tested on Ubuntu 12.04 only!
- Preliminary support for Windows notifications. Not heavily tested yet.


## Configuration

| Option |Type|  Description | Default |
| --- | ---| --- |---|
|timeout|numeric|Number of seconds to display notification|`4`


**Examples:**
:::{warning}
Examples show a specifc scenario usage of the <plugin:notify> plugin. See its wiki for a more detailed usage exaplantion.
:::

**Basic:**
```yaml
notify:
  task:
    via:
      - toast: yes
```

**With timeout:**
```yaml
notify:
  task:
    via:
      - toast:
          timeout: 5
```
<div class="alert alert-warning">
  
  <!--<span class="glyphicon glyphicon glyphicon-cog"></span>-->
  &nbsp; <strong>Warning!</strong> Please ensure you have a notification system on your distribution before enabling this option.
</div>


