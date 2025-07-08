<!--div align="center">
  <h1>Önizleme</h1>
</div>

[preview.mp4](https://github.com/user-attachments/assets/199d940e-14c6-468c-9120-496185ab2217)

<p>
  <img src="assets/discord_rpc_preview.png"/>
</p>
-->

**anitr-cli (Windows Fork):** Bu proje, orijinal [anitr-cli](https://github.com/xeyossr/anitr-cli) terminal tabanlı anime izleme aracının Windows uyumlu hale getirilmiş sürümüdür.  
Orijinal sürüm yalnızca Linux sistemler için optimize edilmişti. Bu fork, Windows kullanıcılarının da aynı deneyimi yaşamasını sağlamak amacıyla oluşturulmuştur.

## ![GitHub release (latest by date)](https://img.shields.io/github/v/release/mstsecurity/anitr-cli-windows?style=for-the-badge&display_name=release&include_prereleases)

## 💻 Kurulum (Windows)

### 1. MPV Gereksinimi

`anitr-cli` uygulaması MPV medya oynatıcıya bağımlıdır. Sistemde MPV yüklü değilse uygulama çalışmaz.

#### MPV Nasıl Kurulur?

1. [https://mpv.io/installation/](https://mpv.io/installation/) sayfasına gidin.
2. "Windows" başlığı altındaki "Installer" bağlantısından `.exe` dosyasını indirin.
3. Kurulum sırasında MPV'nin sistem `PATH` değişkenine eklenmesine dikkat edin. Aksi takdirde uygulama MPV'yi bulamaz.

> [!WARNING]
> PATH'e ekleme yapılmadıysa uygulama çalışmaz ve bir hata mesajı verir.

---

### 2. anitr-cli'yi İndirme ve Çalıştırma

1. [Releases](https://github.com/mstsecurity/anitr-cli-windows/releases) sayfasından en son `anitr-cli.exe` dosyasını indirin.
2. Dosyayı aşağıdaki dizine manuel olarak kopyalayın:

```bash
%LOCALAPPDATA%\Programs\anitr-cli\
```

> Bu klasör yoksa elle oluşturabilirsiniz.

3. `anitr-cli.exe` çalıştırılabilir hale geldikten sonra, terminal (CMD) üzerinden aşağıdaki komutu kullanarak erişebilirsiniz:

```bash
anitr-cli
```

> Eğer `PATH` değişkenine yukarıdaki klasör eklenmemişse, tam yolu vermeniz gerekebilir.

## 👾 Kullanım

```
usage: anitr-cli.exe [-h] [--source {AnimeciX,OpenAnime}] [--disable-rpc] [--tui] [--update]

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
