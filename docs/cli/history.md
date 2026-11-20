# `history`
View the history of entries that FlexGet has accepted.

## Optional arguments
| Argument | Description |
| --- | --- |
| `--limit <num>` | Limit to `<num>` results |
| `--search <term>` | Limit to results that contain `<term>` |
| `--task <task>` | Limit to results in specified `<task>` |
| `--short`, `-s` | Shorter output |
| [`--table-type {plain,porcelain,github,single,double}`](/cli/misc/table-styles) | Select output table style |
| [`--porcelain`](/cli/misc/table-styles) | Make the output parseable. Similar to using `--table-type porcelain` |

## Examples
```console
$ # displays the accepted history in porcelain table format
$ flexget history --porcelain
```