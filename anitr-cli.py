#!/usr/bin/env python3

from modules.fetch import animecix, openanime
import modules.player as player
import modules.ui as ui

from dotenv import load_dotenv
import argparse, sys, os, re

load_dotenv(os.path.expanduser("~/.config/anitr-cli/config"))
default_ui = os.getenv("DEFAULT_UI", "tui")
sources = ["AnimeciX (anm.cx)", "OpenAnime (openani.me)"]

def get_source() -> str:
    return ui.select_menu(default_ui, sources, "Kaynak seç:", False)

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="💫 Terminalden anime izlemek için CLI aracı."
    )

    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "--rofi",
        action="store_true",
        help="Uygulamanın arayüzünü rofi ile açar."
    )
    group.add_argument(
        "--tui",
        action="store_true",
        help="Terminalde TUI arayüzü ile açar."
    )

    return parser.parse_args()

def AnimeciX():
    def remove_movies_animecix(data):
        return [
            item for item in data
            if item.get("type") != "movie" and item.get("title_type") != "movie"
        ]
    
    query = ui.search_menu(default_ui, "Anime ara >")
    
    if not query or query == "Çık":
        return

    search_data = animecix().fetch_anime_search_data(query)
    search_data = remove_movies_animecix(search_data)
    
    anime_data = [{"name": item["name"], "id": item["id"]} for item in search_data]
    anime_names = [f'{item["name"]} (ID: {item["id"]})' for item in anime_data]
    
    selected_anime_name = ui.select_menu(default_ui, anime_names, "Anime seç:", True)
    if not selected_anime_name:
        return

    match = re.match(r'(.+) \(ID: (\d+)\)', selected_anime_name)
    if match:
        selected_anime_name = match.group(1)
        selected_anime_id = match.group(2)

    # labels = []  # kullanılmıyor
    selected_index, selected_label = None, None 
    selected_resolution_index = 0  
    selected_resolution = None 

    def update_watch_api(index):
        data = animecix().fetch_anime_watch_api_url(anime_episodes_data[index]["url"])
        labels = [item['label'] for item in data]
        urls = [item['url'] for item in data]
        return data, labels, urls

    anime_episodes_data = animecix().fetch_anime_episodes(selected_anime_id)
    anime_episode_names = [item['name'] for item in anime_episodes_data]
    selected_episode_index = 0
    total_episodes = len(anime_episode_names)
    selected_episode_name = anime_episode_names[selected_episode_index]
    selected_season_index = anime_episodes_data[selected_episode_index]["season_num"] - 1

    anime_series_menu_options = ["İzle", "Sonraki bölüm", "Önceki bölüm", "Bölüm seç", "Çözünürlük seç", "Anime ara", "Çık"]

    while True:
        if selected_resolution:
            menu_header = (f"\033[33mOynatılıyor\033[0m: {selected_anime_name} ({selected_resolution}) |"
                           f" {selected_episode_index + 1}/{total_episodes}"
                           if selected_anime_name else "")
        else:
            menu_header = (f"\033[33mOynatılıyor\033[0m: {selected_anime_name} |"
                           f" {selected_episode_index + 1}/{total_episodes}"
                           if selected_anime_name else "")
            
        print(menu_header)
        selected_option = ui.select_menu(default_ui, anime_series_menu_options, "", False, menu_header)

        if selected_option == "İzle":
            watch_api_data, watch_api_labels, watch_api_urls = update_watch_api(selected_episode_index)

            if selected_resolution is None:
                if watch_api_labels:
                    selected_index, selected_label = max(
                        enumerate(watch_api_labels), key=lambda x: int(x[1][:-1])
                    )
                    selected_resolution = selected_label 
                    selected_resolution_index = selected_index
                else:
                    # selected_resolution = watch_api_labels[0]  # hata verebilir çünkü watch_api_labels boş olabilir
                    selected_resolution_index = 0

            while selected_resolution_index >= len(watch_api_urls):
                selected_resolution_index -= 1

            selected_season_index = anime_episodes_data[selected_episode_index]["season_num"] - 1
            watch_url = watch_api_urls[selected_resolution_index]
            subtitle_url = animecix().fetch_tr_caption_url(selected_season_index, selected_episode_index, selected_anime_id)
            print(f"\033[33mOynatılıyor\033[0m: {selected_episode_name}")
            player.open_with_video_player(watch_url, subtitle_url)
            continue

        elif selected_option == "Sonraki bölüm":
            if selected_episode_index + 1 >= len(anime_episodes_data):
                ui.show_error(default_ui, "Zaten son bölümdesiniz.")
                continue
            selected_episode_index += 1
            selected_episode_name = anime_episode_names[selected_episode_index]
            continue

        elif selected_option == "Önceki bölüm":
            if selected_episode_index == 0:
                ui.show_error(default_ui, "Zaten ilk bölümdesiniz.")
                continue
            selected_episode_index -= 1
            selected_episode_name = anime_episode_names[selected_episode_index]
            continue

        elif selected_option == "Bölüm seç":
            selected_episode_name = ui.select_menu(default_ui, anime_episode_names, "Bölüm seç:", True)

            if not selected_episode_name:
                continue

            selected_episode_index = anime_episode_names.index(selected_episode_name)
            selected_episode_name = anime_episode_names[selected_episode_index]
            continue
        
        elif selected_option == "Çözünürlük seç":
            watch_api_data, watch_api_labels, watch_api_urls = update_watch_api(selected_episode_index)
            selected_resolution = ui.select_menu(default_ui, watch_api_labels, "Çözünürlük seç:", False)

            if not selected_resolution:
                continue

            selected_resolution_index = watch_api_labels.index(selected_resolution)
        
        elif selected_option == "Anime ara":
            AnimeciX()
            continue

        elif selected_option == "Çık":
            sys.exit()

def OpenAnime():    
    query = ui.search_menu(default_ui, "Anime ara >")
    if not query or query == "Çık":
        return
    
    search_data = openanime().search(query)
    
    anime_names = [f'{item["name"]} (ID: {item["slug"]})' for item in search_data]

    selected_anime_name = ui.select_menu(default_ui, anime_names, "Anime seç:", True)
    
    if not selected_anime_name:
        return
    
    match = re.match(r'(.+) \(ID: (.+)\)', selected_anime_name)
    if match:
        selected_anime_name = match.group(1)
        selected_anime_slug = match.group(2)

    # labels = []  # kullanılmıyor
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
                anime_episode_names.append(f"{season}. Sezon, {episode}. Bölüm")

    # seasons_data = openanime().get_seasons(selected_anime_slug)  # tekrar alınmış, gereksiz
    # anime_type = seasons_data.get("type", "movie")  # tekrar alınmış, gereksiz
    # is_movie = anime_type == "movie"  # tekrar alınmış, gereksiz

    # anime_episodes_data = openanime().get_episodes(selected_anime_slug, is_movie)  # tekrar alınmış, gereksiz

    if not anime_episodes_data:
        ui.show_error(default_ui, "Bu animeye ait bölüm bulunamadı.")
        return

    selected_episode_index = 0
    total_episodes = len(anime_episode_names)
    selected_episode_name = anime_episode_names[selected_episode_index]
    

    anime_series_menu_options = (
        ["Filmi izle", "Çözünürlük seç", "Anime ara", "Çık"] if is_movie else
        ["İzle", "Sonraki bölüm", "Önceki bölüm", "Bölüm seç", "Çözünürlük seç", "Anime ara", "Çık"]
    )

    def update_watch_api(index):
        episode_data = anime_episodes_data[index]
        data = openanime().get_stream_url(selected_anime_slug, episode_data["episode"], episode_data["season"])
        if not data:
            return [], [], []
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

        print(menu_header)
        selected_option = ui.select_menu(default_ui, anime_series_menu_options, "", False, menu_header)

        if selected_option in ["İzle", "Filmi izle"]:
            watch_api_data, watch_api_labels, watch_api_urls = update_watch_api(selected_episode_index)

            if not watch_api_labels:
                ui.show_error(default_ui, "Çözünürlük verisi alınamadı.")
                continue

            if selected_resolution is None:
                selected_index, selected_label = max(
                    enumerate(watch_api_labels), key=lambda x: int(x[1][:-1])
                )
                selected_resolution = selected_label 
                selected_resolution_index = selected_index

            while selected_resolution_index >= len(watch_api_urls):
                selected_resolution_index -= 1

            raw_video_url = watch_api_urls[selected_resolution_index]
            season_for_url = 1 if is_movie else anime_episodes_data[selected_episode_index]["season"]
            watch_url = f"{openanime().player}/animes/{selected_anime_slug}/{season_for_url}/{raw_video_url}"
            subtitle_url = None
            print(f"\033[33mOynatılıyor\033[0m: {selected_episode_name}")
            player.open_with_video_player(watch_url, subtitle_url)
            continue

        elif selected_option == "Sonraki bölüm":
            if selected_episode_index + 1 >= len(anime_episodes_data):
                ui.show_error(default_ui, "Zaten son bölümdesiniz.")
                continue
            selected_episode_index += 1
            selected_episode_name = anime_episode_names[selected_episode_index]
            continue

        elif selected_option == "Önceki bölüm":
            if selected_episode_index == 0:
                ui.show_error(default_ui, "Zaten ilk bölümdesiniz.")
                continue
            selected_episode_index -= 1
            selected_episode_name = anime_episode_names[selected_episode_index]
            continue

        elif selected_option == "Bölüm seç":
            selected_episode_name = ui.select_menu(default_ui, anime_episode_names, "Bölüm seç:", True)

            if not selected_episode_name:
                continue

            selected_episode_index = anime_episode_names.index(selected_episode_name)
            continue

        elif selected_option == "Çözünürlük seç":
            watch_api_data, watch_api_labels, watch_api_urls = update_watch_api(selected_episode_index)
            selected_resolution = ui.select_menu(default_ui, watch_api_labels, "Çözünürlük seç:", False)

            if not selected_resolution:
                continue

            selected_resolution_index = watch_api_labels.index(selected_resolution)
        
        elif selected_option == "Anime ara":
            OpenAnime()
            continue

        elif selected_option == "Çık":
            sys.exit()

def main():
    global default_ui
    args = parse_arguments()

    if args.rofi:
        default_ui = "rofi"
    elif args.tui:
        default_ui = "tui"
    
    selected_source = get_source()
    if selected_source == "AnimeciX (anm.cx)":
        AnimeciX()
    elif selected_source == "OpenAnime (openani.me)":
        OpenAnime()
    else:
        return

if __name__ == "__main__":
    main()
