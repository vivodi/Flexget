## `pending`
View and manage entries [pending approval](plugin:pending_approval).

### Sub-commands
| Sub-command | Option | Description |
| --- | --- | --- |
| `list` | List pending entries |
|| *optional:* ||
|| `--task-name <task_name>` | Filter by `<task_name>` |
|| `--approved` | Show only approved entires|
|| `--pending` | Show only pending entires|
|| [`--table-type {plain,porcelain,github,single,double}`](/cli/misc/table-styles) | Select output table style |
|| [`--porcelain`](/cli/misc/table-styles) | Make the output parseable. Similar to using `--table-type porcelain` |
| `approve` || Approve pending entries |
|| *positional:* ||
|| `(<entry_id>\|all)` | Approve one pending entry by ID, or all pending entries |
| `reject` || Reject pending entries |
|| *positional:* ||
|| `(<entry_id>\|all)` | Reject one pending entry by ID, or all pending entries |
| `clear` | Clear all unapproved pending entries |
|| *optional:* ||
|| `--task-name <task_name>` | Filter by task name ||

### Examples
```console
# List all pending entries
$ flexget pending list

# Approve all pending entries
$ flexget pending approve all
```