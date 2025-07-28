import time
import pyautogui
import customtkinter as ctk
import threading
import sys 

pyautogui.PAUSE = 0.05 

app = ctk.CTk()
app.geometry("500x400")
app.title("Farm Bot")
ctk.set_appearance_mode("dark")

button_frame = ctk.CTkFrame(master=app, fg_color="transparent")
button_frame.pack(expand=True, anchor="center")

BUTTON_NORMAL_COLOR = "#4E71FF"
BUTTON_HOVER_EFFECT_COLOR = "#5000DA"

is_automation_running = False
automation_thread = None

FARM_CYCLE_DELAY = 25 

def perform_automation_steps():
    pyautogui.click() 

def _minecraft_close_sequence():
    print("Oyun kapatılıyor...")
    # Toplam bekleme süresi 3 saniyeyi aşmayacak şekilde ayarlandı
    time.sleep(0.5) # Başlamadan önce kısa bir bekleme

    pyautogui.press('esc')
    time.sleep(0.7) # Menünün açılması için bekleme

    pyautogui.press('tab', presses=8, interval=0.05) 
    time.sleep(0.2) # Tab basıldıktan sonra seçenek odaklanması için bekleme

    pyautogui.press('enter')
    time.sleep(1.5) # Oyundan çıkış ve başlık ekranına dönme süresi (bu en kritik süre)

    pyautogui.hotkey('alt', 'f4')
    time.sleep(0.1) # Alt+F4 komutu sonrası çok kısa bekleme

def _automation_loop_infinite():
    global is_automation_running 
    print("Farm Bot başlatılıyor. Serbest Bırakın!")
    for i in range(5, 0, -1):
        print(i)
        time.sleep(1)
    
    pyautogui.hotkey('alt', 'tab')
    time.sleep(0.3)
    pyautogui.press('esc')
    
    print("Süresiz otomasyon başlatıldı.")
    while is_automation_running:
        try:
            perform_automation_steps()
            time.sleep(FARM_CYCLE_DELAY) 
        except Exception as e:
            print(f"HATA: Süresiz otomasyon sırasında bir sorun oluştu: {e}")
            is_automation_running = False
            break
    print("Süresiz otomasyon durduruldu.")

def _automation_loop_timed(duration, end_action):
    global is_automation_running 
    print(f"Farm Bot {duration} saniye süreli otomasyon başlatılıyor. Serbest Bırakın!")
    for i in range(5, 0, -1):
        print(i)
        time.sleep(1)

    pyautogui.hotkey('alt', 'tab')
    time.sleep(0.3)
    pyautogui.press('esc')

    print(f"Süreli otomasyon başlatıldı.") 
    
    start_time = time.time()
    while is_automation_running and (time.time() - start_time) < duration:
        try:
            perform_automation_steps()
            time.sleep(FARM_CYCLE_DELAY) 
        except Exception as e:
            print(f"HATA: Süreli otomasyon sırasında bir sorun oluştu: {e}")
            is_automation_running = False
            break
    
    is_automation_running = False
    print(f"Süreli otomasyon tamamlandı.") 

    if end_action == "game_and_app":
        _minecraft_close_sequence()
        print("Program kapatılıyor...") 
        app.destroy() 
        sys.exit() 
    elif end_action == "game_only":
        _minecraft_close_sequence()
    elif end_action == "stop_only":
        print("İşlemler durduruldu.") 

def start_infinite_automation():
    global is_automation_running, automation_thread 
    if is_automation_running:
        print("Uyarı: Otomasyon zaten çalışıyor.")
        return

    is_automation_running = True
    automation_thread = threading.Thread(target=_automation_loop_infinite)
    automation_thread.daemon = True
    automation_thread.start()

def start_timed_automation_prompt():
    global is_automation_running, automation_thread 
    if is_automation_running:
        print("Uyarı: Otomasyon zaten çalışıyor.")
        return

    try:
        duration_str = ctk.CTkInputDialog(text="Otomasyon kaç saniye çalışsın?", title="Süre Ayarı").get_input()
        if duration_str is None or not duration_str.isdigit():
            print("Bilgi: Geçersiz süre girişi veya işlem iptal edildi.")
            return

        duration = int(duration_str)
        if duration <= 0:
            print("Uyarı: Süre pozitif bir sayı olmalı.")
            return

        action_window = ctk.CTkToplevel(app)
        action_window.geometry("300x200")
        action_window.title("Süre Bitince Ne Olsun?")
        action_window.transient(app) 
        action_window.grab_set() 

        choice_var = ctk.StringVar(value="stop_only") 

        ctk.CTkLabel(action_window, text="Süre Bitince Ne Yapılsın?").pack(pady=10)

        radio_stop = ctk.CTkRadioButton(action_window, text="Sadece İşlemleri Durdur", variable=choice_var, value="stop_only")
        radio_stop.pack(pady=5)

        radio_game = ctk.CTkRadioButton(action_window, text="Minecraft'ı Kapat", variable=choice_var, value="game_only")
        radio_game.pack(pady=5)

        radio_both = ctk.CTkRadioButton(action_window, text="Minecraft ve Programı Kapat", variable=choice_var, value="game_and_app")
        radio_both.pack(pady=5)

        def start_with_action():
            global is_automation_running, automation_thread 
            selected_action = choice_var.get()
            action_window.destroy() 

            is_automation_running = True
            automation_thread = threading.Thread(target=_automation_loop_timed, args=(duration, selected_action))
            automation_thread.daemon = True
            automation_thread.start()

        ctk.CTkButton(action_window, text="Başlat", command=start_with_action).pack(pady=10)

        action_window.update_idletasks()
        x_action = app.winfo_x() + app.winfo_width() // 2 - action_window.winfo_width() // 2
        y_action = app.winfo_y() + app.winfo_height() // 2 - action_window.winfo_height() // 2
        action_window.geometry(f"+{x_action}+{y_action}")
        
        app.wait_window(action_window) 

    except ValueError:
        print("HATA: Süre için geçerli bir sayı girin.")
    except Exception as e:
        print(f"HATA: Süreli otomasyon başlatma sırasında beklenmedik bir hata oluştu: {e}")

def stop_automation():
    global is_automation_running, automation_thread 
    if is_automation_running:
        is_automation_running = False
    else:
        print("Uyarı: Zaten çalışan bir otomasyon yok.")

button1 = ctk.CTkButton(master=button_frame, text="Süresiz Aç", corner_radius=25,
                        fg_color=BUTTON_NORMAL_COLOR,
                        hover_color=BUTTON_HOVER_EFFECT_COLOR,
                        command=start_infinite_automation)
button1.pack(pady=5, anchor="center")

button2 = ctk.CTkButton(master=button_frame, text="Süreyi Ayarla", corner_radius=25,
                        fg_color=BUTTON_NORMAL_COLOR,
                        hover_color=BUTTON_HOVER_EFFECT_COLOR,
                        command=start_timed_automation_prompt)
button2.pack(pady=5, anchor="center")

stop_button = ctk.CTkButton(master=button_frame, text="Otomasyonu Durdur", corner_radius=25,
                             fg_color="#CC0000", hover_color="#990000",
                             command=stop_automation)
stop_button.pack(pady=5, anchor="center")

app.update_idletasks()
x = app.winfo_screenwidth() // 2 - app.winfo_width() // 2
y = app.winfo_screenheight() // 2 - app.winfo_height() // 2
app.geometry(f"+{x}+{y}")

app.mainloop()