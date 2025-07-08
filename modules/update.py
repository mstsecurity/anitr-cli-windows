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
        utils.log_error(config.error_log,
                        f"GitHub API'ye bağlanırken hata: {e}")
        utils.show_notification(
            "anitr-cli", "Güncelleme kontrolü başarısız oldu: Ağ hatası.", "critical")
        return config.CURRENT_VERSION


def download_and_replace_binary():
    print("📦 Güncelleme başlatılıyor...")

    install_dir = os.path.join(
        os.getenv("LOCALAPPDATA"), "Programs", "anitr-cli-windows")
    bin_dir = os.path.join(os.getenv("LOCALAPPDATA"), "Programs", "bin")
    zip_path = os.path.join(os.getenv("TEMP"), "anitr-cli.zip")
    bat_filename = "anitr-cli.bat"
    bat_source = os.path.join(install_dir, bat_filename)
    bat_dest = os.path.join(bin_dir, bat_filename)

    latest = get_latest_version()
    download_url = f"https://github.com/{
        config.GITHUB_REPO}/archive/refs/tags/v{latest}.zip"

    try:
        print(f"{download_url} adresinden indiriliyor...")
        response = requests.get(download_url, timeout=15)
        response.raise_for_status()

        # ZIP dosyasını geçici dizine yaz
        with open(zip_path, "wb") as f:
            f.write(response.content)

        # Mevcut kurulu klasörü sil (önceki dosyaları temizlemek için)
        if os.path.exists(install_dir):
            shutil.rmtree(install_dir)

        # Zip'i aç
        shutil.unpack_archive(zip_path, install_dir)

        # GitHub ZIP içindeki alt klasörü bul (örnek: anitr-cli-0.1.2)
        extracted_root = next((os.path.join(install_dir, d) for d in os.listdir(install_dir)
                              if os.path.isdir(os.path.join(install_dir, d))), None)

        if not extracted_root:
            raise Exception("ZIP içeriği beklenmedik şekilde eksik.")

        # İçeriği doğrudan install_dir'e taşı
        for item in os.listdir(extracted_root):
            s = os.path.join(extracted_root, item)
            d = os.path.join(install_dir, item)
            shutil.move(s, d)

        shutil.rmtree(extracted_root)

        # bin klasörünü oluştur
        os.makedirs(bin_dir, exist_ok=True)

        # .bat dosyasını hedefe taşı
        if os.path.exists(bat_source):
            shutil.copy2(bat_source, bat_dest)
            print(f"\033[32m{bat_filename} başarıyla {
                  bat_dest} konumuna kopyalandı.\033[0m")
        else:
            print(
                f"\033[91m{bat_filename} bulunamadı. Lütfen elle kontrol edin.\033[0m")

        # PATH kontrolü
        path_env = os.environ.get("PATH", "")
        if bin_dir.lower() not in [p.strip().lower() for p in path_env.split(";")]:
            print(f"\033[93mUyarı: {bin_dir} dizini PATH içinde değil.\033[0m")
            print("anitr-cli komutunu çalıştırmak için bu dizini PATH'e ekleyin.")
            utils.show_notification(
                "anitr-cli", "Kurulum başarılı ama PATH'e ekli değil.", "normal")
        else:
            print(
                "\033[32manitr-cli komutu artık doğrudan kullanılabilir.\033[0m")
            utils.show_notification(
                "anitr-cli", "Güncelleme tamamlandı.", "normal")

    except Exception as e:
        print(f"\033[91mKurulum hatası: {e}\033[0m")
        utils.log_error(config.error_log, f"Güncelleme indirilemedi: {e}")
        utils.show_notification(
            "anitr-cli", "Kurulum başarısız oldu.", "critical")


def check_update_notice():
    try:
        latest = get_latest_version()
        if version.parse(latest) > version.parse(config.CURRENT_VERSION):
            notice = f"Yeni bir anitr-cli sürümü mevcut: \033[31mv{config.CURRENT_VERSION}\033[0m → \033[32mv{latest}\033[0m\n" \
                f"Güncellemek için şunu çalıştırın: anitr-cli --update"
            return notice
    except Exception as e:
        utils.log_error(config.error_log,
                        f"Güncelleme bildirimi kontrol edilirken hata: {e}")
        pass
    return None
