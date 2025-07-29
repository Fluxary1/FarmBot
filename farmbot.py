import customtkinter as ctk
import time
import pyautogui
import threading
import sys

pyautogui.PAUSE = 0.05

class FarmBotApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("450x700")
        self.title("FarmBot")
        ctk.set_appearance_mode("dark")
        self.resizable(False, False)

        self.is_automation_running = False
        self.automation_thread = None
        self.ZOMBIE_FARM_DELAY = 25
        self.RAID_FARM_DELAY = 2
        self.current_frame = None

        self.current_xp_farm_type_choice = None
        self.current_xp_farm_duration = None
        self.current_xp_farm_end_action = None

        self.create_widgets()

        self.show_main_page()

    def center_window(self):
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.geometry(f"+{x}+{y}")

    def create_widgets(self):
        self.remaining_time_label = ctk.CTkLabel(master=self, text="", font=("Arial", 16, "bold"), text_color="#00FF00")
        self.log_textbox = ctk.CTkTextbox(master=self, width=360, height=150, corner_radius=10,
                                          state="disabled", wrap="word", fg_color="#333333", text_color="#CCCCCC")
        self.remaining_time_label.pack(side="bottom", pady=(5, 0))
        self.log_textbox.pack(side="bottom", fill="x", padx=20, pady=(5, 10))

        self._configure_log_tags()

        self.main_page_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        self.settings_page_frame = ctk.CTkFrame(master=self, fg_color="transparent")

        self.xp_farm_type_selection_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        self.xp_farm_duration_input_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        self.xp_farm_end_action_selection_frame = ctk.CTkFrame(master=self, fg_color="transparent")

        self.create_main_page_widgets()
        self.create_settings_page_widgets()
        self._create_xp_farm_type_selection_widgets()
        self._create_xp_farm_duration_input_widgets()
        self._create_xp_farm_end_action_selection_widgets()

    def _configure_log_tags(self):
        self.log_textbox._textbox.tag_configure('info', foreground='#CCCCCC')
        self.log_textbox._textbox.tag_configure('warning', foreground='orange')
        self.log_textbox._textbox.tag_configure('error', foreground='red')

    def log_message(self, message, message_type='info'):
        self.log_textbox.configure(state="normal")
        timestamp = time.strftime("[%H:%M:%S]")
        full_message = f"{timestamp} {message}\n"
        self.log_textbox.insert(ctk.END, full_message, message_type)
        self.log_textbox.see("end")
        self.log_textbox.configure(state="disabled")

    def create_main_page_widgets(self):
        main_content_wrapper_frame = ctk.CTkFrame(master=self.main_page_frame, fg_color="transparent")
        main_content_wrapper_frame.pack(side="top", fill="both", expand=True, padx=0, pady=0)

        centered_content_frame = ctk.CTkFrame(master=main_content_wrapper_frame, fg_color="transparent")
        centered_content_frame.pack(expand=True, pady=30)

        ctk.CTkLabel(master=centered_content_frame, text="FARMBOT", font=("Arial", 24, "bold"), text_color="#EEEEEE").pack(pady=(0, 30))

        top_buttons_frame = ctk.CTkFrame(master=centered_content_frame, fg_color="transparent")
        top_buttons_frame.pack(pady=15)

        xp_farm_button = ctk.CTkButton(master=top_buttons_frame, text="XP FARM", corner_radius=10,
                                       fg_color="#444444", hover_color="#555555",
                                       command=self.show_xp_farm_type_selection)
        xp_farm_button.pack(side="left", padx=10)

        raid_farm_button = ctk.CTkButton(master=top_buttons_frame, text="RAID FARM", corner_radius=10,
                                         fg_color="#444444", hover_color="#555555",
                                         command=lambda: self.start_automation("RAID FARM Botu", duration=355, end_action="stop_only", is_raid_farm=True))
        raid_farm_button.pack(side="left", padx=10)

        bottom_buttons_frame = ctk.CTkFrame(master=centered_content_frame, fg_color="transparent")
        bottom_buttons_frame.pack(pady=15)

        stop_button = ctk.CTkButton(master=bottom_buttons_frame, text="STOP", corner_radius=10,
                                     fg_color="#900000", hover_color="#C20202",
                                     command=self.stop_automation)
        stop_button.pack(side="left", padx=10)

        settings_button = ctk.CTkButton(master=bottom_buttons_frame, text="SETTINGS", corner_radius=10,
                                         fg_color="#444444", hover_color="#555555",
                                         command=self.show_settings_page)
        settings_button.pack(side="left", padx=10)

    def _create_xp_farm_type_selection_widgets(self):
        frame = self.xp_farm_type_selection_frame
        xp_options_content_frame = ctk.CTkFrame(master=frame, fg_color="transparent")
        xp_options_content_frame.pack(expand=True, pady=20)

        ctk.CTkLabel(master=xp_options_content_frame, text="XP Farmı Tipi Seçimi", font=("Arial", 20, "bold")).pack(pady=(0, 20))

        self.xp_farm_choice_var = ctk.StringVar(value="infinite")

        ctk.CTkRadioButton(master=xp_options_content_frame, text="Süresiz Otomasyon", variable=self.xp_farm_choice_var, value="infinite").pack(pady=5)
        ctk.CTkRadioButton(master=xp_options_content_frame, text="Süreli Otomasyon", variable=self.xp_farm_choice_var, value="timed").pack(pady=5)

        next_button = ctk.CTkButton(master=xp_options_content_frame, text="İleri", corner_radius=25,
                                    fg_color="#4E71FF", hover_color="#5000DA",
                                    command=self._handle_xp_type_selection)
        next_button.pack(pady=25)

        back_button = ctk.CTkButton(master=xp_options_content_frame, text="Geri", corner_radius=25,
                                    fg_color="#7A7A7A", hover_color="#555555",
                                    command=self.show_main_page)
        back_button.pack(pady=15)

    def _handle_xp_type_selection(self):
        self.current_xp_farm_type_choice = self.xp_farm_choice_var.get()
        if self.current_xp_farm_type_choice == "timed":
            self.show_frame(self.xp_farm_duration_input_frame)
            self.xp_farm_duration_entry.delete(0, ctk.END)
            self.xp_farm_duration_entry.configure(state="normal")
        else:
            self.show_frame(self.xp_farm_end_action_selection_frame)
            self.current_xp_farm_duration = None
            self.xp_farm_end_action_var.set("stop_only")

    def _create_xp_farm_duration_input_widgets(self):
        frame = self.xp_farm_duration_input_frame
        duration_content_frame = ctk.CTkFrame(master=frame, fg_color="transparent")
        duration_content_frame.pack(expand=True, pady=20)

        ctk.CTkLabel(master=duration_content_frame, text="Otomasyon Süresi", font=("Arial", 20, "bold")).pack(pady=(0, 20))

        self.xp_farm_duration_label = ctk.CTkLabel(master=duration_content_frame, text="Otomasyon kaç saniye çalışsın?")
        self.xp_farm_duration_entry = ctk.CTkEntry(master=duration_content_frame, width=200)

        self.xp_farm_duration_label.pack(pady=(15, 5))
        self.xp_farm_duration_entry.pack(pady=5)

        next_button = ctk.CTkButton(master=duration_content_frame, text="İleri", corner_radius=25,
                                    fg_color="#4E71FF", hover_color="#5000DA",
                                    command=self._handle_xp_duration_input)
        next_button.pack(pady=25)

        back_button = ctk.CTkButton(master=duration_content_frame, text="Geri", corner_radius=25,
                                    fg_color="#7A7A7A", hover_color="#555555",
                                    command=lambda: self.show_frame(self.xp_farm_type_selection_frame))
        back_button.pack(pady=15)

    def _handle_xp_duration_input(self):
        try:
            duration_str = self.xp_farm_duration_entry.get()
            if not duration_str.isdigit() or int(duration_str) <= 0:
                self.log_message("Bilgi: Geçersiz süre girişi. Lütfen pozitif bir sayı girin.", message_type='warning')
                return
            self.current_xp_farm_duration = int(duration_str)
            self.show_frame(self.xp_farm_end_action_selection_frame)
            self.xp_farm_end_action_var.set("stop_only")
        except ValueError:
            self.log_message("HATA: Süre için geçerli bir sayı girin.", message_type='error')
        except Exception as e:
            self.log_message(f"HATA: Süre girişi sırasında beklenmedik bir hata oluştu: {e}", message_type='error')

    def _create_xp_farm_end_action_selection_widgets(self):
        frame = self.xp_farm_end_action_selection_frame
        end_action_content_frame = ctk.CTkFrame(master=frame, fg_color="transparent")
        end_action_content_frame.pack(expand=True, pady=20)

        ctk.CTkLabel(master=end_action_content_frame, text="Süre Bitince Ne Yapılsın?", font=("Arial", 20, "bold")).pack(pady=(0, 20))

        self.xp_farm_end_action_var = ctk.StringVar(value="stop_only")

        ctk.CTkRadioButton(master=end_action_content_frame, text="Sadece İşlemleri Durdur", variable=self.xp_farm_end_action_var, value="stop_only").pack(pady=5)
        ctk.CTkRadioButton(master=end_action_content_frame, text="Minecraft'ı Kapat", variable=self.xp_farm_end_action_var, value="game_only").pack(pady=5)
        ctk.CTkRadioButton(master=end_action_content_frame, text="Minecraft ve Programı Kapat", variable=self.xp_farm_end_action_var, value="game_and_app").pack(pady=5)

        start_button = ctk.CTkButton(master=end_action_content_frame, text="Başlat", corner_radius=25,
                                     fg_color="#4E71FF", hover_color="#5000DA",
                                     command=self._start_xp_farm_automation)
        start_button.pack(pady=25)

        back_button = ctk.CTkButton(master=end_action_content_frame, text="Geri", corner_radius=25,
                                    fg_color="#7A7A7A", hover_color="#555555",
                                    command=self._go_back_from_end_action)
        back_button.pack(pady=15)

    def _go_back_from_end_action(self):
        if self.current_xp_farm_type_choice == "timed":
            self.show_frame(self.xp_farm_duration_input_frame)
        else:
            self.show_frame(self.xp_farm_type_selection_frame)

    def _start_xp_farm_automation(self):
        self.current_xp_farm_end_action = self.xp_farm_end_action_var.get()
        farm_type = "Zombi Farm Botu"

        duration = None
        if self.current_xp_farm_type_choice == "timed":
            duration = self.current_xp_farm_duration

        self.show_main_page()
        self.start_automation(farm_type, duration, self.current_xp_farm_end_action, is_raid_farm=False)

    def create_settings_page_widgets(self):
        ctk.CTkLabel(master=self.settings_page_frame, text="Ayarlar", font=("Arial", 24, "bold")).pack(pady=20)
        ctk.CTkLabel(master=self.settings_page_frame, text="Buraya ileride gecikme ayarları, tuş atamaları vb. eklenecek.").pack(pady=10)

        button_back_from_settings = ctk.CTkButton(master=self.settings_page_frame, text="Geri", corner_radius=25,
                                                  fg_color="#4E71FF", hover_color="#5000DA",
                                                  command=self.show_main_page)
        button_back_from_settings.pack(pady=20, anchor="center")

    def show_frame(self, frame):
        if self.current_frame:
            self.current_frame.pack_forget()
        frame.pack(expand=True, fill="both")
        self.current_frame = frame
        self.center_window()

    def show_main_page(self):
        self.show_frame(self.main_page_frame)
        self.remaining_time_label.configure(text="")
        self.current_xp_farm_type_choice = None
        self.current_xp_farm_duration = None
        self.current_xp_farm_end_action = None

    def show_xp_farm_type_selection(self):
        self.xp_farm_choice_var.set("infinite")
        self.xp_farm_duration_entry.delete(0, ctk.END)
        self.xp_farm_duration_entry.configure(state="disabled")
        self.xp_farm_end_action_var.set("stop_only")
        self.show_frame(self.xp_farm_type_selection_frame)

    def show_settings_page(self):
        self.show_frame(self.settings_page_frame)

    def start_automation(self, farm_type, duration=None, end_action=None, is_raid_farm=False):
        if self.is_automation_running:
            self.log_message("Uyarı: Otomasyon zaten çalışıyor.", message_type='warning')
            return

        self.is_automation_running = True
        self.log_message(f"Otomasyon başlatılıyor: {farm_type}.")

        if duration is None:
            self.automation_thread = threading.Thread(target=self._automation_loop_infinite, args=(farm_type, is_raid_farm))
        else:
            self.automation_thread = threading.Thread(target=self._automation_loop_timed, args=(duration, end_action, farm_type, is_raid_farm))

        self.automation_thread.daemon = True
        self.automation_thread.start()

    def stop_automation(self):
        if self.is_automation_running:
            self.is_automation_running = False
            self.log_message("Otomasyon durduruluyor...", message_type='warning')
            self.remaining_time_label.configure(text="")
        else:
            self.log_message("Uyarı: Zaten çalışan bir otomasyon yok.", message_type='warning')

    def perform_automation_steps(self):
        pyautogui.click()

    def _minecraft_close_sequence(self):
        self.log_message("Oyun kapatılıyor...", message_type='info')
        time.sleep(0.5)
        pyautogui.press('esc')
        time.sleep(0.7)
        pyautogui.press('tab', presses=8, interval=0.05)
        time.sleep(0.2)
        pyautogui.press('enter')
        time.sleep(1.5)
        pyautogui.hotkey('alt', 'f4')
        time.sleep(0.1)
        self.log_message("Oyun kapatıldı.", message_type='info')

    def _raid_farm_startup_sequence(self):
        self.log_message("Raid Farmı başlangıç hazırlıkları yapılıyor...", message_type='info')
        pyautogui.hotkey('alt', 'tab')
        time.sleep(0.5)
        pyautogui.press('esc')
        time.sleep(0.3)
        self.log_message("İksir slotuna geçiliyor (Slot 8)...", message_type='info')
        pyautogui.press('8')
        time.sleep(0.2)
        pyautogui.mouseDown(button='right')
        time.sleep(1.6)
        pyautogui.mouseUp(button='right')
        self.log_message("Kılıç slotuna geçiliyor (Slot 1)...", message_type='info')
        pyautogui.press('1')
        time.sleep(0.2)
        self.log_message("Raid Farmı hazırlıkları tamamlandı. Otomasyon başlıyor!", message_type='info')

    def _automation_loop_infinite(self, farm_type, is_raid_farm_mode):
        self.log_message(f"Farm Bot başlatılıyor: {farm_type}. Serbest Bırakın!", message_type='info')
        for i in range(5, 0, -1):
            self.log_message(f"Başlangıca {i} saniye kaldı...", message_type='info')
            time.sleep(1)

        if is_raid_farm_mode:
            self._raid_farm_startup_sequence()
        else:
            pyautogui.hotkey('alt', 'tab')
            time.sleep(0.3)
            pyautogui.press('esc')
            self.log_message("Oyun ekranına geçildi.", message_type='info')

        self.log_message(f"Süresiz otomasyon aktif: {farm_type}.", message_type='info')
        current_delay = self.RAID_FARM_DELAY if "Raid Farm" in farm_type else self.ZOMBIE_FARM_DELAY

        while self.is_automation_running:
            try:
                self.perform_automation_steps()
                time.sleep(current_delay)
            except Exception as e:
                self.log_message(f"HATA: {farm_type} sırasında bir sorun oluştu: {e}", message_type='error')
                self.is_automation_running = False
                break
        self.log_message(f"Süresiz otomasyon durduruldu: {farm_type}.", message_type='warning')
        self.remaining_time_label.configure(text="")

    def _automation_loop_timed(self, duration, end_action, farm_type, is_raid_farm_mode):
        self.log_message(f"Farm Bot {duration} saniye süreli otomasyon başlatılıyor: {farm_type}. Serbest Bırakın!", message_type='info')
        for i in range(5, 0, -1):
            self.log_message(f"Başlangıca {i} saniye kaldı...", message_type='info')
            time.sleep(1)

        if is_raid_farm_mode:
            self._raid_farm_startup_sequence()
        else:
            pyautogui.hotkey('alt', 'tab')
            time.sleep(0.3)
            pyautogui.press('esc')
            self.log_message("Oyun ekranına geçildi.", message_type='info')

        self.log_message(f"Süreli otomasyon aktif: {farm_type}.", message_type='info')

        current_delay = self.RAID_FARM_DELAY if "Raid Farm" in farm_type else self.ZOMBIE_FARM_DELAY

        start_time = time.time()
        elapsed_time = 0
        while self.is_automation_running and elapsed_time < duration:
            try:
                self.perform_automation_steps()
                time.sleep(current_delay)
                elapsed_time = time.time() - start_time
                remaining_time = max(0, duration - int(elapsed_time))

                self.remaining_time_label.configure(text=f"Kalan Süre: {remaining_time} sn")

                if remaining_time % 30 == 0 and remaining_time > 0 or (remaining_time <= 10 and remaining_time > 0 and (int(elapsed_time) % 1 == 0)):
                     self.log_message(f"Kalan süre: {remaining_time} saniye.", message_type='info')
                elif remaining_time == 0:
                     self.log_message("Süre doldu. Otomasyon durduruluyor...", message_type='warning')

            except Exception as e:
                self.log_message(f"HATA: {farm_type} sırasında bir sorun oluştu: {e}", message_type='error')
                self.is_automation_running = False
                break

        self.is_automation_running = False
        self.log_message(f"Süreli otomasyon tamamlandı: {farm_type}.", message_type='warning')
        self.remaining_time_label.configure(text="")

        if end_action == "game_and_app":
            self.log_message("Program kapatılıyor...", message_type='info')
            self._minecraft_close_sequence()
            self.after(2000, self.destroy)
        elif end_action == "game_only":
            self._minecraft_close_sequence()
        elif end_action == "stop_only":
            self.log_message("İşlemler durduruldu.", message_type='info')

if __name__  == "__main__":
    app = FarmBotApp()
    app.mainloop()
