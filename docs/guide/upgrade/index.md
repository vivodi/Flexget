---
title: Upgrade
description: 
published: true
date: 2025-04-14T13:22:29.716Z
tags: 
editor: markdown
dateCreated: 2022-09-18T04:52:13.370Z
---

# Upgrading

> Before upgrading, check if your config or anything else needs updated on the [upgrade actions](/changelog/UpgradeActions) page.
{.is-warning}

```{toctree}
:hidden:
UpgradeActions
```

## Choose installation method

```{toctree}
:maxdepth: 1
Pip
Git
```

For uv tool installation, see [here](/guide/install/uv.md#updating).

### Problems ?

If you encounter problems, there are ways to get [help](/NeedHelp) !

If you receive errors about database upgrades please report them via an [issue](https://github.com/Flexget/Flexget/issues). If you do not care about the history for that plugin, you can reset the database for that plugin with `--reset-plugin PLUGINNAME` to get it working again.
