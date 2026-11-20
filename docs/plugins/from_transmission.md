# From Transmission
This plugin creates an entry for each item you have loaded in transmission.

:::{warning}
This plugin requires the `transmission-rpc` library. 
Newer versions of FlexGet require `transmission-rpc` 4.1.4 or greater.
:::

To install it, run:
```console
$ pip install transmission-rpc
```

You may be required to upgrade transmission-rpc after upgrading transmission, for that just add `--upgrade` to the previous command.

## Options

| Name | Info | Description |
| --- | --- | --- |
| host | Text | Where transmission is listening (default: localhost) |
| port | Number | Connected port (default: 9091) |
| netrc | File |  |
| username | Text |  |
| password | Text |  |
|enabled| Text||
| only_complete | [yes\|no] | If this is enabled, only completed torrents, which have also finished their seeding requirements will have entries created. |


**Example:**

```yaml
from_transmission:
  host: localhost
  port: 9091
  username: myusername
  password: mypassword
```


