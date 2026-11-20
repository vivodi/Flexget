# Archive
The archive plugin will keep a history of all entries from a given task, whether they have been accepted or not. This archive can then later be searched, and entries injected into a task again.


Simply enable without any tagging.

```yaml
archive: yes
```

With tagging:

```yaml
archive: [torrent, tv]
```

Search (via commandline):

```console
$ flexget archive search [@TAG] [@TAG] KEYWORD
```
Note: if keyword has spaces it must be quoted.

Retrieve and inject into task (via commandline):

```console
$ flexget archive inject ID [FORCE]
```
For more examples and complete commandline/CLI usage see the [CLI archive](/cli/archive) article.

## Urlrewriter
```yaml
flexget_archive: yes
```

or

```yaml
flexget_archive: [tag, tag]
```

This works with <plugin:discover> and also with urlrewriting but has less use in there.

## See also
- [`flexget_archive` as search plugin for `discover`](plugin:flexget_archive)