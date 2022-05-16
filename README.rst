=======================
pulse-bt-profile-toggle
=======================

This simple Python script allows to toggle between Bluetooth audio profiles
from CLI, and can be assigned to a keyboard shortcut.

Uses ``jeepney`` for desktop notification, should work with any DBus-based
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

This application has only few pure-Python dependencies, so it is easy to
install with pip in whatever manner.
My favorite for such kind of programs is ``pipx`` that creates a dedicated
virtualenv to install the application and dependencies, and places the main
program script via ``~/.local/bin`` so it is easy to consume.


configure
=========

To have a keyboard shortcut, go to the
``GNOME Settings -> Devices -> Keyboard`` settings,
scroll down and add a new shortcut under ``Custom Shortcuts``
(I use ``<Super>-B``) pointing to ``pulse-bt-profile-toggle`` script
(system, userspace, or in the virtualenv)::

    which pulse-bt-profile-toggle
