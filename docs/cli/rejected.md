# `rejected`
List or clear [remembered rejections](plugin:remember_rejected).

## Sub-commands
| Sub-command | option | description |
| --- | ---| --- |
| `list` || List all entries that have been rejected |
|| *optional:* ||
|| [`--table-type {plain,porcelain,github,single,double}`](/cli/misc/table-styles) | Select output table style |
|| [`--porcelain`](/cli/misc/table-styles) | Make the output parseable. Similar to using `--table-type porcelain` |
| `clear` || Clear all rejected entries from the database so they can be retried |

## Examples
```console
#lists all rejected entries
$ flexget rejected list
```