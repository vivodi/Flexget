# Nyaa
> This plugin is part of [search](/plugins/index.md#search) plugin system
{.is-success}

Search plugin which gives results from [nyaa.si](http://nyaa.si/)
### Config
Takes two options:

**Category:**

Valid choices are `all`, `anime`, `anime eng`, `anime non-eng`, and `anime raw`

**Filter:**

Valid choices are `all`, `filter remakes`, `trusted only`, and `a+ only`

### Example

```yaml
nyaa:
  category: anime eng
  filter: trusted only
```