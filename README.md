# TTX

Bu proje, **Edge-TTS** kütüphanesini kullanarak metinleri Türkçe yapay zeka seslerine dönüştüren, kullanımı kolay ve modern bir masaüstü arayüz uygulamasıdır. **CustomTkinter** kütüphanesi ile geliştirilmiştir.

## Özellikler

- **Türkçe Ses Desteği:** Erkek ve Kadın ses seçenekleri.
- **Hız (Rate) Ayarı:** Ses çıkış hızını `%` bazında özelleştirme.
- **Perde (Pitch) Ayarı:** Ses tonunu `Hz` bazında inceltip kalınlaştırma.
- **Asenkron Çalışma:** Ses işleme esnasında arayüz donmaz veya kilitlenmez.
- **MP3 Çıktısı:** Oluşturulan sesleri doğrudan bilgisayarınıza kaydedebilirsiniz.

---

## Kurulum ve Çalıştırma

### 1. Gerekli Kütüphanelerin Kurulması

Projeyi çalıştırmak için öncelikle gerekli Python kütüphanelerini yüklemeniz gerekir:

```bash
pip install -r requirements.txt
