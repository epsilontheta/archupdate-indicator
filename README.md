# Arch Update Indicator
> Creates a taskbar icon that indicates if updates are available and provides a context menu to inspect and install them.

Uses wxpython to create a taskbar icon that visually indicates if updates are available using `checkupdates` from the pacman-contrib package.

You can use `UPDATE_CMD` environment variable to configure the command that will be executed to update (default is `sudo pacman -Syu`) and `ICONS_FOLDER` to configure the path where the icons are stored (default is `/usr/share/pixmaps/archupdate-indicator`).

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

TODO

## Release History

* 0.0.1
    * Initial release
