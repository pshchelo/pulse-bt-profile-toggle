=======================
pulse-bt-profile-toggle
=======================

This simple Python script allows to toggle between Bluetooth audio profiles
from CLI, and can be assigned to a keyboard shortcut.

Uses ``notify2`` for desktop notification, should work with any DBus-based
desktop notification implementation.
Notification icons are default available in Adwaita GNOME shell theme,
if missing they will just be omitted.

why
===
My Ubuntu does not support multi-profile Bluetooth connect or switching
automatically between HeadSet and A2DP audio profiles when application may
warrant this.
When in need to switch from listening music to conference call one has to
manually go to sound settings and change the profile - which is inconvenient.

install
=======

Easiest way I've found is to install dependencies into the user space::

    pip3 install --user .

because the required dbus-python is probably already installed in the system
(it seems to be a dependency for many things like networkd).

If not, or when installing into a virtualenv, you will need to install it via::

    pip3 install --user .[dbus]

but that requires libdbus headers package and all the usual suspects
for compiling Python C-extensions (see ``bindep.txt``,
list may be not complete, and only tested on my local Ubuntu 18.04 desktop).

See the TODO item to how that inconvenience might be solved
in the future.


configure
=========

To have a keyboard shortcut, go to the
``GNOME Settings -> Devices -> Keyboard`` settings,
scroll down and add a new shortcut under ``Custom Shortcuts``
(I use ``<Super>-B``) pointing to ``pulse-bt-profile-toggle`` script
(system, userspace, or in the virtualenv)::

    which pulse-bt-profile-toggle


TODO
====

#. Rewrite with ``Jeepney`` as pure Python DBus interface
   to avoid necessity of building any C extensions.
