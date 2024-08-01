import speech_recognition as sr
import os
import functools
import pyttsx3
import mysql.connector
import customtkinter as ctk
from tkinter import messagebox, simpledialog
from datetime import datetime
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
import openpyxl
from openpyxl.utils import get_column_letter
from AppOpener import close, open
import psutil
import subprocess
import atexit

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

def run_task(name):
    subprocess.Popen(name)
    print(f"Task '{name}' has been started.")

kill_task("nvda.exe")

# Initialize recognizer and TTS engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="abcdefgh",
    database="cafeteria"
)
cursor = db.cursor()

# Function to speak text
def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Function to listen to voice input
def listen():
    with sr.Microphone() as source:
        status_label.configure(text="Listening...")
        speak("speak now")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            status_label.configure(text=f"User said: {command}")
            print(f"User said: {command}")
            return command
        except sr.UnknownValueError:
            status_label.configure(text="Sorry, I did not understand that.")
            speak("Sorry, I did not understand that.")
            return None

# Function to get item price from database
def get_item_price(item_name):
    cursor.execute("SELECT price FROM items WHERE item_name = %s", (item_name,))
    result = cursor.fetchone()
    return result[0] if result else None

# Function to start nvda on exit 
def start_nvda_on_exit():
    os.startfile("C:/Program Files (x86)/NVDA/nvda.exe")

# Function to record sale in database
def record_sale(item_name, quantity, total_price):
    cursor.execute("INSERT INTO sales (item_id, quantity, total_price) VALUES ((SELECT item_id FROM items WHERE item_name = %s), %s, %s)", (item_name, quantity, total_price))
    db.commit()

# Function to calculate daily sales
def calculate_daily_sales():
    today = datetime.today().date()
    cursor.execute("""
        SELECT i.item_name, SUM(s.quantity) AS total_quantity, SUM(s.quantity * i.price) AS total_sales
        FROM sales s
        JOIN items i ON s.item_id = i.item_id
        WHERE s.sale_date = %s
        GROUP BY i.item_name
    """, (today,))
    sales_data = cursor.fetchall()
    total_sales = sum(row[2] for row in sales_data)
    return sales_data, total_sales

# Function to generate PDF bill
def generate_pdf_bill(order_items, total_price):
    # Create a list of data for the table
    data = [["Item", "Quantity", "Price"]]
    for item_name, quantity, price in order_items:
        data.append([item_name, str(quantity), str(price)])
    data.append(["", "", ""])
    data.append(["Total", "", str(total_price)])

    # Create a PDF document
    doc = SimpleDocTemplate("bill.pdf", pagesize=letter)
    elements = []

    # Create a table from the data
    table = Table(data)
    style = TableStyle([('BACKGROUND', (0,0), (-1,0), colors.grey),
                        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0,0), (-1,0), 12),
                        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
                        ('GRID', (0,0), (-1,-1), 1, colors.black)])
    table.setStyle(style)
    elements.append(table)

    # Build the PDF document
    doc.build(elements)
    speak(f"PDF bill generated for your order with a total price of {total_price} rupees.")

    # Open the generated PDF file
    os.startfile("bill.pdf")

# Function to handle voice input
def handle_voice_input():
    global order_items, total_order_price
    speak("The system is now active. Please say the item name and quantity to make a purchase, or say 'generate bill' to generate the bill.")
    order_items = []
    total_order_price = 0
    while True:
        command = listen()
        if command:
            if command.lower() == "generate bill":
                if order_items:
                    update_bill_preview(order_items, total_order_price)
                    generate_pdf_bill(order_items, total_order_price)
                    order_items = []
                    total_order_price = 0
                    speak("Bill generated successfully.")
                else:
                    speak("No order has been placed yet.")
                break
            elif command.lower() in ["stop", "no"]:
                if order_items:
                    speak(f"The total price for your order is {total_order_price} rupees.")
                break
            try:
                items = command.split()  
                item_name = ' '.join(items[:-1])
                quantity = int(items[-1])
                price = get_item_price(item_name)
                if price:
                    item_total_price = price * quantity
                    total_order_price += item_total_price
                    order_items.append((item_name, quantity, item_total_price))
                    record_sale(item_name, quantity, item_total_price)
                    speak(f"Added {quantity} {item_name}(s) to the order.")
                    update_bill_preview(order_items, total_order_price)
                else:
                    speak(f"Item {item_name} not found.")
                speak(f"The current total price for your order is {total_order_price} rupees.")
                speak("Do you want to add anything else or generate bill?")
            except ValueError:
                speak("Please provide both item names and quantities correctly.")

def add_item_to_database():
    item_name = simpledialog.askstring("Add Item", "Enter the item name:")
    if item_name:
        item_price = simpledialog.askfloat("Add Item", "Enter the item price:")
        if item_price:
            try:
                cursor.execute("INSERT INTO items (item_name, price) VALUES (%s, %s)", (item_name, item_price))
                db.commit()
                speak(f"Item '{item_name}' with price {item_price} has been added to the database.")
            except mysql.connector.Error as error:
                speak(f"Error adding item to the database: {error}")

def trigger_voice_input(button, event):
    button.invoke()

def generate_bill_button():
    global order_items, total_order_price
    if order_items:
        update_bill_preview(order_items, total_order_price)
        generate_pdf_bill(order_items, total_order_price)
        order_items = []
        total_order_price = 0
    else:
        speak("No order has been placed yet.")

# Function to display daily sales
def display_daily_sales():
    sales_data, total_sales = calculate_daily_sales()
    if sales_data:
        # Create a DataFrame from the sales data
        df = pd.DataFrame(sales_data, columns=['Item', 'Total Quantity', 'Total Sales'])

        # Add the total sales row to the DataFrame
        total_sales_row = pd.Series({'Item': 'Total Sales', 'Total Quantity': df['Total Quantity'].sum(), 'Total Sales': total_sales})
        df.loc[len(df)] = total_sales_row

        # Save the DataFrame to an Excel file
        today = datetime.today().date()
        file_name = f'sales_report_{today.strftime("%d-%m-%Y")}.xlsx'
        df.to_excel(file_name, index=False, header=True)

        speak(f"Total sales for {today.strftime('%d-%m-%Y')} is {total_sales} rupees.")

        # Open the generated Excel file
        os.startfile(file_name)
    else:
        speak("No sales data available for today.")
        

def update_bill_preview(order_items, total_price):
    bill_preview.delete("1.0", "end")  # Clear the previous bill preview
    bill_preview.insert("end", "Bill Preview:\n\n")
    bill_preview.insert("end", "Item\tQuantity\tPrice\n")
    bill_preview.insert("end", "-" * 30 + "\n")
    for item_name, quantity, price in order_items:
        bill_preview.insert("end", f"{item_name}\t{quantity}\t\t{price}\n")
    bill_preview.insert("end", "-" * 30 + "\n")
    bill_preview.insert("end", f"Total:\t\t\t{total_price}\n")
    
def trigger_daily_sales(button, event):
    button.invoke()

def trigger_exit(button, event):
    button.invoke()

# Create the main window
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.title("Cafeteria Billing System")
root.geometry("600x400")
root.configure(bg="black")

# Create a frame for side buttons
side_frame = ctk.CTkFrame(root, width=150)
side_frame.pack(side="left", fill="y", padx=10, pady=10)

# Create a frame for the bill preview and "Generate Bill" button
right_frame = ctk.CTkFrame(root)
right_frame.pack(side="right", fill="both", padx=10, pady=10, expand=True)

# Create a Text widget for the bill preview
bill_preview = ctk.CTkTextbox(right_frame, width=300, height=300)
bill_preview.pack(pady=10)

# Create a label for displaying "Listening..." and "User said:"
status_label = ctk.CTkLabel(root, text="", font=("Arial", 12))
status_label.pack(pady=10)

# Create buttons and add them to the side frame
voice_input_button = ctk.CTkButton(side_frame, text="Start Voice Input", command=handle_voice_input, font=("Arial", 12), fg_color="white", text_color="black")
voice_input_button.pack(pady=10)
root.bind('<space>', functools.partial(trigger_voice_input, voice_input_button))

daily_sales_button = ctk.CTkButton(side_frame, text="Calculate Daily Sales", command=display_daily_sales, font=("Arial", 12), fg_color="white", text_color="black")
daily_sales_button.pack(pady=10)
root.bind('<f>', functools.partial(trigger_daily_sales, daily_sales_button))

root.bind('<f>', functools.partial(trigger_daily_sales, daily_sales_button))
add_item_button = ctk.CTkButton(side_frame, text="Add Item", command=add_item_to_database, font=("Arial", 12), fg_color="white", text_color="black")
add_item_button.pack(pady=10)

exit_button = ctk.CTkButton(side_frame, text="Exit", command=root.quit, font=("Arial", 12), fg_color="white", text_color="black")
exit_button.pack(pady=10)
root.bind('<j>', functools.partial(trigger_exit, exit_button) )

# Create the "Generate Bill" button 
generate_bill_button = ctk.CTkButton(right_frame, text="Generate Bill", command=generate_bill_button, font=("Arial", 12), fg_color="white", text_color="black")
generate_bill_button.pack(pady=10)

atexit.register(start_nvda_on_exit)
# Run the main loop
root.mainloop()
