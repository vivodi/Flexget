# Include
Allows including configuration from another file into a task.

## Example

**config.yml**

```yaml
tasks:
  stuff:
    rss: ...
    include: series.yml
    download: ~/downloads/
```

**series.yml**

```yaml
series:
  - foo
  - bar
```

This allows parts of configuration to be shared between multiple configuration files (databases).

You can also include multiple files using this format:
```yaml
include:
  - include1.yml
  - include2.yml
```