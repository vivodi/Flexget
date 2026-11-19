# Command Line Interface (CLI)
FlexGet is usually invoked as a [Daemon](/guide/daemon) or via [cron](/guide/installation/linux/scheduling.md#using-cronjobs), configured with its [configuration](/guide/configuration/index) file. Many functions can also be performed on the command line. The following information can be seen on the command line by invoking `flexget --help` or the equivalent `flexget -h`.

```{toctree}
:caption: Top-level subcommands
:glob:
:hidden:

*
```

## Usage
FlexGet is invoked from the command line like so:
```console
$ flexget <argument> <command> <command-arguments>
```
For example, the FlexGet configuration file can be checked against configuration errors by calling `flexget check`. This particularly useful command should be ran whenever you make changes or after [upgrading](/guide/upgrading/index).

### `<command>`
In the above example, `check` is the `<command>` being used. 

### `<argument>`
One-letter "shortcut" arguments are prefixed with a single dash (`-`). The long form of arguments are prefixed with two dashes (`--`).

Some arguments are directed to FlexGet itself, such as `--loglevel`. They change the overall settings of the FlexGet operation or output. These are placed before the command when invoking FlexGet.

Most commands also have arguments. In the command `flexget execute --task awesome`, `--task awesome` is an argument to the `execute` command. These direct specific commands to operate in certain ways, or to perform particular functions, such as executing the task named `awesome` in the above example. Because they affect specific commands, they follow those commands when invoking FlexGet.

Some commands will have mandatory arguments called positional arguments or actions. These are not prefixed and look like commands. FlexGet has a lot of list-type options/arguments. These usually support different [output table styles](misc/table-styles).

## Top-level subcommands
Clicking on the commands will take you to a page with more information about it.
| Command | Description |
| --- | ---|
| [`archive`](archive) | Search and manipulate the archive database|
| [`backlog`](backlog) | View or clear entries from the <plugin:backlog> plugin |
| [`check`](check) | Validate [configuration file](/guide/configuration/index) and print errors |
| [`daemon`](daemon) | Run continuously, executing tasks according to [schedules](plugin:scheduler) defined in config |
| [`database`](database) | Utilities to manage the FlexGet database |
| [`doc`](doc) | Display [plugin](/plugins/index) documentation |
| [`entry-list`](entry-list) | View and manage [entry lists](plugin:entry_list) |
| [`execute`](execute) | Execute tasks now |
| [`failed`](failed) | List or clear remembered [failures](plugin:retry_failed) |
| [`history`](history) | View the history of entries that FlexGet has accepted |
| [`inject`](inject) | Inject an entry from the CLI into tasks |
| [`irc`](irc) | View and manage <plugin:irc> connections |
| [`jinja-filters`](jinja-filters)| View avaialble [Jinja](/guide/jinja) filters|
| [`movie-list`](movie-list) | View and manage [movie lists](plugin:movie_list) |
| [`pending`](pending)| View and manage entries [pending approval](plugin:pending_approval)|
| [`pending-list`](pending-list)| View and manage [pending lists](plugin:pending_list)|
| [`plugins`](plugins) | Print registered plugin summaries |
| [`regexp-list`](regexp-list) | View and manage [regexp lists](plugin:regexp_list) |
| [`rejected`](rejected) | List or clear [remembered rejections](plugin:remember_rejected) |
| [`seen`](seen) | View or forget entries remembered by the <plugin:seen> plugin |
| [`series`](series) | View and manipulate the <plugin:series> plugin database | 
| [`service`](service)| Install a Windows service which runs the FlexGet daemon|
| [`status`](status) | View task health status |
| [`templates`](templates)| View file templates to be used with [notifer](/plugins/index.md#notifier-services-output) plugins|
| [`trakt`](trakt) | View and manage [Trakt authentication](/guide/trakt.md/#trakt-authentication) |
| [`web`](web) | Manage [web server](/guide/web-ui/index) settings |

## Top-level options
| Argument | Description |
| --- | --- |
| `-h, --help` | Show help message and exit. Note that most commands support this as an argument to the command as well, such as `flexget series show -h` for help on how to use `series show`. This particular argument always follows the command (and any arguments to the command). |
| `-V, --version` | Print FlexGet version and exit. |
| `--test` | Copies the database and executes task(s) in a testing mode. Prints a `verbose` log of what would happen on normal execution. (Note some plugin network functionality is disabled during `--test`.)|
| `-c CONFIG` | Specify configuration file (optionally with path). Default: `config.yml` |
| `--logfile LOGFILE, -l LOGFILE` | Specify a custom logfile filename (optionally with path). Default: `flexget.log` in the config directory. |
| `--loglevel LEVEL, -L LEVEL` | Set the verbosity of the logger. Levels: `critical`, `error`, `warning`, `info`, `verbose`, `debug`, `trace` |
| `--bugreport` | Create a detailed bug report for use in reporting an issue on [GitHub](https://github.com/Flexget/Flexget/issues). Note that the output might contain _private_ data, such as URLs or IP addresses, so edit that out before posting or submitting it. |
| `--profile [OUTFILE]` | Use the Python profiler for this run to debug performance issues. |
| `--cron` | Used when executing FlexGet non-interactively. This allows background maintenance to run, disables stdout and stderr output, and reduces the logging level to `info`. |
| `--debug-warnings` | Elevate warnings to errors for debugging purposes, so a traceback is shown.
| `--debug-db-sessions` | Debug session starts and ends, for finding problems with database locks. |

```{toctree}
:caption: Miscellaneous
:glob:
:hidden:

misc/*
```
