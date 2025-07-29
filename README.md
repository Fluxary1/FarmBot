# FarmBot

Bu, Minecraft'ta sana yardımcı olmak için hazırlanmış basit bir otomasyon botudur.

## Nedir Bu?

Bu FarmBot, Minecraft'ta belirli tekrarlayan görevleri senin yerine yapması için tasarlandı. Özellikle iki ana farm türü için otomasyon sağlar:

* **XP Farmı (Zombi Farmı):** Genellikle zombi farmı gibi yerlerde fare tıklamalarını otomatikleştirir, böylece sen AFK kalırken XP kasabilirsin.
* **Raid Farmı:** Raid farmında gerekli iksir ve kılıç slotuna geçişleri ve tıklamaları otomatikleştirir.

Botu süresiz çalıştırabilir veya belirli bir süre sonra otomatik olarak duracak şekilde ayarlayabilirsin. Ayrıca süre bitiminde sadece botu durdurabilir, Minecraft'ı kapatabilir veya hem Minecraft'ı hem de programı tamamen kapatabilirsin.

## Nasıl Çalışır?

1.  **Programı Başlat:** `FarmBot.exe` dosyasını (veya Python dosyasını) çalıştır.
2.  **Farm Türünü Seç:** Ana ekranda "XP FARM" veya "RAID FARM" seçeneklerinden birini tıkla.
    * **XP Farmı için:** Süresiz mi yoksa süreli mi çalışacağını seçersin. Süreli seçersen ne kadar süre çalışacağını girer, ardından süre bitiminde ne yapılacağını belirlersin.
    * **Raid Farmı için:** Doğrudan başlar ve ayarları sabittir.
3.  **Botu Başlat:** Seçimlerini yaptıktan sonra "Başlat" düğmesine tıkla.
4.  **Oyun Ekranına Geç:** Bot başladıktan sonra 5 saniye içinde Minecraft ekranına geçiş yaptığından ve botun tıklamaları doğru yere yapabildiğinden emin ol. Oyun içinde klavye menüsünün (`ESC` ile açılan) kapalı olduğundan emin olman önemli.
5.  **Durdurmak İçin:** İstediğin zaman programdaki "STOP" düğmesine basarak otomasyonu durdurabilirsin.

## Kurulum (Python ile Çalıştırmak İstersen)

Eğer `.exe` dosyasını kullanmak yerine Python kodunu doğrudan çalıştırmak istersen, bilgisayarında Python'ın kurulu olması ve şu kütüphanelere ihtiyacın var:

* `customtkinter`
* `pyautogui`

Bu kütüphaneleri yüklemek için komut istemcisine şunları yazabilirsin:

```bash
pip install customtkinter pyautogui
