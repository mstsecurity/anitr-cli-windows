from packaging import version
import requests
import os
import shutil
import subprocess
import sys
from . import config
from . import utils

def get_latest_version():
    url = f"https://api.github.com/repos/{config.GITHUB_REPO}/releases/latest"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        tag = response.json()["tag_name"]
        return tag.lstrip("v")
    except requests.exceptions.RequestException as e:
        utils.log_error(config.error_log, f"GitHub API'ye bağlanırken hata: {e}")
        utils.show_notification("anitr-cli", "Güncelleme kontrolü başarısız oldu: Ağ hatası.", "critical")
        return config.CURRENT_VERSION

def download_and_replace_binary():
    print("📦 Güncelleme başlatılıyor...")

    install_dir = os.path.join(os.getenv("LOCALAPPDATA"), "Programs", "anitr-cli")
    os.makedirs(install_dir, exist_ok=True)
    exe_path = os.path.join(install_dir, "anitr-cli.exe")

    latest = get_latest_version()
    download_url = f"https://github.com/{config.GITHUB_REPO}/releases/download/v{latest}/anitr-cli.exe"

    try:
        print(f"{download_url} adresinden indiriliyor...")
        response = requests.get(download_url, timeout=15)
        response.raise_for_status()

        with open(exe_path, "wb") as f:
            f.write(response.content)

        print(f"\033[32mYeni sürüm {exe_path} konumuna yüklendi.\033[0m")

        # PATH içinde mi kontrolü
        path_env = os.environ.get("PATH", "")
        if install_dir.lower() not in [p.strip().lower() for p in path_env.split(";")]:
            print(f"\033[93mUyarı: {install_dir} dizini PATH ortam değişkeninde bulunmuyor.\033[0m")
            print("anitr-cli komutunu doğrudan kullanmak için bu dizini PATH'e ekleyin.")
            utils.show_notification("anitr-cli", "Yükleme başarılı ancak PATH'e ekli değil.", "normal")
        else:
            print("\033[32manitr-cli komutu artık doğrudan kullanılabilir.\033[0m")
            utils.show_notification("anitr-cli", "Güncelleme tamamlandı.", "normal")

    except requests.exceptions.RequestException as e:
        print(f"\033[91mİndirme hatası: {e}\033[0m")
        utils.log_error(config.error_log, f"Güncelleme indirilemedi: {e}")
        utils.show_notification("anitr-cli", "Güncelleme indirilemedi.", "critical")

def check_update_notice():
    try:
        latest = get_latest_version()
        if version.parse(latest) > version.parse(config.CURRENT_VERSION):
            notice = f"Yeni bir anitr-cli sürümü mevcut: \033[31mv{config.CURRENT_VERSION}\033[0m → \033[32mv{latest}\033[0m\n" \
                     f"Güncellemek için şunu çalıştırın: anitr-cli --update"
            return notice
    except Exception as e:
        utils.log_error(config.error_log, f"Güncelleme bildirimi kontrol edilirken hata: {e}")
        pass
    return None
