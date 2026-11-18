# `execute`
Execute tasks now. If FlexGet is not running as a [daemon](/Daemon) or via [cron](/InstallWizard/Partial/Crontab), this is the only way tasks can be executed.

```{toctree}
:glob:
:hidden:

execute/*
```

## Arguments
| Argument | Description |
| --- | --- |
| [`--tasks <task> [<task> ...]`](execute/--tasks)| Run only specified task(s), optionally using glob patterns ("tv-*"); matching is case-insensitive |
| `--learn` | Matches are not downloaded but will be skipped in the future |
| `--no-cache` | Disable caches; works only in plugins that have explicit support |
| `--stop-waiting <name>` | Stop [timeframe](plugin:series/timeframe) for a given series |
| `--tail-reset <file\|task>` | reset <plugin:tail> position for a file or an entire task|
| `--discover-now` | Immediately try to discover everything, bypassing the `discover` option [`interval`](plugin:discover#interval) |
| `-T NAME, --template <name>` | Execute tasks using given template |
| `--now` | Run task(s) even if the <plugin:interval> plugin would normally prevent it |
| `-v, --verbose` | Verbose undecided entries |
| `-s, --silent` | Don't verbose any actions (accept, reject, fail) |
| `--dump-config` | Display the config of each task after template merging/config generation occurs |
| `--dump [{eval,trace,accepted,rejected,undecided,title} [{eval,trace,accepted,rejected,undecided,title} ...]]` | Display all entries in task with fields they contain after task execution. Use `--dump eval` to evaluate all lazy fields; specify an entry state or states to only dump matching entries |
| `--dl-path <path>` | Override path for download plugin; this applies to all executed tasks |
| [`--cli-config <variable=value> [<variable=value> ...]`](execute/--cli-config) | Use dynamic configuration values to replace keywords in your configuration file |
| [`--try-regexp`](execute/--try-regexp)| Test how regexps work on task(s) interactively|
| [`--inject`](execute/--inject) | Injects custom entry into task(s)|

## Examples
```console
#executes the "foo_task"
$ flexget execute --tasks foo_task
```