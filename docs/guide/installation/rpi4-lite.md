# RaspberryPi OS Lite

Install FlexGet into pipx managed virtualenv.

There may be better options for some of the steps, but this works (2022) well.

Install full python3

```console
sudo apt install python3-full libpython3-dev
```

Install distutils (necessary?)

```console
sudo apt install distutils
```

Install pip

(ensure-pip might work too?)

https://pip.pypa.io/en/stable/installation/#get-pip-py

Use get-pip.py

```console
cd /tmp
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
```

Install pipx, update path and reload changes

```console
python3 -m pip install --user pipx
~/.local/bin/pipx ensurepath
source ~/.bashrc
```

Install FlexGet

```console
~/.local/bin/pipx install flexget
```

Test, you should see version number

```console
flexget -V
```

## Installing extra dependencies with pipx

Our plugin documentation instructs to use pip to install libraries such as transmission-rpc. This needs to be adjusted with pipx

Use following pipx command instead:

```console
pipx inject flexget transmission-rpc
```


## Next Step

Continue to [Scheduling](/InstallWizard/Linux/Scheduling).