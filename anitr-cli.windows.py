#!/usr/bin/env python3

from modules.fetch import animecix, openanime
import modules.player as player
import modules.ui as ui
import modules.utils as utils
import modules.config as config
import modules.discord_rpc as rpc
import argparse
import sys
import re
import requests
import os
from packaging import version


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="💫 Terminalden anime izlemek için CLI aracı.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "--source",
        choices=["AnimeciX",
                 "OpenAnime"],
        type=str,
        help="Hangi kaynak ile anime izlemek istediğinizi belirtir."
    )

    parser.add_argument(
        "--disable-rpc",
        action="store_true",
        help="Discord Rich Presence özelliğini devre dışı bırakır."
    )

    parser.add_argument(
        "--update",
        action="store_true",
        help="anitr-cli aracını en son sürüme günceller."
    )

    return parser.parse_args()


def is_valid_image_url(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=3)
        content_type = response.headers.get("Content-Type", "")
        return response.status_code == 200 and "image" in content_type
    except requests.RequestException:
        return False


def save_image_from_url(url, selected_anime_name):
    if not is_valid_image_url(url):
        return None

    safe_name = selected_anime_name.lower().replace(" ", "-")

    try:
        _, ext = os.path.splitext(url)
    except Exception as e:
        utils.log_error(config.error_log, e)
        return None

    temp_dir = os.environ.get('TEMP') or os.environ.get('TMP')
    if not temp_dir:
        temp_dir = os.path.join(os.path.expanduser("~"), "anitr_temp")

    if not os.path.exists(temp_dir):
        try:
            os.makedirs(temp_dir)
        except OSError as e:
            utils.log_error(config.error_log,
                            f"Geçici dizin oluşturulurken hata: {e}")
            return None

    file_path = os.path.join(temp_dir, f"{safe_name}{ext}")

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        with open(file_path, "wb") as f:
            f.write(response.content)

        return file_path
    except requests.RequestException as e:
        utils.log_error(config.error_log, f"Resim indirilirken hata: {e}")
        return None


def AnimeciX():
    query = ui.search_menu(config.default_ui, "Anime ara >")

    if not query or query == "Çık":
        return

    search_data = animecix().fetch_anime_search_data(query)

    # YENİ EKLENEN KONTROL: Eğer arama sonucu boşsa
    if not search_data:
        ui.show_error(config.default_ui, "Arama sonucu bulunamadı.")
        return

    anime_data = [{"name": item["name"], "id": item["id"], "title_type": item.get(
        "title_type", ""), "type": item.get("type", ""), "poster": item.get("poster", "")} for item in search_data]
    anime_names = [f'{item["name"]} (ID: {item["id"]})' for item in anime_data]

    selected_anime_name = ui.select_menu(
        config.default_ui, anime_names, "Anime seç:", Type="fuzzy")
    if not selected_anime_name:
        return

    selected_anime_index = anime_names.index(selected_anime_name)
    selected_anime_type = anime_types[selected_anime_index]
    is_movie = selected_anime_type == "movie"

    poster_url = anime_data[selected_anime_index].get("poster")
    poster_url = poster_url if is_valid_image_url(poster_url) else "anitrcli"

    match = re.match(r'(.+) \(ID: (\d+)\)', selected_anime_name)
    if match:
        selected_anime_name = match.group(1)
        selected_anime_id = match.group(2)

    selected_index, selected_label = None, None
    selected_resolution_index = 0
    selected_resolution = None

    def update_watch_api(index, selected_id):
        if is_movie:
            data = animecix().fetch_anime_movie_watch_api_url(selected_id)
            data = data.get("video_streams", [])

            caption_url = None
            for stream in data:
                if "caption_url" in stream:
                    caption_url = stream["caption_url"]
                    break

        else:
            anime_episodes_data_local = animecix().fetch_anime_episodes(selected_id)
            if not anime_episodes_data_local:
                utils.show_notification("anitr-cli", "Bölüm verisi alınamadı.", "critical")
                return [], [], [], None

            data = animecix().fetch_anime_watch_api_url(
                anime_episodes_data_local[index]["url"])

            caption_url = animecix().fetch_tr_caption_url(
                selected_season_index, selected_episode_index, selected_id)

        try:
            data.sort(key=lambda x: int(re.sub(r'\D', '', x['label'])))
        except Exception as e:
            utils.log_error(config.error_log,
                            f"Çözünürlük verileri sıralanırken hata: {e}")
            utils.show_notification(
                "anitr-cli", f"anitr-cli bir hatayla karşılaştı. Hata detayları: {config.error_log}", "critical")
            pass

        labels = [item['label'] for item in data]
        urls = [item['url'] for item in data]
        return data, labels, urls, caption_url

    if not is_movie:
        anime_episodes_data = animecix().fetch_anime_episodes(selected_anime_id)
        if not anime_episodes_data:
            ui.show_error(config.default_ui, "Bu animeye ait bölüm bulunamadı.")
            return
        anime_episode_names = [item['name'] for item in anime_episodes_data]
        selected_episode_index = 0
        total_episodes = len(anime_episode_names)
        selected_episode_name = anime_episode_names[selected_episode_index]
        selected_season_index = anime_episodes_data[selected_episode_index]["season_num"] - 1
    else:
        selected_episode_index = 0
        total_episodes = 1
        selected_episode_name = selected_anime_name
        selected_season_index = 0

    anime_series_menu_options = (
        ["Filmi izle", "Çözünürlük seç", "Kaynak değiştir", "Anime ara", "Çık"] if is_movie else
        ["İzle", "Sonraki bölüm", "Önceki bölüm", "Bölüm seç",
            "Çözünürlük seç", "Kaynak değiştir", "Anime ara", "Çık"]
    )

    while True:
        if selected_resolution:
            if not is_movie:
                menu_header = (f"\033[33mOynatılıyor\033[0m: {selected_anime_name} ({selected_resolution}) |"
                               f" {selected_episode_index + 1}/{total_episodes}"
                               if selected_anime_name else "")
            elif is_movie:
                menu_header = (f"\033[33mOynatılıyor\033[0m: {selected_anime_name} ({selected_resolution})"
                               if selected_anime_name else "")

        else:
            if not is_movie:
                menu_header = (f"\033[33mOynatılıyor\033[0m: {selected_anime_name} |"
                               f" {selected_episode_index + 1}/{total_episodes}"
                               if selected_anime_name else "")
            elif is_movie:
                menu_header = (f"\033[33mOynatılıyor\033[0m: {selected_anime_name}"
                               if selected_anime_name else "")

        utils.smart_print(menu_header, f"{selected_anime_name} için detaylar", False, icon=save_image_from_url(
            poster_url, selected_anime_name))

        if config.discord_rpc.lower() == "enabled":
            rpc.log_anime_details(
                details=f"{selected_anime_name}",
                state=f"{selected_episode_name} ({selected_episode_index + 1}/{
                    total_episodes})" if not is_movie else f"{selected_anime_name}",
                large_image=poster_url,
                large_text=f"{selected_anime_name}",
                source="AnimeciX",
                source_url="https://anm.cx"
            )
            rpc.start_discord_rpc()

        selected_option = ui.select_menu(
            config.default_ui, anime_series_menu_options, "", Type="list", header=menu_header)

        if selected_option == "İzle" or selected_option == "Filmi izle":
            watch_api_data, watch_api_labels, watch_api_urls, subtitle_url = update_watch_api(
                selected_episode_index, selected_anime_id)

            if not watch_api_labels:
                ui.show_error(config.default_ui,
                               "Çözünürlük verisi alınamadı. Lütfen başka bir bölüm veya anime deneyin.")
                continue

            if selected_resolution is None:
                if watch_api_labels:
                    selected_index, selected_label = max(
                        enumerate(watch_api_labels), key=lambda x: int(re.sub(r'\D', '', x[1]))
                    )
                    selected_resolution = selected_label
                    selected_resolution_index = selected_index
                else:
                    selected_resolution_index = 0
            while selected_resolution_index >= len(watch_api_urls):
                selected_resolution_index -= 1
                if selected_resolution_index < 0:
                    ui.show_error(config.default_ui,
                                   "Geçerli bir video URL'si bulunamadı.")
                    break
            if selected_resolution_index < 0:
                continue

            if not is_movie:
                utils.smart_print(
                    f"\033[33mOynatılıyor\033[0m: {selected_episode_name}",
                    f"{selected_anime_name}, {selected_episode_name} ({selected_episode_index+1}/{total_episodes}) oynatılıyor", icon=save_image_from_url(poster_url, selected_anime_name)
                )

            elif is_movie:
                utils.smart_print(
                    f"\033[33mOynatılıyor\033[0m: {selected_anime_name}",
                    f"{selected_anime_name} oynatılıyor", icon=save_image_from_url(poster_url, selected_anime_name)
                )

            try:
                watch_url = watch_api_urls[selected_resolution_index]
            except IndexError as e:
                utils.log_error(config.error_log,
                                f"Video URL'si alınırken çözünürlük indeksi hatası: {e}")
                utils.show_notification(
                    "anitr-cli", f"anitr-cli bir hatayla karşılaştı. Hata detayları: {config.error_log}", "critical")
                continue

            player.open_with_video_player(
                watch_url, subtitle_url, save_position_on_quit=config.save_position_on_quit
            )
            continue

        elif selected_option == "Sonraki bölüm":
            if is_movie:
                ui.show_error(config.default_ui,
                               "Film izliyorsunuz, sonraki bölüm yok.")
                continue
            if selected_episode_index + 1 >= len(anime_episodes_data):
                ui.show_error(config.default_ui, "Zaten son bölümdesiniz.")
                continue
            selected_episode_index += 1
            selected_episode_name = anime_episode_names[selected_episode_index]
            selected_season_index = anime_episodes_data[selected_episode_index]["season_num"] - 1

            if config.discord_rpc.lower() == "enabled":
                rpc.log_anime_details(
                    details=f"{selected_anime_name}",
                    state=f"{selected_episode_name} ({selected_episode_index + 1}/{
                        total_episodes})" if not is_movie else f"{selected_anime_name}",
                    large_image=poster_url,
                    large_text=f"{selected_anime_name}",
                    source="AnimeciX",
                    source_url="https://anm.cx"
                )
                rpc.update_discord_rpc()

            continue

        elif selected_option == "Önceki bölüm":
            if is_movie:
                ui.show_error(config.default_ui,
                               "Film izliyorsunuz, önceki bölüm yok.")
                continue
            if selected_episode_index == 0:
                ui.show_error(config.default_ui, "Zaten ilk bölümdesiniz.")
                continue
            selected_episode_index -= 1
            selected_episode_name = anime_episode_names[selected_episode_index]
            selected_season_index = anime_episodes_data[selected_episode_index]["season_num"] - 1

            if config.discord_rpc.lower() == "enabled":
                rpc.log_anime_details(
                    details=f"{selected_anime_name}",
                    state=f"{selected_episode_name} ({selected_episode_index + 1}/{
                        total_episodes})" if not is_movie else f"{selected_anime_name}",
                    large_image=poster_url,
                    large_text=f"{selected_anime_name}",
                    source="AnimeciX",
                    source_url="https://anm.cx"
                )
                rpc.update_discord_rpc()

            continue

        elif selected_option == "Bölüm seç":
            if is_movie:
                ui.show_error(config.default_ui,
                               "Film izliyorsunuz, bölüm seçme yok.")
                continue
            selected_episode_name_from_menu = ui.select_menu(
                config.default_ui, anime_episode_names, "Bölüm seç:", Type="fuzzy")

            if not selected_episode_name_from_menu:
                continue

            selected_episode_index = anime_episode_names.index(
                selected_episode_name_from_menu)

            if config.discord_rpc.lower() == "enabled":
                rpc.log_anime_details(
                    details=f"{selected_anime_name}",
                    state=f"{selected_episode_name} ({selected_episode_index + 1}/{
                        total_episodes})" if not is_movie else f"{selected_anime_name}",
                    large_image=poster_url,
                    large_text=f"{selected_anime_name}",
                    source="AnimeciX",
                    source_url="https://anm.cx"
                )
                rpc.update_discord_rpc()

            continue

        elif selected_option == "Çözünürlük seç":
            watch_api_data, watch_api_labels, watch_api_urls = update_watch_api(
                selected_episode_index)

            if not watch_api_labels:
                ui.show_error(config.default_ui,
                               "Çözünürlük verisi alınamadı.")
                continue

            selected_resolution = ui.select_menu(
                config.default_ui, watch_api_labels, "Çözünürlük seç:", Type="list")

            if not selected_resolution:
                continue

            selected_resolution_index = watch_api_labels.index(
                selected_resolution)

        elif selected_option == "Kaynak değiştir":
            selected_source = utils.get_source(ui)
            if selected_source == "AnimeciX (anm.cx)":
                return AnimeciX()
            elif selected_source == "OpenAnime (openani.me)":
                return OpenAnime()
            else:
                return

        elif selected_option == "Anime ara":
            AnimeciX()
            continue

        elif selected_option == "Çık":
            sys.exit()


def OpenAnime():
    query = ui.search_menu(config.default_ui, "Anime ara >")
    if not query or query == "Çık":
        return

    search_data = openanime().search(query)

    if not search_data:
        ui.show_error(config.default_ui, "Arama sonucu bulunamadı.")
        return

    anime_names = []
    for item in search_data:
        if "name" in item and "slug" in item:
            anime_names.append(f'{item["name"]} (ID: {item["slug"]})')

    selected_anime_name = ui.select_menu(
        config.default_ui, anime_names, "Anime seç:", Type="fuzzy")

    selected_anime_index = anime_names.index(selected_anime_name)
    poster_url = search_data[selected_anime_index].get('poster')
    poster_url = poster_url if is_valid_image_url(poster_url) else "anitrcli"

    if not selected_anime_name:
        return

    match = re.match(r'(.+) \(ID: (.+)\)', selected_anime_name)
    if match:
        selected_anime_name = match.group(1)
        selected_anime_slug = match.group(2)

    selected_index, selected_label = None, None
    selected_resolution_index = 0
    selected_resolution = None

    seasons_data = openanime().get_seasons(selected_anime_slug)
    anime_type = seasons_data.get("type", "").lower()
    is_movie = anime_type == "movie"

    anime_episodes_data = openanime().get_episodes(selected_anime_slug, is_movie)

    anime_episode_names = []
    for item in anime_episodes_data:
        if is_movie:
            anime_episode_names.append(selected_anime_name)
        else:
            season = item['season']
            episode = item['episode']
            if season == 1:
                anime_episode_names.append(f"{episode}. Bölüm")
            else:
                anime_episode_names.append(
                    f"{season}. Sezon, {episode}. Bölüm")

    if not anime_episodes_data:
        ui.show_error(config.default_ui, "Bu animeye ait bölüm bulunamadı.")
        return

    selected_episode_index = 0
    total_episodes = len(anime_episode_names)
    selected_episode_name = anime_episode_names[selected_episode_index]

    anime_series_menu_options = (
        ["Filmi izle", "Çözünürlük seç", "Kaynak değiştir", "Anime ara", "Çık"] if is_movie else
        ["İzle", "Sonraki bölüm", "Önceki bölüm", "Bölüm seç",
            "Çözünürlük seç", "Kaynak değiştir", "Anime ara", "Çık"]
    )

    def update_watch_api(index):
        episode_data = anime_episodes_data[index]
        data = openanime().get_stream_url(selected_anime_slug,
                                          episode_data["episode"], episode_data["season"])
        if not data:
            return [], [], []

        try:
            data.sort(key=lambda x: int(x['resolution']), reverse=True)
        except Exception as e:
            utils.log_error(config.error_log,
                            f"Çözünürlük verileri sıralanırken hata: {e}")
            utils.show_notification(
                "anitr-cli", f"anitr-cli bir hatayla karşılaştı. Hata detayları: {config.error_log}", "critical")
            pass

        labels = [f"{item['resolution']}p" for item in data]
        urls = [item['url'] for item in data]
        return data, labels, urls

    while True:
        if selected_resolution:
            menu_header = (f"\033[33mOynatılıyor\033[0m: {selected_anime_name} ({selected_resolution}) |"
                           f" {selected_episode_index + 1}/{total_episodes}"
                           if selected_anime_name else "")
        else:
            menu_header = (f"\033[33mOynatılıyor\033[0m: {selected_anime_name} |"
                           f" {selected_episode_index + 1}/{total_episodes}"
                           if selected_anime_name else "")

        utils.smart_print(menu_header, f"{selected_anime_name} için detaylar", False, icon=save_image_from_url(
            poster_url, selected_anime_name))

        if config.discord_rpc.lower() == "enabled":
            rpc.log_anime_details(
                details=f"{selected_anime_name}",
                state=f"{selected_episode_name} ({selected_episode_index + 1}/{
                    total_episodes})" if not is_movie else f"{selected_anime_name}",
                large_image=poster_url,
                large_text=f"{selected_anime_name}",
                source="OpenAnime",
                source_url="https://openani.me"
            )
            rpc.start_discord_rpc()

        selected_option = ui.select_menu(
            config.default_ui, anime_series_menu_options, "", Type="list", header=menu_header)

        if selected_option in ["İzle", "Filmi izle"]:
            watch_api_data, watch_api_labels, watch_api_urls = update_watch_api(
                selected_episode_index)

            if not watch_api_labels:
                ui.show_error(config.default_ui,
                               "Çözünürlük verisi alınamadı.")
                continue

            if selected_resolution is None:
                selected_index, selected_label = max(
                    enumerate(watch_api_labels), key=lambda x: int(re.sub(r'\D', '', x[1]))
                )
                selected_resolution = selected_label
                selected_resolution_index = selected_index

            while selected_resolution_index >= len(watch_api_urls):
                selected_resolution_index -= 1
                if selected_resolution_index < 0:
                    ui.show_error(config.default_ui,
                                   "Geçerli bir video URL'si bulunamadı.")
                    break
            if selected_resolution_index < 0:
                continue

            utils.smart_print(
                f"\033[33mOynatılıyor\033[0m: {selected_episode_name}",
                f"{selected_anime_name}, {
                    selected_episode_name} ({selected_episode_index+1}/{total_episodes}) oynatılıyor", icon=save_image_from_url(poster_url, selected_anime_name)
            )

            raw_video_url = watch_api_urls[selected_resolution_index]
            season_for_url = 1 if is_movie else anime_episodes_data[selected_episode_index]["season"]
            watch_url = f"{
                openanime().player}/animes/{selected_anime_slug}/{season_for_url}/{raw_video_url}"
            subtitle_url = None
            player.open_with_video_player(
                watch_url, subtitle_url, save_position_on_quit=config.save_position_on_quit
            )
            continue

        elif selected_option == "Sonraki bölüm":
            if is_movie:
                ui.show_error(config.default_ui,
                               "Film izliyorsunuz, sonraki bölüm yok.")
                continue
            if selected_episode_index + 1 >= len(anime_episodes_data):
                ui.show_error(config.default_ui, "Zaten son bölümdesiniz.")
                continue
            selected_episode_index += 1
            selected_episode_name = anime_episode_names[selected_episode_index]

            if config.discord_rpc.lower() == "enabled":
                rpc.log_anime_details(
                    details=f"{selected_anime_name}",
                    state=f"{selected_episode_name} ({selected_episode_index + 1}/{
                        total_episodes})" if not is_movie else f"{selected_anime_name}",
                    large_image=poster_url,
                    large_text=f"{selected_anime_name}",
                    source="OpenAnime",
                    source_url="https://openani.me"
                )
                rpc.update_discord_rpc()

            continue

        elif selected_option == "Önceki bölüm":
            if is_movie:
                ui.show_error(config.default_ui,
                               "Film izliyorsunuz, önceki bölüm yok.")
                continue
            if selected_episode_index == 0:
                ui.show_error(config.default_ui, "Zaten ilk bölümdesiniz.")
                continue
            selected_episode_index -= 1
            selected_episode_name = anime_episode_names[selected_episode_index]

            if config.discord_rpc.lower() == "enabled":
                rpc.log_anime_details(
                    details=f"{selected_anime_name}",
                    state=f"{selected_episode_name} ({selected_episode_index + 1}/{
                        total_episodes})" if not is_movie else f"{selected_anime_name}",
                    large_image=poster_url,
                    large_text=f"{selected_anime_name}",
                    source="OpenAnime",
                    source_url="https://openani.me"
                )
                rpc.update_discord_rpc()

            continue

        elif selected_option == "Bölüm seç":
            if is_movie:
                ui.show_error(config.default_ui,
                               "Film izliyorsunuz, bölüm seçme yok.")
                continue
            selected_episode_name_from_menu = ui.select_menu(
                config.default_ui, anime_episode_names, "Bölüm seç:", Type="fuzzy")

            if not selected_episode_name_from_menu:
                continue

            selected_episode_index = anime_episode_names.index(
                selected_episode_name_from_menu)

            if config.discord_rpc.lower() == "enabled":
                rpc.log_anime_details(
                    details=f"{selected_anime_name}",
                    state=f"{selected_episode_name} ({selected_episode_index + 1}/{
                        total_episodes})" if not is_movie else f"{selected_anime_name}",
                    large_image=poster_url,
                    large_text=f"{selected_anime_name}",
                    source="OpenAnime",
                    source_url="https://openani.me"
                )
                rpc.update_discord_rpc()

            continue

        elif selected_option == "Çözünürlük seç":
            watch_api_data, watch_api_labels, watch_api_urls = update_watch_api(
                selected_episode_index)

            if not watch_api_labels:
                ui.show_error(config.default_ui,
                               "Çözünürlük verisi alınamadı.")
                continue

            selected_resolution = ui.select_menu(
                config.default_ui, watch_api_labels, "Çözünürlük seç:", Type="list")

            if not selected_resolution:
                continue

            selected_resolution_index = watch_api_labels.index(
                selected_resolution)

        elif selected_option == "Kaynak değiştir":
            selected_source = utils.get_source(ui)
            if selected_source == "AnimeciX (anm.cx)":
                return AnimeciX()
            elif selected_source == "OpenAnime (openani.me)":
                return OpenAnime()
            else:
                return

        elif selected_option == "Anime ara":
            AnimeciX()
            continue

        elif selected_option == "Çık":
            sys.exit()


def main():
    import modules.update as update
    args = parse_arguments()

    config.default_ui = "tui"

    if not args.update:
        if update.check_update_notice():
            utils.show_notification("anitr-cli", update.check_update_notice())

    if args.update:
        latest = update.get_latest_version()
        if version.parse(latest) > version.parse(config.CURRENT_VERSION):
            print(f"Yeni sürüm bulundu: \033[31mv{
                    config.CURRENT_VERSION}\033[0m → \033[32mv{latest}\033[0m")
            update.download_and_replace_binary()
        else:
            print("Zaten en güncel sürümdesiniz.")
        sys.exit()

    if args.disable_rpc:
        config.discord_rpc = "Disabled"

    if args.source:
        if args.source.lower() == "openanime":
            OpenAnime()
        elif args.source.lower() == "animecix":
            AnimeciX()
        else:
            print(f"\033[31m[!] - Geçersiz kaynak\033[0m")
            sys.exit(1)
    else:
        selected_source = utils.get_source(ui)
        if selected_source == "AnimeciX (anm.cx)":
            AnimeciX()
        elif selected_source == "OpenAnime (openani.me)":
            OpenAnime()
        else:
            return


if __name__ == "__main__":
    main()
