import os, subprocess, atexit, functools, psutil, pyttsx3, mysql.connector
from modules.listen_to_voice_input import listen
from modules.handle_voice_input import handle_voice_input
from modules.add_items import add_item_to_database
from modules.calculate_daily_sales import calculate_daily_sales
from modules.display_daily_sales import display_daily_sales
from modules.generate_bill import generate_pdf_bill
from modules.update_bill import update_bill_preview
from modules.create_ui_with_tkinter import root, bill_preview, status_label, voice_input_button, daily_sales_button, add_item_button, exit_button, generate_bill_button
from tkinter import simpledialog
from datetime import datetime
import pandas as pd

# --- Voice setup and DB setup ---
tts_engine = pyttsx3.init()
recognizer = sr.Recognizer()
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="abcdefgh",
    database="cafeteria"
)
cursor = db.cursor()

# --- Voice output ---
def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# --- Sales record ---
def record_sale(item_name, quantity, total_price):
    cursor.execute("INSERT INTO sales (item_id, quantity, total_price) VALUES ((SELECT item_id FROM items WHERE item_name = %s), %s, %s)", (item_name, quantity, total_price))
    db.commit()

# --- Fetch item price ---
def get_item_price(item_name):
    cursor.execute("SELECT price FROM items WHERE item_name = %s", (item_name,))
    result = cursor.fetchone()
    return result[0] if result else None

# --- Bill Generation UI Action ---
def generate_bill_button_action():
    global order_items, total_order_price
    if order_items:
        update_bill_preview(order_items, total_order_price)
        generate_pdf_bill(order_items, total_order_price)
        order_items = []
        total_order_price = 0
    else:
        speak("No order has been placed yet.")

# --- Helper UI Triggers ---
def trigger_voice_input(button, event): button.invoke()
def trigger_daily_sales(button, event): button.invoke()
def trigger_exit(button, event): button.invoke()

# --- Kill NVDA ---
def get_pid(name):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == name:
            return proc.pid
    return None

def kill_task(name):
    pid = get_pid(name)
    if pid:
        os.kill(pid, 9)
        print(f"Task '{name}' (PID: {pid}) has been killed.")
    else:
        print(f"Task '{name}' not found.")

def start_nvda_on_exit():
    os.startfile("C:/Program Files (x86)/NVDA/nvda.exe")

kill_task("nvda.exe")
atexit.register(start_nvda_on_exit)

# --- Bind UI Events ---
import tkinter as tk
root.bind('<space>', functools.partial(trigger_voice_input, voice_input_button))
root.bind('<f>', functools.partial(trigger_daily_sales, daily_sales_button))
root.bind('<j>', functools.partial(trigger_exit, exit_button))

# --- Replace generate_bill_button's command ---
generate_bill_button.configure(command=generate_bill_button_action)

# --- Start UI ---
root.mainloop()
