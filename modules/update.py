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
    
    app_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    
    if shutil.which("git") is None:
        utils.show_notification("anitr-cli", "Git kurulu değil. Lütfen Git'i kurduğunuzdan emin olun.", "critical")
        print("\033[91mHata: Git kurulu değil. Lütfen Git'i kurun ve PATH'inize ekleyin.\033[0m")
        return

    try:
        os.chdir(app_dir)
        print(f"Güncelleme için dizin: {os.getcwd()}")

        print("Git pull çekiliyor...")
        pull_result = subprocess.run(["git", "pull"], capture_output=True, text=True, check=True)
        print(pull_result.stdout)
        if pull_result.stderr:
            print(f"\033[93mGit uyarısı: {pull_result.stderr}\033[0m")

        if "Already up to date" not in pull_result.stdout and "Fast-forward" in pull_result.stdout:
            print("Uygulama güncellendi. Bağımlılıklar kontrol ediliyor...")
            if os.path.exists("requirements.txt"):
                try:
                    pip_install_cmd = [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
                    print(f"Bağımlılıklar güncelleniyor: {' '.join(pip_install_cmd)}")
                    pip_result = subprocess.run(pip_install_cmd, capture_output=True, text=True, check=True)
                    print(pip_result.stdout)
                    if pip_result.stderr:
                        print(f"\033[93mPip uyarısı: {pip_result.stderr}\033[0m")
                    print("Bağımlılıklar güncellendi.")
                except subprocess.CalledProcessError as e:
                    utils.log_error(config.error_log, f"Bağımlılıklar güncellenirken hata: {e.stderr}")
                    utils.show_notification("anitr-cli", "Bağımlılıklar güncellenirken hata oluştu.", "critical")
                    print(f"\033[91mHata: Bağımlılıklar güncellenirken hata oluştu: {e.stderr}\033[0m")
            else:
                print("requirements.txt bulunamadı, bağımlılıklar güncellenmedi.")
            
            utils.show_notification("anitr-cli", "Uygulama başarıyla güncellendi!", "normal")
            print("\033[32mUygulama başarıyla güncellendi! Lütfen uygulamayı yeniden başlatın.\033[0m")
        else:
            print("Uygulama zaten en güncel sürümde.")
            utils.show_notification("anitr-cli", "Uygulama zaten en güncel sürümde.", "normal")

    except subprocess.CalledProcessError as e:
        utils.log_error(config.error_log, f"Güncelleme hatası: {e.stderr}")
        utils.show_notification("anitr-cli", f"Güncelleme başarısız oldu: {e.stderr.strip()}", "critical")
        print(f"\033[91mGüncelleme hatası: {e.stderr}\033[0m")
    except Exception as e:
        utils.log_error(config.error_log, f"Beklenmedik güncelleme hatası: {e}")
        utils.show_notification("anitr-cli", f"Beklenmedik güncelleme hatası: {e}", "critical")
        print(f"\033[91mBeklenmedik bir hata oluştu: {e}\033[0m")

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
