# Set 2.0
```yaml
set:
  FIELD_NAME: <string format>

  FIELD_NAME:
    {value]: <string format>
    regexp: <regexp groups>
    replace: [<regexp what>, <with text>]
```

**Simple example:**

```yaml
set:
  path: /foo/bar/%(series_name)s/
```


**Advanced example:**

```yaml
set:
  path:
    value: /foo/bar/%(series_name)s/
    replace: [' ', '.']
```