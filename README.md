arandr-indicator
================

Quick and simple tray icon menu for changing the monitor layout. A great companion to ARandR tool.

[![YouTube demonstration](http://img.youtube.com/vi/xqpF6RrYUmo/0.jpg)](http://youtu.be/xqpF6RrYUmo)


Requirements
------------

* [ARandR](http://christian.amsuess.com/tools/arandr/) (optional!)
* Python 2.x
* [PyGTK](http://www.pygtk.org/)
* [python-appindicator](https://launchpad.net/libappindicator)
* [PyXDG](http://freedesktop.org/wiki/Software/pyxdg/)
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

1. `sudo apt-get install python-appindicator python-gtk2 python-xfd arandr`
2. Download `arandr-indicator.py` and save it anywhere.
3. `chmod +x arandr-indicator.py` to make it executable.
4. `./arandr-indicator.py` to execute it.
5. Add it to autostart, so it runs whenever you login.


Credits
-------

The need for this tool started with my girlfriend.

The code organization was inspired by [indicator-chars](https://github.com/tobyS/indicator-chars), written by [Tobias Schlitt](mailto:toby@php.net).
