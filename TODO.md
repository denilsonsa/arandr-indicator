Update README with the new 3.x stuff

Make a note about deprecated image menu item: https://stackoverflow.com/a/48473708
 Maybe even this: https://stackoverflow.com/questions/35661101/gtkmenuitem-empty-space-on-the-sides
Or this (but first check license): https://github.com/DLR-RM/RAFCON/blob/07c38ea01f89d5983f4811dd41660b8ff43116c1/source/rafcon/gui/helpers/label.py#L213-L228

Figure out what are the exact package name dependencies (on both arch linux and debian/ubuntu). This gets trickier because of GTK.

There are so many GTK bindings for Python! https://en.wikipedia.org/wiki/List_of_language_bindings_for_GTK

Be aware: PyXDG ≠ xdg

https://docs.gtk.org/gtk3/class.ImageMenuItem.html


https://packages.debian.org/stretch/gir1.2-appindicator3-0.1
https://askubuntu.com/questions/772064/python-3-appindicator3-what-is-the-dependency


https://lazka.github.io/pgi-docs/Gio-2.0/classes/File.html#Gio.File.new_for_path


Also move the LICENSE to somewhere else. Or just copy it.
