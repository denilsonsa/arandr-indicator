arandr-indicator
================

Quick and simple tray icon menu for changing the monitor layout. A great companion to ARandR tool.

Demonstration video on YouTube:

[![YouTube demonstration](http://img.youtube.com/vi/xqpF6RrYUmo/0.jpg)](http://youtu.be/xqpF6RrYUmo)


Requirements
------------

* [ARandR](http://christian.amsuess.com/tools/arandr/) (optional)
* Python 2.7
* [PyGTK](http://www.pygtk.org/)
* [python-appindicator](https://launchpad.net/libappindicator)
* [PyXDG](http://freedesktop.org/wiki/Software/pyxdg/) (optional)
* Some kind of UI that supports [Unity indicators](https://unity.ubuntu.com/projects/appindicators/), should work on Gnome, KDE, Unity, LXDE…


How to use
----------

1. Run `arandr`.
2. Configure the monitor layout the way you like.
3. Save the layout.
    * ARandR tool will save the layout as a simple one-line shell script that calls `xrandr` with the appropriate commands. The script will be saved in `~/.screenlayout/`.
4. Magic! All layout scripts from that directory will automatically show up in the menu!


Installation
------------

1. `sudo apt-get install python-appindicator python-gtk2 python-xdg arandr`
2. Download [`arandr-indicator.py`](https://raw.githubusercontent.com/denilsonsa/arandr-indicator/master/arandr-indicator.py) and save it anywhere.
3. `chmod +x arandr-indicator.py` to make it executable.
4. `./arandr-indicator.py` to execute it.
5. Add it to autostart, so it runs whenever you login.

### Pre-built packages

* [arandr-indicator-git](https://aur.archlinux.org/packages/arandr-indicator-git/) for [Arch Linux](https://www.archlinux.org/), written by [thiagowfx](https://github.com/thiagowfx)

How to add icons
----------------

To define an icon for any `~/.screenlayout/*.sh` script, just add a line containing `META:ICON = "icon-name-here"` anywhere in the first 512 bytes of the file. The actual requirements are:

* The line must contain:
    * `META:ICON` string,
    * followed by optional whitespace (spaces or tabs),
    * followed by `=` (equals sign),
    * followed by optional whitespace (spaces or tabs),
    * followed by the icon name inside double-quotes.
* The icon name does not support escapes.
* The icon name cannot contain the double-quote character.
* The icon name can be:
    * A [standard icon name][icon-naming-spec] that is available in your current icon theme.
    * A filename to be found in `~/.screenlayout/`.
    * A relative path (will be considered relative to `~/.screenlayout/`).
    * A path relative to the user home (i.e. beginning with `~`).
    * An absolute path.
* The line must be in the first 512 bytes of the file.
    * This size has been chosen arbitrarily.
    * Since most scripts in that directory will be very small, this is not an issue.
    * It is a good idea to put this line as the first line (or one of the first lines) after the [shebang][].


Credits
-------

The need for this tool started with my girlfriend's laptop.

The code organization was inspired by [indicator-chars](https://github.com/tobyS/indicator-chars), written by [Tobias Schlitt](mailto:toby@php.net).


Further hints and tips
----------------------

Since the files in `~/.screenlayout/*.sh` are just shell scripts, they can do more than calling `xrandr` to setup the monitors. They can also configure PulseAudio to redirect audio to the HDMI port. Try the following commands:

* To set audio output to HDMI: `pacmd set-card-profile 0 output:hdmi-stereo+input:analog-stereo`
* To set audio output to analog speakers: `pacmd set-card-profile 0 output:analog-stereo+input:analog-stereo`
* To see the available cards and profiles in your system: `pacmd list-cads`
* Nice GUI to configure PulseAudio: `pavucontrol`

Read more:

* https://bitbucket.org/denilsonsa/small_scripts/src/default/screenlayout/
* https://wiki.archlinux.org/index.php/PulseAudio/Examples
* http://askubuntu.com/questions/63599/configuring-hdmi-audio-via-command-line
* http://askubuntu.com/questions/14077/how-can-i-change-the-default-audio-device-from-command-line

[shebang]: https://en.wikipedia.org/wiki/Shebang_%28Unix%29
[icon-naming-spec]: http://standards.freedesktop.org/icon-naming-spec/icon-naming-spec-latest.html
