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
