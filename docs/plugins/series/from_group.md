## Specify group (eg. anime fansubs)

**Example:**

```yaml
series:
  - some series name:
      from_group: fansubber 1
  - another series name:
      from_group:
        - fansubber 1
        - fansubber 2
```

**Supported notations:**

 * [Group] Series
 * Series XviD-Group

To disallow certain groups use <plugin:regexp> plugin to reject them.
