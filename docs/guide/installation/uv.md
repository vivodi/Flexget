# Installation via uv
[uv](https://docs.astral.sh/uv/) has multiple purposes, but one of them ([uv tool](https://docs.astral.sh/uv/guides/tools/)) is to easily install python based CLI tools (like FlexGet!) and not worry about the virtual environment or python management yourself. Here are the steps to install and update FlexGet using uv tool.

## Install uv
Instructions can be found [at the uv website.](https://docs.astral.sh/uv/getting-started/installation/)

## Install FlexGet
We can then use uv to install FlexGet:
```console
$ uv tool install flexget
```
or with fully locked dependency versions:
```console
$ uv tool install flexget[locked]
```
This will install FlexGet into a uv managed virtual environment, and add the binaries to your PATH.

The `locked` extra is not required, but is recommended, because it makes sure you get the exact dependencies that we have tested with.

### Specifying python version
You can also specify what version of python you would like to use
```console
$ uv tool install flexget[locked] --python 3.13
```

### Adding extras
There are several extras we include that install optional dependencies needed by some of the most common plugins. They are:
- [`boto3`](plugin:sns)
- <plugin:deluge>
- ftp (used by <plugin:ftp_list> and <plugin:ftp_download> plugins)
- <plugin:qbittorrent>
- [`plexapi`](plugin:plex)
- [`rarfile`](plugin:decompress)
- sftp (used by <plugin:sftp_list>, <plugin:sftp_download> and <plugin:sftp_upload> plugins)
- <plugin:subliminal>
- <plugin:transmission>
- <plugin:telegram>
- all (this will include all of the above)

You can specify them when installing and an appropriate version of the dependency will be installed and upgraded alongside flexget for you. e.g.
```console
$ uv tool install flexget[locked,all]
$ uv tool install flexget[locked,deluge,telegram]
```

If you need extra dependencies other than the extras listed above, they can also be specified.
```console
$ uv tool install flexget[locked] --with myotherdependency
```
:::{note}
If you later decide you want to switch python versions or change extras, you can simply run the `uv tool install` command again with your new options.
:::

## Run FlexGet
FlexGet will be added to your PATH, so you can run it from anywhere.
```console
$ flexget --help
```

## Updating
To update to the latest version of FlexGet, you can run:
```console
$ uv tool upgrade flexget
```
If you need to get a specific version, you can specify it:
```console
$ uv tool upgrade flexget==3.15.36
```
:::{warning}
You probably don't want to specify a specific FlexGet version during `uv tool install`, as this version constraint will keep applying when you try to `uv tool upgrade` later. It is better to do the install, then "upgrade" to the specific version you need right now.
:::

## Uninstalling
If you installed with this method, you can:
```console
$ uv tool uninstall flexget
```

## Next Step

Choose your OS to continue setting up scheduling:
 * [Linux](linux/scheduling)
 * [Windows](windows/scheduling)
 * [Mac OSX](macos/autorun)