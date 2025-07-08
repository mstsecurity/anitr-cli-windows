import os
import time
from dotenv import load_dotenv
import modules.utils as utils

_user_home = os.path.expanduser("~")
_anitr_config_dir = os.path.join(_user_home, ".anitr-cli")
_config_file_path = os.path.join(_anitr_config_dir, "config")

if not os.path.exists(_anitr_config_dir):
    os.makedirs(_anitr_config_dir, exist_ok=True)

load_dotenv(_config_file_path)

discord_rpc = utils.get_env("discord_rpc", "DISCORD_RPC", default="enabled")
save_position_on_quit = utils.get_bool_env(
    "save_position_on_quit", "SAVE_POSITION_ON_QUIT", default="false")

default_ui = "tui"

sources = ["AnimeciX (animecix.tv)", "OpenAnime (openani.me)"]

discord_client_id = "1383421771159572600"
rpc = None
rpc_initialized = False
start_time = int(time.time())

_temp_dir = os.environ.get('TEMP') or os.environ.get('TMP')
if not _temp_dir:
    _temp_dir = os.path.join(_user_home, "anitr_temp")
    if not os.path.exists(_temp_dir):
        os.makedirs(_temp_dir, exist_ok=True)

anime_details = os.path.join(_temp_dir, "anime_details.json")
error_log = os.path.join(_temp_dir, "anitr-cli-error.log")
config_path = _config_file_path

github_repo = "https://github.com/mstsecurity/anitr-cli-windows"

GITHUB_REPO = "mstsecurity/anitr-cli-windows"

CURRENT_VERSION = "3.6.0-2"
