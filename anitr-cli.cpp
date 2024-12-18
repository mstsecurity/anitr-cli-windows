#include "modules/anitr_fetch.h"
#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <cstdlib>
#include <fstream>
#include <sstream>

// Yardım menüsünü yazdırır
void printHelp() {
    std::cout << "anitr-cli kullanımı:\n"
              << "  --help, -h: Bu yardım menüsünü gösterir\n"
              << "  --gen-config: rofi-flags.conf dosyasını oluşturur\n"
              << "\n";
}

// rofi.flags.conf dosyasını oluşturacak funksiyon
void generateConfigFile() {
    std::string configDir = std::string(getenv("HOME")) + "/.config/anitr-cli";
    std::string configFile = configDir + "/rofi-flags.conf";

    // Klasörü oluştur (varsa atla)
    std::filesystem::create_directories(configDir);

    // Konfigürasyon dosyası varsa, uyarı göster ve çık
    if (std::filesystem::exists(configFile)) {
        std::cout << "Konfigürasyon dosyası zaten var: " << configFile << "\n";
        return;
    }

    // Varsayılan parametrelerle dosya oluştur
    std::ofstream config(configFile);
    if (config.is_open()) {
        config << "";
        config.close();
        std::cout << "Konfigürasyon dosyası oluşturuldu: " << configFile << "\n";
    } else {
        std::cerr << "Konfigürasyon dosyası oluşturulamıyor: " << configFile << "\n";
    }
}


// Kullanıcıdan rofi ile giriş alacak fonksiyon
std::string getInputFromRofi(const std::string& prompt, const std::vector<std::string>& options) {
    // Rofi parametrelerini okumak için konfigürasyon dosyasını kontrol et
    std::string rofi_flags = "";
    std::ifstream config_file(std::string(getenv("HOME")) + "/.config/anitr-cli/rofi-flags.conf");

    if (config_file.is_open()) {
        std::string line;
        while (std::getline(config_file, line)) {
            if (!line.empty() && line[0] != '#') {  // Yorum satırlarını atla
                rofi_flags += line + " ";  // Parametreleri birleştir
            }
        }
        config_file.close();
    }

    // Rofi komutunu oluştur
    std::string rofi_cmd = "echo '" + prompt + "\n" + 
                            "\n" + 
                            "[\n" + 
                            "  '" + prompt + "'\n" +
                            "'<back>'\n" +
                            "'<exit>'" + 
                            "']\n\n" ;
    rofi_cmd += "echo -e \"" ;
    for (const auto& option : options) {
        rofi_cmd += option + "\n";
    }

    rofi_cmd += "\" | rofi -dmenu -p '" + prompt + "' " + rofi_flags;  // Parametreleri ekle
    std::string selected;
    FILE* fp = popen(rofi_cmd.c_str(), "r");
    if (fp != NULL) {
        char buffer[1024];
        if (fgets(buffer, sizeof(buffer), fp) != NULL) {
            selected = buffer;
        }
        fclose(fp);
    }

    // Satır sonu karakterini kaldır
    if (!selected.empty() && selected.back() == '\n') {
        selected.pop_back();
    }

    return selected;
}

int main(int argc, char* argv[]) {

    // Komut satırı parametrelerini kontrol et
    for (int i = 1; i < argc; ++i) {
        std::string arg = argv[i];
        if (arg == "--help" || arg == "-h") {
            printHelp();
            return 0;
        } else if (arg == "--gen-config") {
            generateConfigFile();
            return 0;
        }
    }

    FetchData fetchdata;
    std::vector<std::map<std::string, std::string>> anime_episodes;
    int selected_episode_index = 0;

    // Anime arama prompt'u
    std::string query = getInputFromRofi("Anime Ara", {});
    // Arama kısmına <exit> ya da exit yazıldıysa çık
    if (query == "<exit>" || query == "exit") exit(0);
    // Arama kısmına sadece özel karakter, sayı ya da boşluk koyulmuşsa kapat
    else if (query.find_first_of("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") == std::string::npos) return 0;
    
    // Arama sonuçlarını al
    auto results = fetchdata.fetch_anime_search_data(query);

    if (results.empty()) {
        std::cout << "Sonuç bulunamadı. Tekrar deneyin!" << std::endl;
        return 0;
    }

    std::vector<std::string> anime_names;
    for (const auto& item : results) {
        anime_names.push_back(item.at("name"));
    }

    // Anime seçimi
    std::string selected_anime_name = getInputFromRofi("Select Anime", anime_names);
    if (selected_anime_name == "<exit>" || selected_anime_name == "exit") exit(0);

    // Seçilen animeyi bul
    std::map<std::string, std::string> selected_anime;
    for (const auto& item : results) {
        if (item.at("name") == selected_anime_name) {
            selected_anime = item;
            break;
        }
    }

    // Seçilen animenin bölümlerini al
    std::string selected_id = selected_anime.at("id");
    anime_episodes = fetchdata.fetch_anime_episodes(selected_id);

    if (anime_episodes.empty()) {
        std::cout << "Bölüm bulunamadı. Tekrar deneyin." << std::endl;
        return 0;
    }

    while (true) {
        // Ana menü seçenekleri
        std::vector<std::string> main_menu_options = {
            "İzle", "Sonraki Bölüm", "Önceki Bölüm", "Bölüm Seç", "Anime Ara", "Çık", anime_episodes[selected_episode_index].at("name")
        };

        // Ana menüyü göster
        std::string main_menu_choice = getInputFromRofi("Main Menu", main_menu_options);

        if (main_menu_choice == "Çık") {
            exit(0);
            break;
        } else if (main_menu_choice == "Anime Ara") {
            // Anime arama işlemini tekrar başlat
            query = getInputFromRofi("Anime Ara", {});
            if (query == "<exit>" || query.empty()) break;

            results = fetchdata.fetch_anime_search_data(query);
            if (results.empty()) {
                std::cout << "Sonuç bulunamadı. Tekrar deneyin." << std::endl;
                continue;
            }

            anime_names.clear();
            for (const auto& item : results) {
                anime_names.push_back(item.at("name"));
            }

            selected_anime_name = getInputFromRofi("Anime Seç", anime_names);
            if (selected_anime_name == "<exit>" || selected_anime_name.empty()) break;

            // Seçilen animenin verisini bul
            for (const auto& item : results) {
                if (item.at("name") == selected_anime_name) {
                    selected_anime = item;
                    break;
                }
            }

            selected_id = selected_anime.at("id");
            anime_episodes = fetchdata.fetch_anime_episodes(selected_id);
            if (anime_episodes.empty()) {
                std::cout << "Bölüm bulunamadı. Tekrar deneyin." << std::endl;
                continue;
            }
        } else if (main_menu_choice == "İzle") {
            // Seçilen bölümün URL'sini al
            std::string episode_url = anime_episodes[selected_episode_index].at("url");
            // Bölüm URL'si ile izleme URL'sini al
            std::vector<std::map<std::string, std::string>> watch_url = fetchdata.fetch_anime_watch_api_url(episode_url);

            if (!watch_url.empty()) {
                // URL'yi al
                std::string video_url = watch_url.back().at("url");

                // MPV ile izleme başlat
                std::cout << "Watching: " << video_url << std::endl;
                std::string mpv_cmd = "mpv --fullscreen " + video_url;
                system(mpv_cmd.c_str());
            } else {
                std::cout << "Failed to fetch watch URL." << std::endl;
            }
        } else if (main_menu_choice == "Sonraki Bölüm") {
            if (selected_episode_index < anime_episodes.size() - 1) {
                selected_episode_index++;
                
                std::string episode_url = anime_episodes[selected_episode_index].at("url");
                std::vector<std::map<std::string, std::string>> watch_url = fetchdata.fetch_anime_watch_api_url(episode_url);

                // URL'yi al
                std::string video_url = watch_url.back().at("url");

                // MPV ile izleme başlat
                std::cout << "Watching: " << video_url << std::endl;
                std::string mpv_cmd = "mpv --fullscreen " + video_url;
                system(mpv_cmd.c_str());

            } else {
                std::cout << "En son bölümdesiniz" << std::endl;
            }
        } else if (main_menu_choice == "Önceki Bölüm") {
            if (selected_episode_index > 0) {
                selected_episode_index--;

                std::string episode_url = anime_episodes[selected_episode_index].at("url");
                std::vector<std::map<std::string, std::string>> watch_url = fetchdata.fetch_anime_watch_api_url(episode_url);
                
                // URL'yi al
                std::string video_url = watch_url.back().at("url");

                // MPV ile izleme başlat
                std::cout << "Watching: " << video_url << std::endl;
                std::string mpv_cmd = "mpv --fullscreen " + video_url;
                system(mpv_cmd.c_str());

            } else {
                std::cout << "İlk bölümdesiniz" << std::endl;
            }
        } else if (main_menu_choice == "Bölüm Seç") {
            // Bölüm listesini göster ve kullanıcıyı seçim yapmaya yönlendir
            std::vector<std::string> episode_titles;
            for (const auto& episode : anime_episodes) {
                episode_titles.push_back(episode.at("name"));
            }

            std::string selected_episode_title = getInputFromRofi("Bölüm Seç", episode_titles);
            if (selected_episode_title == "<exit>" || selected_episode_title.empty()) break;

            // Seçilen bölüm verisini bul
            for (int i = 0; i < anime_episodes.size(); i++) {
                if (anime_episodes[i].at("name") == selected_episode_title) {
                    selected_episode_index = i;
                    break;
                }
            }
        }
    }

    return 0;
}
