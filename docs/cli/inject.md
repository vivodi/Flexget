# `inject`
Execute tasks immediately with an injected entry from the CLI, loosely equivalent to `execute --inject`.

## Description
`inject` expects to be passed a title and a URL. If only a URL is passed, Flexget attempts to find a suitable title from the response headers when that URL is requested. If, even after this, no title was found, the command will abort.

Alternatively, you can use the [](execute) command with the `--inject` argument. The only difference is that unlike the `inject` command, `--inject` treats a single argument as `title` and sets `url` to `http://localhost/inject/` followed by a random 30-character alphanumeric string.

## Arguments
Inherits all arguments from [](execute), and also supports the following arguments:

| Argument | Description |
| --- | --- |
| `<title>` | Title of the entry to inject |
| `<url>` | Url of the entry to inject |
| `--force` | Prevent any plugins from rejecting this entry |
| `--accept` | Accept this entry immediately upon injection|
| `--fields <entry_field=value> [<entry_field=value> ...]` | Populate additional fields in the entry |

## Examples
```console
#Example, passing both title and URL (for example if the remote server doesn’t return a filename in its response headers)
$ flexget inject "your.tv.show.s01e01.720p.web-dl.mkv" "http://example.com/torrents.php?id=33"

#Example, passing only a URL (will fail if no title can be determined)
$ flexget inject "http://example.com/torrents.php?id=33"

#Arguments for the execute command can be appended, for example to tell a particular task to run with the injected entry
$ flexget --test inject "http://example.com/your.tv.show.s01e01.torrent" --tasks yourtask --dump
```