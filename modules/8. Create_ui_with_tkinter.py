import functools
import customtkinter as ctk
from tkinter import messagebox, simpledialog
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
