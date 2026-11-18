# OSX

macOS (previously called OS X) ships with a version of Python installed, but it is usually not the latest version, and installing additional packages against the system version is not recommended. If you don't already have a separate Python installation, the easiest and safest way is to install a separate copy of Python for use with FlexGet.

## Homebrew
On macOS 10.10 or higher, the easiest way to install Python, pip, and FlexGet is using [Homebrew](https://brew.sh/), also known as simply Brew. (This may work on prior versions of macOS, but Homebrew is not officially supported prior to 10.10.)

First, open Terminal and install the Xcode Command Line Tools using this command:
```console
$ xcode-select --install
```

Then install Homebrew using this command:
```console
$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Once Homebrew has been installed, modify your PATH. Edit your `~/.profile` file:
```console
$ nano ~/.bash_profile
```

Add this at the bottom by using your arrow keys to navigate and pasting it on a new line.
```console
export PATH="/usr/local/bin:/usr/local/sbin:~/bin:$PATH"
```

Press Control+X which will prompt you to save (press Y then Enter) and exit.

Run this command so your shell reflects the changes you just made:
```console
$ source ~/.bash_profile
```

## Continue
```{toctree}
:maxdepth: 1
python
flexget
autorun
```
