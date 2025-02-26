import mysql.connector
import speech_recognition as sr
import pyttsx3
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
