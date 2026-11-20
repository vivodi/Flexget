# Require field
This plugin will reject any [entries](/guide/entry) that do not have the specified [fields](/guide/entry.md#known-fields). Also rejects if specified field is present, but is an empty string.

**Example:**

This example does the same thing as the `imdb_required` plugin. (As long as <plugin:imdb_lookup> is also enabled on the task.)
```yaml
require_field: imdb_id
```

**Example:**

This example will reject entries that do not have parsed series information.
```yaml
require_field:
  - series_name
  - series_season
  - series_episode
```