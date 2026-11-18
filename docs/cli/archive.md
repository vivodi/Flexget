# `archive`
Search and manipulate the <plugin:archive> plugin database.

## Sub-commands
| Sub-command | Option | Description |
| --- | --- | --- |
| `search` || Search from the archive |
|| *positional:* ||
|| `<keyword>` | Keyword(s) to search for |
|| *optional:* ||
|| `--tags <tag> [<tag> ...]` | Tag(s) to search within |
|| `--sources <source> [<source> ...]` | Source(s) to search within |
|| [`--table-type {plain,porcelain,github,single,double}`](/cli/misc/table-styles) | Select output table style |
|| [`--porcelain`](/cli/misc/table-styles) | Make the output parseable. Similar to using `--table-type porcelain` |
| `inject` || Inject entries from the archive back into tasks |
|| *positional:* ||
|| `ID` | Archive ID of an item to inject |
|| *optional:* ||
|| `--immortal` | Injected entries will not be able to be rejected by any plugins |
|| *execute arguments:* ||
||| Arguments from the [`execute` command](/CLI/execute) are allowed here |
| `tag-source` || Tag all archived entries within a given source | 
|| *positional:* ||
|| `<source>` | The source whose entries you would like to tag |
|| `<tag>` |  The tag(s) you would like to apply to the entries |
| `consolidate` || Migrate old archive data to new model. This may take a long time. |

## Examples
```console
#searches the archive for "foo"
$ flexget archive search "foo"
```