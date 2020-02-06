#!/usr/bin/python3
import notify2
import pulsectl

APP_NAME = "Bluetooth audio profile toggle"


def get_icon_for_profile(profile):
    if "head" in profile.lower():
        return "audio-headset-symbolic"
    elif 'a2dp' in profile.lower():
        return "audio-headphones-symbolic"


def send_notification(text, icon="dialog-info"):
    notify2.init(APP_NAME)
    n = notify2.Notification(text, icon=icon)
    n.timeout = notify2.EXPIRES_DEFAULT
    n.hints["transient"] = True
    n.hints["category"] = "device"
    n.show()


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
