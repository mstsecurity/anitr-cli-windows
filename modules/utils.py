import subprocess
from datetime import datetime
from . import config

def log_error(path, error):
    with open(path, "a", encoding="utf-8") as e:
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        e.write(f"{timestamp} {error}\n")

def send_notification(title, message, urgency="normal", icon = None):
    if not icon:
        subprocess.run(['notify-send', '-u', urgency, '-a', title, message])
    else:
        subprocess.run(['notify-send', '-u', urgency, '-a', title, message, "--icon", icon])

def smart_print(text: str, notification_msg: str, notification: bool = True, icon = None):
    if config.default_ui == "rofi":
        if notification:
            send_notification("anitr-cli", notification_msg, "normal", icon)
    else:
        print(text)

def get_source(ui):
    return ui.select_menu(config.default_ui, config.sources, "Kaynak seç:", False)
