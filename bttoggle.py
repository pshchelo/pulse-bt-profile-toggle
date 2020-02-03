#!/usr/bin/python3
import logging

import gi
from gi.repository import GObject
gi.require_version('Notify', '0.7')
from gi.repository import Notify # noqa
import pulsectl # noqa

APP_NAME = "BT profile toggle"
LOG = logging.getLogger(APP_NAME)


class BtProfileToggle(GObject.Object):
    def __init__(self):
        super().__init__()
        # lets initialise with the application name
        Notify.init(APP_NAME)
        self.pulse = pulsectl.Pulse(APP_NAME)

    def _send_notification(self, text, file_path_to_icon=""):

        n = Notify.Notification.new(APP_NAME, text, file_path_to_icon)
        n.set_timeout(Notify.EXPIRES_DEFAULT)
        n.show()

    def bt_toggle(self):
        btcards = list(c for c in self.pulse.card_list() if "bluez" in c.name)
        if not btcards:
            self._send_notification("No active BT card found")
            return
        elif len(btcards) > 1:
            self._send_notification("Multiple BT cards is not supported yet")
            return
        btcard = btcards[0]
        toggle_to = list(
            p for p in btcard.profile_list if (
                p.name not in ('off', btcard.profile_active.name)))
        if not toggle_to:
            self._send_notification("No profile to toggle to found")
            return
        elif len(toggle_to) > 1:
            self._send_notification(
                "Multiple alternative BT profiles not supported")
            return
        self.pulse.card_profile_set(btcard, toggle_to[0].name)
        LOG.info(btcard.profile_active.name)
        self._send_notification(
            f"Set BT profile: {btcard.profile_active.name}")


if __name__ == "__main__":
    toggler = BtProfileToggle()
    toggler.bt_toggle()
