#!/usr/bin/python3
from jeepney import DBusAddress, new_method_call
from jeepney.io.blocking import open_dbus_connection
import pulsectl

APP_NAME = "Bluetooth audio profile toggle"


def get_icon_for_profile(profile):
    if "head" in profile.lower():
        return "audio-headset-symbolic"
    elif 'a2dp' in profile.lower():
        return "audio-headphones-symbolic"


def send_notification(text, info='', icon="dialog-info"):
    notifications = DBusAddress('/org/freedesktop/Notifications',
                                bus_name='org.freedesktop.Notifications',
                                interface='org.freedesktop.Notifications')
    connection = open_dbus_connection(bus='SESSION')
    # Construct a new D-Bus message. new_method_call takes the address, the
    # method name, the signature string, and a tuple of arguments.
    msg = new_method_call(
        notifications, 'Notify', r'susssasa{sv}i',
        (
            APP_NAME,  # App name
            0,  # Not replacing any previous notification
            icon or '',  # Icon
            text,  # Summary
            info,  # more info (optional)
            [],  # Actions
            {"transient": ("b", True), "category": ("s", "device")},  # Hints
            -1,      # expire_timeout (-1 = default)
        )
    )
    # Not actually interested in reply
    connection.send_and_get_reply(msg)
    connection.close()


def toggle():
    pulse = pulsectl.Pulse(APP_NAME)
    btcards = list(c for c in pulse.card_list() if "bluez" in c.name)
    if not btcards:
        send_notification("No active Bluetooth audio found",
                          icon="dialog-error")
        return
    elif len(btcards) > 1:
        send_notification("Multiple Bluetooth audios is not supported yet")
        return
    btcard = btcards[0]
    toggle_to = list(
        p for p in btcard.profile_list if (
            p.name not in ("off", btcard.profile_active.name)))
    if not toggle_to:
        send_notification("No alternarive Bluetooth audio profile found",
                          icon="dialog-error")
        return
    elif len(toggle_to) > 1:
        send_notification(
            "Multiple alternative Bluetooth profiles not supported"
        )
        return
    pulse.card_profile_set(btcard, toggle_to[0].name)
    active_profile = btcard.profile_active.name
    send_notification(
        f"Using {active_profile.upper()} Bluetooth audio profile",
        icon=get_icon_for_profile(active_profile)
    )


if __name__ == "__main__":
    toggle()
