# Upgrading

:::{warning}
Before upgrading, check if your config or anything else needs updated on the [upgrade actions](upgrade-actions) page.
:::

```{toctree}
:hidden:
upgrade-actions
```

## Choose installation method

```{toctree}
:maxdepth: 1
pip
git
```

For uv tool installation, see [here](/guide/installation/uv.md#updating).

### Problems ?

If you encounter problems, there are ways to get [help](/guide/support) !

If you receive errors about database upgrades please report them via an [issue](https://github.com/Flexget/Flexget/issues). If you do not care about the history for that plugin, you can reset the database for that plugin with `--reset-plugin PLUGINNAME` to get it working again.
