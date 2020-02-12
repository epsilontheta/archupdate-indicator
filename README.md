# Arch Update Indicator
> Creates a taskbar icon that indicates if updates are available and provides a context menu to inspect and install them.

Uses wxpython to create a taskbar icon that visually indicates if updates are available using `checkupdates` from the pacman-contrib package.

You can use `UPDATE_CMD` environment variable to configure the command that will be executed to update (default is `sudo pacman -Syu`).
The `ICONS_FOLDER` environment variable is used to configure the path where the icons are stored (default is `/usr/share/pixmaps/archupdate-indicator`).
With `UPDATE_PERIOD` the time between checking for updates is set in ms (default 1h).
Use `TERMINAL` to change the terminal emulator (default is `xterm`).

## Installation

### Manual installation

```sh
# install dependencies
pacman -S pacman-contrib python-wxpython
git clone 'https://github.com/epsilontheta/archupdate-indicator.git'
cd archupdate-indicator/
cp archupdate-indicator.py /usr/local/bin/
cp -r img/ /usr/share/pixmaps/archupdate-indicator
```

### AUR

https://aur.archlinux.org/packages/archupdate-indicator/

## Release History

* 1.0.0
    * Add return code 2 handling of checkupdates
* 0.0.2
    * Add additional environment variables
* 0.0.1
    * Initial release
