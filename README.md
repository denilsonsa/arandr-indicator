arandr-indicator
================

Quick and simple tray icon menu for changing the monitor layout.


Requirements
------------

* [ARandR](http://christian.amsuess.com/tools/arandr/) (optional!)
* Python 2.x
* [PyGTK](http://www.pygtk.org/)
* [python-appindicator](https://launchpad.net/libappindicator)
* Some kind of UI that supports [Unity indicators](https://unity.ubuntu.com/projects/appindicators/), should work on Gnome, KDE, Unity, LXDE…


How to use
----------

1. Run `arandr-indicator.py`.
2. Add it to autostart, so it runs whenever you login.
3. Run `arandr`.
4. Configure the monitor layout the way you like.
5. Save the layout.
    * ARandR tool will save the layout as a simple one-line shell script that calls `xrandr` with the appropriate commands. The script will be saved in `~/.screenlayout/`.
6. Magic! All layout scripts from that directory will automatically show up in the menu!


Credits
-------

The idea and code organization was inspired by [indicator-chars](https://github.com/tobyS/indicator-chars), written by [Tobias Schlitt](mailto:toby@php.net).
