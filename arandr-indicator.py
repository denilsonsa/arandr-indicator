#!/usr/bin/env python3
#
# Simple arandr menu for changing the monitor layout.
# See README for detailed information.
#
# Code based on indicator-chars by Tobias Schlitt <toby@php.net>.
# https://github.com/tobyS/indicator-chars
#
#
# BSD-2-Clause
#
# Copyright (c) 2014, Denilson Sá
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
# DAMAGE.

# GTK / GLib / GObject Introspection
# https://wiki.gnome.org/Projects/GObjectIntrospection
# https://gi.readthedocs.io/
# https://pygobject.readthedocs.io/
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Gio", "2.0")
from gi.repository import Gtk as gtk
from gi.repository import Gio as gio

# Try one of the two supported libraries:
try:
    gi.require_version("AppIndicator3", "0.1")
    from gi.repository import AppIndicator3 as appindicator
except (ImportError, ValueError):
    gi.require_version("AyatanaAppIndicator3", "0.1")
    from gi.repository import AyatanaAppIndicator3 as appindicator

# Optional dependency: PyXDG
# https://freedesktop.org/wiki/Software/pyxdg/
# https://cgit.freedesktop.org/xdg/pyxdg/
# https://gitlab.freedesktop.org/xdg/pyxdg
# https://github.com/takluyver/pyxdg
try:
    import xdg
    import xdg.BaseDirectory
    import xdg.DesktopEntry
except ImportError:
    xdg = None

# Built-in Python modules:
import glob
import os
import os.path
import re
import signal
import subprocess


class ARandRIndicator:
    LAYOUTS_PATH = os.path.expanduser("~/.screenlayout")
    LAYOUTS_GLOB = os.path.join(LAYOUTS_PATH, "*.sh")
    SELF_PATH = os.path.abspath(__file__)
    MAIN_ICON = "video-display"
    ARANDR_ICON = "preferences-desktop-display"
    LAYOUT_ICON_RE = re.compile(r'META:ICON[ \t]*=[ \t]*"(?P<iconname>[^"]*)"', re.I)

    def __init__(self):
        self.indicator = appindicator.Indicator.new(
            "ARandR", self.MAIN_ICON, appindicator.IndicatorCategory.HARDWARE
        )
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)

        self.update_menu()

    def run_and_forget(self, args, **kwargs):
        """Runs a new process in the background and forgets about it."""
        subprocess.Popen(args, shell=False, close_fds=True, **kwargs)

    def am_i_in_autostart(self):
        """Checks if this tool is currently configured in the XDG autostart directory.

        This check isn't fool-proof, it won't detect some edge cases, but it
        should work well enough for most scenarios.
        """
        try:
            filename = xdg.BaseDirectory.load_first_config(
                "autostart/arandr-indicator.desktop"
            )
            if not filename:
                return False

            entry = xdg.DesktopEntry.DesktopEntry()
            entry.parse(filename)
            return entry.get("Exec") == self.SELF_PATH
        except:
            return False

    def create_autostart_desktop_file(self):
        """As the function name says, it creates an autostart desktop file.

        This function will setup this tool to be autostarted on most desktop
        environments. It greatly simplifies the onboarding of new users.
        """
        path = xdg.BaseDirectory.save_config_path("autostart")
        filename = os.path.join(path, "arandr-indicator.desktop")
        entry = xdg.DesktopEntry.DesktopEntry()
        entry.new(filename)
        entry.set("Name", "ARandR Indicator")
        entry.set("GenericName", "Display layout quick menu")
        entry.set("Comment", "Quickly change between monitor layouts")
        entry.set("Exec", self.SELF_PATH)
        entry.set("Icon", self.MAIN_ICON)
        entry.set("Terminal", "false")
        entry.set("StartupNotify", "false")
        entry.set("Categories", "Settings;HardwareSettings;")
        entry.set("Type", "Application")
        entry.write()

    def get_layouts(self):
        """Returns a sorted list of the available layout script files.

        Returns a list of a tuple of (full filename, basename, pretty name).
        """
        arr = []
        for pathname in glob.glob(self.LAYOUTS_GLOB):
            basename = os.path.basename(pathname)
            pretty_name = re.sub(r"\.sh$", "", basename).replace("_", " ")
            arr.append((pathname, basename, pretty_name))

        return sorted(arr, key=lambda x: (x[2], x[0]))

    def get_icon_name_from_layout_file(self, filename):
        """Given a layout script file, reads its metadata to find an optional
        icon image filename.
        """
        with open(filename, "r", encoding="utf8") as f:
            head = f.read(512)  # First 512 bytes of the file.
        for line in head.split("\n"):  # Splitting into lines.
            match = self.LAYOUT_ICON_RE.search(line.strip())
            if match:
                return match.group("iconname")

        return None

    def update_menu(self, widget=None, data=None):
        menu = gtk.Menu()
        self.indicator.set_menu(menu)

        for (pathname, basename, pretty_name) in self.get_layouts():
            icon_name = self.get_icon_name_from_layout_file(pathname)
            icon = None

            if icon_name:
                if "." in icon_name:
                    icon_path = os.path.join(
                        self.LAYOUTS_PATH, os.path.expanduser(icon_name)
                    )
                    icon = gtk.Image.new_from_file(icon_path)
                else:
                    icon = gtk.Image.new_from_icon_name(icon_name, gtk.IconSize.MENU)

            if icon:
                item = gtk.ImageMenuItem()
                item.set_image(icon)
            else:
                item = gtk.MenuItem()

            item.set_label(pretty_name)
            item.connect("activate", self.on_item_click, pathname)
            menu.append(item)

        menu.append(gtk.SeparatorMenuItem())

        arandr_item = gtk.ImageMenuItem()
        arandr_item.set_label("Launch ARandR")
        arandr_item.set_image(
            gtk.Image.new_from_icon_name(self.ARANDR_ICON, gtk.IconSize.MENU)
        )
        arandr_item.connect("activate", self.on_launch_arandr)
        menu.append(arandr_item)

        if xdg and not self.am_i_in_autostart():
            autostart_item = gtk.MenuItem()
            autostart_item.set_label("Write autostart file")
            autostart_item.connect("activate", self.on_create_autostart)
            menu.append(autostart_item)

        quit_item = gtk.ImageMenuItem(label=gtk.STOCK_QUIT)
        quit_item.set_use_stock(True)
        quit_item.connect("activate", self.on_quit)
        menu.append(quit_item)

        menu.show_all()

    def on_directory_changed(self, filemonitor, file, other_file, event_type):
        if event_type in [
            gio.FileMonitorEvent.CHANGES_DONE_HINT,
            gio.FileMonitorEvent.DELETED,
        ]:
            self.update_menu()

    def on_item_click(self, widget, name):
        if os.access(name, os.X_OK):
            # If executable, run it directly.
            args = [name]
        else:
            # Otherwise, run it through sh.
            args = ["/bin/sh", name]

        self.run_and_forget(args, cwd=os.path.dirname(name))

    def on_create_autostart(self, widget):
        self.create_autostart_desktop_file()
        self.update_menu()

    def on_launch_arandr(self, widget):
        self.run_and_forget(["arandr"], cwd=self.LAYOUTS_PATH)

    def on_quit(self, widget):
        gtk.main_quit()


if __name__ == "__main__":
    # Catch CTRL-C.
    signal.signal(signal.SIGINT, lambda signal, frame: gtk.main_quit())

    # Run the app.
    app = ARandRIndicator()

    # Monitor ~/.screenlayout/ changes
    file = gio.File.new_for_path(app.LAYOUTS_PATH)
    monitor = file.monitor_directory(gio.FileMonitorFlags.NONE, None)
    monitor.connect("changed", app.on_directory_changed)

    # Main gtk loop
    gtk.main()
