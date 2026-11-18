# `failed`
list or clear remembered failures

## Sub-commands
| Sub-command | Option| Description |
| --- | ---| --- |
| `list` || List all the entries that have had failures |
||*optional:*||
|| [`--table-type {plain,porcelain,github,single,double}`](/cli/misc/table-styles) | Select output table style |
|| [`--porcelain`](/cli/misc/table-styles) | Make the output parseable. Similar to using `--table-type porcelain` |
| `clear` || Clear all failures from database so they can be retried |

## Examples
```console
#lists all the entries with failures
$ flexget failed list
```