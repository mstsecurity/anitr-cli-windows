# Katkıda Bulunma Rehberi

## 1. Katkıda Bulunmadan Önce

Pull request atmadan önce, lütfen aşağıdaki adımları izlediğinizden emin olun:

- **Projeyi Fork Edin**: Öncelikle bu projeyi kendi GitHub hesabınıza fork edin. Böylece kendi kopyanız üzerinde çalışmalar yapabilirsiniz.
- **Branch (Dal) Oluşturun**: Ana projeye katkı sağlamak için ana dalı (main) değil, kendi dalınızı kullanın. Yeni özellikler veya hata düzeltmeleri için yeni bir branch (dal) oluşturun. Branch adı, üzerinde çalıştığınız konu ile ilgili olmalı:

```bash
git checkout -b yeni-ozellik-adi
```

- **Kendi Fork'unuzu Güncel Tutun:** Projenin ana dalında yapılan güncellemeleri takip etmek için kendi fork'unuzu zaman zaman güncelleyin.

## 2. Kod Yazma Kuralları

AniTR-CLI projesine katkı sağlarken aşağıdaki kurallara dikkat etmeniz beklenir:

- **Kod Düzenine Dikkat Edin**: Projeye eklediğiniz kodun temiz ve düzenli olmasına özen gösterin. Okunabilirliği artırmak için açıklamalar eklemeyi unutmayın.
- **Fonksiyon ve Değişken İsimlendirmesi**: Anlamlı isimler kullanarak, kodunuzun ne yaptığını kolayca anlayabilen başkalarının işini kolaylaştırın. Kısa ve anlamlı isimler seçmeye çalışın.

## 3. Pull Request (PR) Göndermek

Kodunuzu yazıp, test edip, branch'ınızı oluşturduktan sonra pull request (PR) gönderebilirsiniz. PR göndermeden önce aşağıdaki adımları takip edin:

- **PR Açmadan Önce**: Kendi branch'ınızda yaptığınız değişiklikleri test edin ve her şeyin düzgün çalıştığından emin olun.
- **Detaylı Açıklama Ekleyin**: PR başlığında, yaptığınız değişikliği veya eklediğiniz özelliği açıkça belirtin. Ayrıca PR açıklamasına yaptığınız değişiklikle ilgili daha fazla bilgi ekleyin.
- **Testler**: Eğer mümkünse, yaptığınız değişikliklerin testlerini ekleyin. Bu, başkalarının kodunuzun düzgün çalışıp çalışmadığını kontrol etmelerine yardımcı olur.
- **Doğru Branch'e PR Gönderin**: Yapmanız gereken değişiklikleri doğru branch'e göndermek için PR'yi oluştururken dikkatli olun. PR'ler `main` dalına yapılmalıdır.

## 4. Issue Açma

Eğer projede bir hata veya geliştirme önerisi ile ilgili bir konu fark ederseniz, lütfen bir **issue** açarak durumu belirtin. Issue açarken şunlara dikkat edin:

- **Açıklayıcı Olun**: Sorunu veya öneriyi açıkça ve detaylı bir şekilde açıklayın.
- **Adımlar**: Hatanın nasıl tekrar edilebileceğini belirten adımları yazın. Eğer bir hata ise, hata mesajları ve çıktıları ekleyin.
- **Çözüm Önerisi**: Eğer mümkünse, sorunun çözümü ile ilgili önerilerde bulunun.

## 5. Lisans

Bu proje, [GPL3 lisansı](LICENSE) altında lisanslanmıştır. Katkılarınızı göndermeden önce bu lisansı gözden geçirdiğinizden emin olun.

## 6. Davranış Kuralları

Projeye katkıda bulunan herkesin aşağıdaki davranış kurallarına uymasını bekliyoruz:

- Saygılı olun.
- Herkesin fikirlerine değer verin ve farklı bakış açılarına saygı gösterin.
- Yardımcı olabileceğiniz yerlerde başkalarına destek olun.
