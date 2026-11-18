## `regexp-list`
View and manage [regexp lists](/Plugins/List/regexp_list).

### Sub-commands
| Sub-command | option | description |
| --- | --- | --- |
| `all` || Shows all existing regexp lists |
|| *optional:*  ||
|| [`--table-type {plain,porcelain,github,single,double}`](/cli/misc/table-styles) | Select output table style |
|| [`--porcelain`](/cli/misc/table-styles) | Make the output parseable. Similar to using `--table-type porcelain` |
| `list` || List regexps from a list |
|| *positional:* ||
|| `<list_name>` | Name of the list to display | 
|| *optional:* ||
|| [`--table-type {plain,porcelain,github,single,double}`](/cli/misc/table-styles) | Select output table style |
|| [`--porcelain`](/cli/misc/table-styles) | Make the output parseable. Similar to using `--table-type porcelain` |
| `add` || Add a regexp to a list | 
|| `<list_name>` | Name of the list to add to | 
|| `<regexp>` | The regexp to add |
| `del` || Remove a regexp from a list | 
|| *positional:* ||
|| `<list_name>` | Name of the list to remove from | 
|| `<regexp>` | The regexp to remove |
| `purge` || Removes an entire list; use this with caution |
|| *positional:* ||
|| `<list_name>` | Name of the regexp list to remove |


### Examples
```console
#lists all existing regexp lists
$ flexget regexp-list all
```