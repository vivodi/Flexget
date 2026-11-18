# Upgrading git checkout

>Detailed changes can be found from [ChangeLog](/ChangeLog).
{.is-info}

## Check current version

Check the latest release you have by getting new tags with `git fetch --tags` then running `git describe`.

Write this version number down somewhere.

```{include} _includes/backup.md
```

## Upgrade GIT checkout

Git users can just run `git pull`. If the dependencies have changed, you'll also have to run `uv sync` again to upgrade them. Remember to use `--group NAME` or `--all-groups` (for everything) or `uv` will uninstall unwanted dependencies which you may actually want to keep.

```{include} _includes/verify.md
```
