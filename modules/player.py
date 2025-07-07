# modules/player.py

import subprocess
import time
import platform
import shutil
from . import config, utils


def open_with_video_player(url, subtitle_url=None, save_position_on_quit=False):
    """Video Oynatıcı"""

    try:
        # PATH'te mpv var mı kontrol et
        mpv_path = shutil.which("mpv")
        if not mpv_path:
            raise FileNotFoundError(
                "mpv bulunamadı. Lütfen mpv'yi sisteminize yükleyin ve PATH'e ekleyin."
            )

        cmd = [
            mpv_path,
            '--fullscreen',
            '--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/137.0.0.0 Safari/537.36',
            '--referrer=https://yeshi.eu.org/'
        ]

        if save_position_on_quit:
            cmd += ['--save-position-on-quit']

        if subtitle_url:
            cmd += ['--sub-file=' + subtitle_url]

        cmd.append(url)

        # Windows'ta terminal açılmasın
        creation_flags = subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0

        subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=creation_flags
        )

    except FileNotFoundError as e:
        utils.send_notification(
            "anitr-cli",
            "mpv bulunamadı. Lütfen mpv'yi yükleyin ve sistem PATH'ine ekleyin.",
            "critical"
        )
        utils.log_error(config.log_error, str(e))
        time.sleep(10)

    except subprocess.CalledProcessError as e:
        utils.send_notification(
            "anitr-cli",
            f"anitr-cli bir hatayla karşılaştı. Hata detayları: {config.error_log}",
            "critical"
        )
        utils.log_error(config.log_error, e)
        time.sleep(10)
