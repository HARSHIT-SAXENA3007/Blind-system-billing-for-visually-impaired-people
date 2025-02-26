from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
def generate_pdf_bill(order_items, total_price):
    # Create a list of data for the table
    data = [["Item", "Quantity", "Price"]]
    for item_name, quantity, price in order_items:
        data.append([item_name, str(quantity), str(price)])
    data.append(["", "", ""])
    data.append(["Total", "", str(total_price)])
