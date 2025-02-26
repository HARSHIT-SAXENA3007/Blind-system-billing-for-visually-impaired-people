import speech_recognition as sr
import pyttsx3
import os
import mysql.connector
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
