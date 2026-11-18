# Install from Git
## Notes

 * Supported Python versions: {{ py_versions }}
 * Requires uv, and git client
 * This where we develop
 
## Install uv
uv is a Python package and project manager. Install instructions can be found [here.](https://docs.astral.sh/uv/getting-started/installation/)

## Initial clone
To checkout use this command:

```console
$ git clone https://github.com/Flexget/Flexget.git ~/flexget-dev
```

You can use whatever directory you like in place of `~/flexget-dev`.

## Create environment with uv sync
In your checkout directory, run:

```console
$ uv sync
```

This will create a virtualenv in the `.venv` directory within your checkout, and install flexget in editable mode, (such that editing your checkout will directly edit the copy of flexget that runs in your venv,) and all of the needed dependencies.

To install additional dependencies such as qbittorrent use:


```console
$ uv sync --group all
```

## Running FlexGet in the venv
To run Flexget (or any other command) inside the venv, you can use `uv run` followed by the command. e.g.
```console
$ uv run flexget execute
```
or, you can explicitly run the binaries from the venv
```console
$ ~/flexget-dev/.venv/bin/flexget execute
```

## Upgrading
To upgrade your install, first pull the changes from our repo:

```console
$ cd ~/flexget-dev
$ git pull
```

If the dependencies have changed, you can re-sync to upgrade all the dependencies:

```console
$ uv sync
```

## Become a contributor
If you're interested in helping to improve FlexGet, or adding new plugins, please read our [contribute page](/Contribute).
