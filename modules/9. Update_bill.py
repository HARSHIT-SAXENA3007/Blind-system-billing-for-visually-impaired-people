import customtkinter as ctk
def update_bill_preview(order_items, total_price):
    bill_preview.delete("1.0", "end")  # Clear the previous bill preview
    bill_preview.insert("end", "Bill Preview:\n\n")
    bill_preview.insert("end", "Item\tQuantity\tPrice\n")
    bill_preview.insert("end", "-" * 30 + "\n")
    for item_name, quantity, price in order_items:
        bill_preview.insert("end", f"{item_name}\t{quantity}\t\t{price}\n")
    bill_preview.insert("end", "-" * 30 + "\n")
    bill_preview.insert("end", f"Total:\t\t\t{total_price}\n")
    
