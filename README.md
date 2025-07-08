<div align="center">
  <h1>Önizleme</h1>

| ![animecix](.github/discord_rpc1.png) | ![openanime](.github/discord_rpc2.png) |
| ------------------------------------- | -------------------------------------- |

**anitr-cli-windows:** Bu proje, orijinal [anitr-cli](https://github.com/xeyossr/anitr-cli) terminal tabanlı anime izleme aracının Windows uyumlu hale getirilmiş sürümüdür.  
Orijinal sürüm yalnızca Linux sistemler için optimize edilmişti. Bu fork, Windows kullanıcılarının da aynı deneyimi yaşamasını sağlamak amacıyla oluşturulmuştur.

## ![GitHub release (latest by date)](https://img.shields.io/github/v/release/mstsecurity/anitr-cli-windows?style=for-the-badge&display_name=release&include_prereleases)

</div>

## 💻 Kurulum (Windows)

### 1. MPV Gereksinimi

`anitr-cli` uygulaması MPV medya oynatıcıya bağımlıdır. Sistemde MPV yüklü değilse uygulama çalışmaz.

#### [Scoop](https://adamtheautomator.com/scoop-windows/) ile kurulum

```bash
scoop install mpv
```

#### Manuel kurulum

![MPV](https://github.com/shinchiro/mpv-winbuild-cmake/releases) sayfasından .exe indirip PATH'e ekleyin.

> [!WARNING]
> PATH'e ekleme yapılmadıysa uygulama çalışmaz ve bir hata mesajı verir.

---

### 2. anitr-cli'yi İndirme ve Çalıştırma

1. [Releases](https://github.com/mstsecurity/anitr-cli-windows/releases) sayfasından en son .zip dosyasını indirin ve arşivden çıkarın
2. Klasörü aşağıdaki dizine kopyalayın

```bash
%LOCALAPPDATA%\Programs\
```

3. Python bağımlılıklarını kurun:

```bash
pip install -r requirements.txt
```

4. .bat dosyasını kopyalayın:
   `anitr-cli.bat` dosyasını `%LOCALAPPDATA%\Programs\bin\` içerisine kopyalayın (yoksa klasörü oluşturun), ardından:

```bash
setx PATH "%PATH%;%LOCALAPPDATA%\Programs\bin"
```

## 👾 Kullanım

```
usage: anitr-cli [-h] [--source {AnimeciX,OpenAnime}] [--disable-rpc] [--update]

💫 Terminalden anime izlemek için CLI aracı.

options:
  -h, --help            show this help message and exit
  --source {AnimeciX,OpenAnime}
                        Hangi kaynak ile anime izlemek istediğinizi belirtir. (default: None)
  --disable-rpc         Discord Rich Presence özelliğini devre dışı bırakır. (default: False)
  --update              anitr-cli aracını en son sürüme günceller. (default: False)
```

### Yapılandırma

Yapılandırma dosyası şurada bulunur:
`C:\Users\<kullanıcı_adı>\.anitr-cli\config`

Örnek yapılandırma:

```ini
discord_rpc=Enabled
save_position_on_quit=True
```

Açıklamalar:

- `discord_rpc` — Discord Rich Presence özelliğini etkinleştirir/devre dışı bırakır.
- `save_position_on_quit` — MPV üzerinden izlemeyi bıraktığınız saniyeyi hatırlayıp tekrar başlattığınızda aynı yerden devam eder.

## Bu Fork Hakkında

Bu proje, [xeyossr/anitr-cli](https://github.com/xeyossr/anitr-cli) projesinin bir forkudur.  
Orijinal proje yalnızca Linux ortamını hedefliyordu. Bu fork, Windows desteği eklemek amacıyla başlatılmıştır.

Kurucu ve geliştirici: [@xeyossr](https://github.com/xeyossr)  
Projeye katkıda bulunan herkes için katkı geçmişine göz atabilirsiniz: [Commits](https://github.com/mstsecurity/anitr-cli-windows/commits)

Fork, orijinal projeyle paralel güncellemeleri izler ve gerekli durumlarda özelleştirmeler içerir.

---

## Sorunlar

Bir sorunla karşılaşırsanız lütfen [issue](https://github.com/mstsecurity/anitr-cli-windows/issues) sayfasına bildirin.  
Windows’a özel karşılaşılan sorunlar bu projeye, genel sorunlar ise ana projeye bildirilmelidir.

---

## Lisans

Bu proje, orijinal proje gibi GNU General Public License v3.0 (GPL-3) lisansı altındadır.  
Daha fazla bilgi için [LICENSE](LICENSE) dosyasını inceleyebilirsiniz.
