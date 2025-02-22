import pyautogui
import tkinter as tk
from tkinter import messagebox, simpledialog
import threading
import time

# Fail-safe özelliğini devre dışı bırak
pyautogui.FAILSAFE = False

class AutoClicker:
    def __init__(self, master):
        self.master = master
        self.master.title("Auto Clicker")
        self.master.geometry("300x150")

        # Başlat ve Durdur butonları
        self.start_button = tk.Button(self.master, text="Başlat", width=15, command=self.start_clicking)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(self.master, text="Durdur", width=15, command=self.stop_clicking)
        self.stop_button.pack(pady=10)
        self.stop_button.config(state=tk.DISABLED)

        # Durum değişkenleri
        self.is_clicking = False
        self.thread = None
        self.mouse_button = "left"  # Varsayılan sol fare tuşu

    def start_clicking(self):
        # Kullanıcıya tıklama süresi soruluyor
        duration = simpledialog.askinteger("Tıklama Süresi", "Kaç saniye tıklama yapılsın?", minvalue=1)
        if duration is None:
            return  # Kullanıcı iptal ederse devam etme

        # Kullanıcıya tıklama hızı soruluyor
        click_speed = simpledialog.askfloat("Tıklama Hızı", "Tıklama hızı (0.1x - 5x):", minvalue=0.1, maxvalue=5)
        if click_speed is None:
            return  # Kullanıcı iptal ederse devam etme

        # Sağ mı sol mu sorusu
        button_choice = simpledialog.askstring("Tuş Seçimi", "Sağ mı Sol mu tıklama yapılacak? (sağ/sol)")
        if button_choice is None or button_choice.lower() not in ["sağ", "sol"]:
            messagebox.showerror("Hata", "Geçersiz tuş seçimi!")
            return

        self.mouse_button = "right" if button_choice.lower() == "sağ" else "left"

        self.is_clicking = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        # Tıklama işlemini ayrı bir thread'de başlatıyoruz
        self.thread = threading.Thread(target=self.clicking, args=(duration, click_speed))
        self.thread.start()

    def stop_clicking(self):
        self.is_clicking = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def clicking(self, duration, click_speed):
        delay = 1 / click_speed  # Hız arttıkça, tıklama arasındaki süre azalacak
        start_time = time.time()

        while self.is_clicking and (time.time() - start_time) < duration:
            pyautogui.click(button=self.mouse_button)  # Hangi tuş kullanılacaksa onu seç
            time.sleep(delay)  # Tıklama hızıyla uyumlu süre

        self.is_clicking = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        messagebox.showinfo("Bilgi", f"{duration} saniye boyunca tıklama tamamlandı.")

# Ana pencereyi başlatıyoruz
if __name__ == '__main__':
    root = tk.Tk()
    app = AutoClicker(root)
    root.mainloop()
