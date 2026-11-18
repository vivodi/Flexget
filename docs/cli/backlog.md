# `backlog`
View or clear entries from the <plugin:backlog> plugin.
## Actions
| Argument | Option | Description |
| --- | --- | --- |
| `list` || Show items in backlog |
|| *positional:*|
| | `<task_name>`| Limit to items from specified `<task_name>`|
|| *optional:*|
|| [`--table-type {plain,porcelain,github,single,double}`](/cli/misc/table-styles) | Select output table style |
|| [`--porcelain`](/cli/misc/table-styles) | Make the output parseable. Similar to using `--table-type porcelain` |
| `clear` || Clear all items in backlog |

## Examples
```console
#lists entries from the backlog of task "foo_task"
$ flexget backlog list foo_task

#lists entries from the backlog of task "foo_task" with porcelain table type
$ flexget backlog --porcelain list foo_task
```