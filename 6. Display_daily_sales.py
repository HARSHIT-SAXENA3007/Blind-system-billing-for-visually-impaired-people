import os
import pandas as pd
import datetime
import pyttsx3
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
