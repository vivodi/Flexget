# `pending-list`
View and manage [pending lists](plugin:pending_list).

## Sub-commands
| Sub-command | Option | Description |
| --- | --- | --- |
| `all` || Shows all existing entry lists |
|| *optional:* ||
|| [`--table-type {plain,porcelain,github,single,double}`](/cli/misc/table-styles) | Select output table style |
|| [`--porcelain`](/cli/misc/table-styles) | Make the output parseable. Similar to using `--table-type porcelain` |
| `list` || List entries from a list | 
|| *positional:* ||
|| `<list_name>` | Name of the list to display | 
|| *optional:* ||
|| [`--table-type {plain,porcelain,github,single,double}`](/cli/misc/table-styles) | Select output table style |
|| [`--porcelain`](/cli/misc/table-styles) | Make the output parseable. Similar to using `--table-type porcelain` |
| `show` || Show entry fields | 
|| *positional:* ||
|| `<list_name>` | Name of the list to display an entry from | 
|| `<entry>` | Entry title or ID from that list | 
| `add` || Add an entry to a list |
|| `list_name` | Name of the list to add to; if the list does not exist, it will be created | 
|| *positional:* ||
|| `<entry_title>` | Title of the entry | 
|| `<original_url>` | URL of the entry |
|| *optional:* ||
|| `--attributes <entry_field=value> [<entry_field=value> ...]` | Can be a string or a list of strings with the format imdb_id=XXX, tmdb_id=XXX, etc |
||`--approved`|Add an entry as already approved|
|`approve`||Mark an entry as approved|
|`reject`||Reject an apprvoed entry|
| `del` || Remove an entry from a list using its title or ID |
|| *positional:* ||
|| `<list_name>` | Name of the list to remove from | 
|| `<entry>` | Entry title or ID from that list | 
| `purge` || Removes an entire list with all of its entries; use this with caution |
|| *positional:* ||
|| `<list_name>` | Name of the list to remove |

## Examples

### Return all pending lists names
```console
$ flexget pending-list all
```

### List all entries from an pending list
```console
$ flexget pending-list list <list_name>
```

### Show details about a specific entry
```console
$ flexget pending-list show <list_name> <entry>
```

### Add or update an entry on an pending list and mark it as approved.
Using a title and original URL is require. You can also add additional identifiers in the following format:

```console
$ flexget pending-list add <list_name> <entry_title> <original_url> --attributes imdb_id=tt1234556 tmdb_id=1234 --approved
```

If the given entry list does not exist it will be created.

If the entry with the title exists on that list, its *entire* list of attributes will be replaced by the given list of attributes (or removed altogether if such a list was not given). 

### Removing an entry from an pending list
```console
$ flexget pending-list del <list_name> <entry>
```

### Clearing an entire pending list
```console
$ flexget pending-list purge <list_name>
```

## Approving an entry on a pending list
```console
$ flexget pending-list approve <list_name> <entry TITLE or ID>
```

### Rejecting an entry from a pending list
```console
$ felxget pending-list reject <list_name> <entry TITLE or ID>
```
