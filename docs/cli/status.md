# `status`
View task health status.

## Optional arguments
| Argument | Description |
| --- | --- |
| `--task <task>` | Limit to results in specified `<task>` |
| `--limit <num>` | Limit to `<num>` results (default `50`) |
| [`--table-type {plain,porcelain,github,single,double}`](/cli/misc/table-styles) | Select output table style |
| [`--porcelain`](/cli/misc/table-styles) | Make the output parseable. Similar to using `--table-type porcelain` |

## Subcommands

| Command | Description |
| --- | --- |
| remove | Remove a task and all its execution records. Supports glob pattern matching.| 

## Examples
```console
#shows the status for all tasks
$ flexget status

#displays status of the "foo_queue" task in porcelain table layout
$ flexget status --task "foo_queue" --porcelain
```