#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Simple arandr menu for changing the monitor layout.
# See README for detailed information.
#
# Code based on indicator-chars by Tobias Schlitt <toby@php.net>.
#
#
# Copyright (c) 2014, Denilson Sá
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.  Redistributions
# in binary form must reproduce the above copyright notice, this list of
# conditions and the following disclaimer in the documentation and/or
# other materials provided with the distribution.
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

import appindicator
import gio
import glob
import gtk
import os
import os.path
import re
import signal
import subprocess

try:
    import xdg
    import xdg.BaseDirectory
    import xdg.DesktopEntry
except ImportError:
    xdg = None


def run_and_forget(args, **kwargs):
    subprocess.Popen(args, shell=False, close_fds=True, **kwargs)


class ARandRIndicator:
    LAYOUTS_PATH = os.path.expanduser('~/.screenlayout')
    LAYOUTS_GLOB = os.path.join(LAYOUTS_PATH, '*.sh')
    SELF_PATH = os.path.abspath(__file__)
    MAIN_ICON = 'video-display'
    ARANDR_ICON = 'preferences-desktop-display'
    LAYOUT_ICON_RE = re.compile(br'META:ICON[ \t]*=[ \t]*"(?P<iconname>[^"]*)"', re.I)

    def __init__(self):
        self.indicator = appindicator.Indicator(
            'ARandR', self.MAIN_ICON, appindicator.CATEGORY_HARDWARE)
        self.indicator.set_status(appindicator.STATUS_ACTIVE)

        self.update_menu()

    def am_i_in_autostart(self):
        try:
            filename= xdg.BaseDirectory.load_first_config(
                'autostart/arandr-indicator.desktop')
            if not filename:
                return False

            entry = xdg.DesktopEntry.DesktopEntry()
            entry.parse(filename)
            return entry.get('Exec') == self.SELF_PATH
        except:
            return False

    def create_autostart_desktop_file(self):
        path = xdg.BaseDirectory.save_config_path('autostart')
        filename = os.path.join(path, 'arandr-indicator.desktop')
        entry = xdg.DesktopEntry.DesktopEntry()
        entry.new(filename)
        entry.set('Name', 'ARandR Indicator')
        entry.set('GenericName', 'Display layout quick menu')
        entry.set('Comment', 'Quickly change between monitor layouts')
        entry.set('Exec', self.SELF_PATH)
        entry.set('Icon', self.MAIN_ICON)
        entry.set('Terminal', 'false')
        entry.set('StartupNotify', 'false')
        entry.set('Categories', 'Settings;HardwareSettings;')
        entry.set('Type', 'Application')
        entry.write()

    def get_layouts(self):
        return sorted(glob.glob(self.LAYOUTS_GLOB))

    def get_icon_name_from_layout_file(self, filename):
        with open(filename, 'rb') as f:
            head = f.read(512)  # First 512 bytes of the file.
        for line in head.split('\n'):  # Splitting into lines.
            line = line.strip(' \t\n\r')  # Stripping whitespace.
            match = self.LAYOUT_ICON_RE.search(line)
            if match:
                return match.group('iconname')

        return None

    def update_menu(self, widget=None, data=None):
        menu = gtk.Menu()
        self.indicator.set_menu(menu)

        for name in self.get_layouts():
            basename = os.path.basename(name)
            pretty_name = re.sub(r'\.sh$', '', basename).replace('_', ' ')
            icon_name = self.get_icon_name_from_layout_file(name)
            icon = None

            if icon_name:
                if '.' in icon_name:
                    icon_path = os.path.join(self.LAYOUTS_PATH, os.path.expanduser(icon_name))
                    icon = gtk.image_new_from_file(icon_path)
                else:
                    icon = gtk.image_new_from_icon_name(icon_name, gtk.ICON_SIZE_MENU)

            if icon:
                item = gtk.ImageMenuItem()
                item.set_image(icon)
            else:
                item = gtk.MenuItem()

            item.set_label(pretty_name)
            item.connect('activate', self.on_item_click, name)
            menu.append(item)

        menu.append(gtk.SeparatorMenuItem())

        arandr_item = gtk.ImageMenuItem()
        arandr_item.set_label('Launch ARandR')
        arandr_item.set_image(
            gtk.image_new_from_stock(self.ARANDR_ICON, gtk.ICON_SIZE_MENU))
        arandr_item.connect('activate', self.on_launch_arandr)
        menu.append(arandr_item)

        if xdg and not self.am_i_in_autostart():
            autostart_item = gtk.MenuItem()
            autostart_item.set_label('Write autostart file')
            autostart_item.connect('activate', self.on_create_autostart)
            menu.append(autostart_item)

        # quit_item = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        # quit_item.connect('activate', self.on_quit)
        # menu.append(quit_item)

        menu.show_all()

    def on_directory_changed(self, filemonitor, file, other_file, event_type):
        if event_type in [
                gio.FILE_MONITOR_EVENT_CHANGES_DONE_HINT,
                gio.FILE_MONITOR_EVENT_DELETED
        ]:
            self.update_menu()

    def on_item_click(self, widget, name):
        if os.access(name, os.X_OK):
            # If executable, run it directly.
            args = [name]
        else:
            # Otherwise, run it through sh.
            args = ['/bin/sh', name]

        run_and_forget(args, cwd=os.path.dirname(name))

    def on_create_autostart(self, widget):
        self.create_autostart_desktop_file()
        self.update_menu()

    def on_launch_arandr(self, widget):
        run_and_forget(['arandr'], cwd=self.LAYOUTS_PATH)

    def on_quit(self, widget):
        gtk.main_quit()


if __name__ == '__main__':
    # Catch CTRL-C.
    signal.signal(signal.SIGINT, lambda signal, frame: gtk.main_quit())

    # Run the app.
    app = ARandRIndicator()

    # Monitor ~/.screenlayout/ changes
    file = gio.File(app.LAYOUTS_PATH)
    monitor = file.monitor_directory()
    monitor.connect('changed', app.on_directory_changed)

    # Main gtk loop
    gtk.main()
