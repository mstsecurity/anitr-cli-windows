import subprocess
from datetime import datetime
import os
import sys
try:
    from win10toast import ToastNotifier
    _toaster = ToastNotifier()
    _WINDOWS_NOTIFICATIONS_AVAILABLE = True
except ImportError:
    _WINDOWS_NOTIFICATIONS_AVAILABLE = False


def get_env(*keys, default=None):
    for key in keys:
        val = os.getenv(key)
        if val is not None:
            return val.strip()
    return default

def get_bool_env(*keys, default="false"):
    val = get_env(*keys, default=default)
    return val.lower() in ("1", "true", "yes", "on")

def log_error(path, error):
    error_str = str(error)
    with open(path, "a", encoding="utf-8") as e:
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        e.write(f"{timestamp} {error_str}\n")

def show_notification(title, message, urgency="normal", icon=None):
    if sys.platform.startswith('win') and _WINDOWS_NOTIFICATIONS_AVAILABLE:
        _toaster.show_toast(title, message, duration=5)
    else:
        print(f"Bildirim: {title} - {message}")

def smart_print(text: str, notification_msg: str, notification: bool = True, icon=None):
    if notification:
        show_notification("anitr-cli", notification_msg, "normal", icon=icon)
    print(text)

def get_source(ui_module):
    return ui_module.select_menu("tui", config.sources, "Kaynak seç:", False)
