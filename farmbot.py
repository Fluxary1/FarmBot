import time
import pyautogui
import customtkinter as ctk
import threading
import sys

# pyautogui'nin her işlem arasında bekleyeceği varsayılan süreyi ayarladık
pyautogui.PAUSE = 0.05

class FarmBotApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("600x550")
        self.title("Farm Bot")
        ctk.set_appearance_mode("dark")

        self.is_automation_running = False
        self.automation_thread = None

        self.ZOMBIE_FARM_DELAY = 25
        self.RAID_FARM_DELAY = 2 # Raid farmı için 2 saniye gecikme

        self.current_frame = None
        self.current_farm_type_for_timed = None

        self.create_widgets()
        self.show_main_page()

    def create_widgets(self):
        # --- Ana Sayfa Frame'i ---
        self.main_page_frame = ctk.CTkFrame(self, fg_color="transparent")

        ctk.CTkLabel(master=self.main_page_frame, text="Zombi Farmı Modu", font=("Arial", 18, "bold")).pack(pady=(20, 10))

        button_zombie_infinite = ctk.CTkButton(master=self.main_page_frame, text="Zombi Farmı - Süresiz Aç", corner_radius=25,
                                               fg_color="#4E71FF", hover_color="#5000DA",
                                               command=lambda: self.start_automation("Zombi Farm Botu"))
        button_zombie_infinite.pack(pady=10, anchor="center")

        button_zombie_timed = ctk.CTkButton(master=self.main_page_frame, text="Zombi Farmı - Süreyi Ayarla", corner_radius=25,
                                            fg_color="#4E71FF", hover_color="#5000DA",
                                            command=lambda: self.show_timed_options("Zombi Farm Botu"))
        button_zombie_timed.pack(pady=10, anchor="center")

        ctk.CTkFrame(master=self.main_page_frame, height=2, fg_color="gray").pack(fill="x", pady=20)

        ctk.CTkLabel(master=self.main_page_frame, text="Raid Farmı Modu", font=("Arial", 18, "bold")).pack(pady=(10, 10))

        # Raid Farmı için sadece tek "Başlat" butonu
        button_raid_start = ctk.CTkButton(master=self.main_page_frame, text="Raid Farmı - Başlat", corner_radius=25,
                                          fg_color="#4E71FF", hover_color="#5000DA",
                                          command=lambda: self.start_automation("Raid Farm Botu", duration=355, end_action="stop_only", is_raid_farm=True))
        button_raid_start.pack(pady=10, anchor="center")
        
        ctk.CTkFrame(master=self.main_page_frame, height=2, fg_color="gray").pack(fill="x", pady=20)


        # --- Ayarlar Sayfası Frame'i ---
        self.settings_page_frame = ctk.CTkFrame(self, fg_color="transparent")
        ctk.CTkLabel(master=self.settings_page_frame, text="Ayarlar", font=("Arial", 24, "bold")).pack(pady=20)
        ctk.CTkLabel(master=self.settings_page_frame, text="Buraya ileride gecikme ayarları, tuş atamaları vb. eklenecek.").pack(pady=10)
        
        button_back_from_settings = ctk.CTkButton(master=self.settings_page_frame, text="Geri", corner_radius=25,
                                                  fg_color="#4E71FF", hover_color="#5000DA",
                                                  command=self.show_main_page)
        button_back_from_settings.pack(pady=20, anchor="center")

        # --- Süreli Ayar Frame'i (Ana Pencere İçinde) ---
        self.timed_options_frame = ctk.CTkFrame(self, fg_color="transparent")
        
        ctk.CTkLabel(master=self.timed_options_frame, text="Otomasyon Süresi ve Kapatma Ayarları", font=("Arial", 18, "bold")).pack(pady=(60, 10))
        
        ctk.CTkLabel(master=self.timed_options_frame, text="Otomasyon kaç saniye çalışsın?").pack(pady=5)
        self.duration_entry = ctk.CTkEntry(master=self.timed_options_frame, width=200)
        self.duration_entry.pack(pady=5)

        ctk.CTkLabel(master=self.timed_options_frame, text="Süre Bitince Ne Yapılsın?").pack(pady=10)
        self.choice_var = ctk.StringVar(value="stop_only")

        ctk.CTkRadioButton(master=self.timed_options_frame, text="Sadece İşlemleri Durdur", variable=self.choice_var, value="stop_only").pack(pady=5)
        ctk.CTkRadioButton(master=self.timed_options_frame, text="Minecraft'ı Kapat", variable=self.choice_var, value="game_only").pack(pady=5)
        ctk.CTkRadioButton(master=self.timed_options_frame, text="Minecraft ve Programı Kapat", variable=self.choice_var, value="game_and_app").pack(pady=5)

        self.start_button_timed = ctk.CTkButton(master=self.timed_options_frame, text="Başlat", corner_radius=25,
                                                   fg_color="#4E71FF", hover_color="#5000DA",
                                                   command=self.start_automation_from_timed_options)
        self.start_button_timed.pack(pady=20)
        
        button_back_from_timed = ctk.CTkButton(master=self.timed_options_frame, text="Geri", corner_radius=25,
                                               fg_color="#4E71FF", hover_color="#5000DA",
                                               command=self.show_main_page)
        button_back_from_timed.pack(pady=10, anchor="center")

        # --- Alt Menü Butonları (Her Zaman Görünür) ---
        self.bottom_buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_buttons_frame.pack(side="bottom", fill="x", pady=10, padx=20)

        stop_button = ctk.CTkButton(master=self.bottom_buttons_frame, text="Otomasyonu Durdur", corner_radius=25,
                                    fg_color="#CC0000", hover_color="#990000",
                                    command=self.stop_automation)
        stop_button.pack(side="left", padx=(0, 10))

        settings_button = ctk.CTkButton(master=self.bottom_buttons_frame, text="Ayarlar", corner_radius=25,
                                        fg_color="#7A7A7A", hover_color="#555555",
                                        command=self.show_settings_page)
        settings_button.pack(side="right", padx=(10, 0))

    def show_frame(self, frame):
        if self.current_frame:
            self.current_frame.pack_forget()
        frame.pack(expand=True, fill="both")
        self.current_frame = frame

    def show_main_page(self):
        self.show_frame(self.main_page_frame)
        self.center_window()

    def show_settings_page(self):
        self.show_frame(self.settings_page_frame)
        self.center_window()
    
    def show_timed_options(self, farm_type):
        self.current_farm_type_for_timed = farm_type
        self.show_frame(self.timed_options_frame)
        self.center_window()
        self.duration_entry.delete(0, ctk.END)
        self.choice_var.set("stop_only")

    def start_automation_from_timed_options(self):
        try:
            duration_str = self.duration_entry.get()
            if not duration_str.isdigit():
                print("Bilgi: Geçersiz süre girişi. Lütfen bir sayı girin.")
                return

            duration = int(duration_str)
            if duration <= 0:
                print("Uyarı: Süre pozitif bir sayı olmalı.")
                return

            selected_action = self.choice_var.get()
            self.show_main_page()
            self.start_automation(self.current_farm_type_for_timed, duration, selected_action)

        except ValueError:
            print("HATA: Süre için geçerli bir sayı girin.")
        except Exception as e:
            print(f"HATA: Süreli otomasyon başlatma sırasında beklenmedik bir hata oluştu: {e}")

    def start_automation(self, farm_type, duration=None, end_action=None, is_raid_farm=False):
        if self.is_automation_running:
            print("Uyarı: Otomasyon zaten çalışıyor.")
            return

        self.is_automation_running = True
        
        # Otomasyon döngüsünü başlatan ana thread
        if duration is None: # Süresiz mod
            self.automation_thread = threading.Thread(target=self._automation_loop_infinite, args=(farm_type, is_raid_farm))
        else: # Süreli mod
            self.automation_thread = threading.Thread(target=self._automation_loop_timed, args=(duration, end_action, farm_type, is_raid_farm))

        self.automation_thread.daemon = True
        self.automation_thread.start()

    def stop_automation(self):
        if self.is_automation_running:
            self.is_automation_running = False
            print("Otomasyon durduruluyor...")
        else:
            print("Uyarı: Zaten çalışan bir otomasyon yok.")

    def perform_automation_steps(self):
        pyautogui.click()

    def _minecraft_close_sequence(self):
        print("Oyun kapatılıyor...")
        time.sleep(0.5)

        pyautogui.press('esc')
        time.sleep(0.7)

        pyautogui.press('tab', presses=8, interval=0.05)
        time.sleep(0.2)

        pyautogui.press('enter')
        time.sleep(1.5)

        pyautogui.hotkey('alt', 'f4')
        time.sleep(0.1)

    def _raid_farm_startup_sequence(self):
        print("Raid Farmı başlangıç hazırlıkları yapılıyor...")
        
        # Alt+Tab ile oyuna geçiş
        pyautogui.hotkey('alt', 'tab')
        time.sleep(0.5) 
        
        # Esc ile menüyü kapatma
        pyautogui.press('esc') 
        time.sleep(0.3)

        # İksir alma: Slot 8'e geç (klavye 8 tuşu)
        pyautogui.press('8') 
        time.sleep(0.2) 

        # İksiri kullanma
        pyautogui.mouseDown(button='right') # Sağ tuşa basılı tut
        time.sleep(1.6) # İksirin içilmesi için yeterli bekleme süresi
        pyautogui.mouseUp(button='right')   # Sağ tuşu bırak

        # Kılıcı çekme:
        pyautogui.press('1') 
        time.sleep(0.2) 
        
        print("Raid Farmı hazırlıkları tamamlandı. Otomasyon başlıyor.")

    def _automation_loop_infinite(self, farm_type, is_raid_farm_mode):
        print(f"Farm Bot başlatılıyor: {farm_type}. Serbest Bırakın.")

        for i in range(5, 0, -1):
            print(i)
            time.sleep(1)

        if is_raid_farm_mode: 
            self._raid_farm_startup_sequence()
        else: 
            pyautogui.hotkey('alt', 'tab')
            time.sleep(0.3)
            pyautogui.press('esc')
        
        print(f"Süresiz otomasyon başlatıldı: {farm_type}.")
        current_delay = self.RAID_FARM_DELAY if "Raid Farm" in farm_type else self.ZOMBIE_FARM_DELAY

        while self.is_automation_running:
            try:
                self.perform_automation_steps()
                time.sleep(current_delay)
            except Exception as e:
                print(f"HATA: {farm_type} sırasında bir sorun oluştu: {e}")
                self.is_automation_running = False
                break
        print(f"Süresiz otomasyon durduruldu: {farm_type}.")

    def _automation_loop_timed(self, duration, end_action, farm_type, is_raid_farm_mode):
        print(f"Farm Bot {duration} saniye süreli otomasyon başlatılıyor: {farm_type}. Serbest Bırakın!")
        for i in range(5, 0, -1):
            print(i)
            time.sleep(1)

        if is_raid_farm_mode:
            self._raid_farm_startup_sequence()
        else:
            pyautogui.hotkey('alt', 'tab')
            time.sleep(0.3)
            pyautogui.press('esc')

        print(f"Süreli otomasyon başlatıldı: {farm_type}.")

        current_delay = self.RAID_FARM_DELAY if "Raid Farm" in farm_type else self.ZOMBIE_FARM_DELAY

        start_time = time.time()
        while self.is_automation_running and (time.time() - start_time) < duration:
            try:
                self.perform_automation_steps()
                time.sleep(current_delay)
            except Exception as e:
                print(f"HATA: {farm_type} sırasında bir sorun oluştu: {e}")
                self.is_automation_running = False
                break

        self.is_automation_running = False
        print(f"Süreli otomasyon tamamlandı: {farm_type}.")

        if end_action == "game_and_app":
            self._minecraft_close_sequence()
            print("Program kapatılıyor...")
            self.destroy()
            sys.exit()
        elif end_action == "game_only":
            self._minecraft_close_sequence()
        elif end_action == "stop_only":
            print("İşlemler durduruldu.")

    def center_window(self):
        self.update_idletasks()
        x = self.winfo_screenwidth() // 2 - self.winfo_width() // 2
        y = self.winfo_screenheight() // 2 - self.winfo_height() // 2
        self.geometry(f"+{x}+{y}")

if __name__ == "__main__":
    app = FarmBotApp()
    app.mainloop()
