# torrent

```{note}
This is a **built-in** plugin. It is enabled automatically for all tasks and does not require any configuration.

```

The `torrent` plugin automatically detects, validates, and parses downloaded `.torrent` files for accepted entries. It ensures that torrent files are intact, populates torrent metadata on the entry, guarantees a valid `.torrent` filename, and saves any modifications made to the torrent by other plugins.

## What It Does

### 1. Validation & Error Handling

When an accepted entry has an associated downloaded file that is identified as a torrent, the plugin performs two integrity checks:

* **Content length check:** If the server reported a `content-length`, the plugin verifies that the downloaded file size matches it.
* **Syntax check:** The plugin parses the file to ensure it is a valid, uncorrupted torrent.

If either check fails, the entry is marked as **failed** and the temporary file is automatically deleted.

### 2. Filename Normalization

The plugin ensures every torrent entry has a clean `filename` ending in `.torrent`:

* If a `filename` is already set (for example, by the `download` plugin) but lacks the `.torrent` extension, `.torrent` is appended.
* If no `filename` is set, one is automatically generated:
1. It starts with the entry's `title`.
2. If the torrent contains a **single file** whose name is longer than the entry title, that filename (without its original extension) is used instead.
3. Slashes (`/`) and spaces are replaced with underscores (`_`), and zero-width spaces (`\u200b`) are removed.
4. The `.torrent` extension is appended.



### 3. Writing Modified Torrents

During the output phase, if another plugin has modified the parsed `torrent` object on an entry, the `torrent` plugin automatically re-encodes and writes the updated torrent data back to the file on disk.

## Entry Fields Provided

Once a torrent file is successfully parsed, the following fields are added to the entry for use by other plugins or templates:

| Field | Description |
| --- | --- |
| `torrent` | The parsed `Torrent` object representing the file's contents and metadata. |
| `torrent_info_hash` | The unique info hash of the torrent. |
| `filename` | The normalized filename guaranteed to end with `.torrent`. |

```{tip}
You can reference `{{ torrent_info_hash }}` or `{{ filename }}` in Jinja2 templates for downstream plugins (such as notifications or custom output plugins).

```

```
