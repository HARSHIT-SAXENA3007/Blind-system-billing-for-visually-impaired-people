# Blind-system-billing-for-visually-impaired-people
# Cafeteria Voice-Automated Billing System

This project is a voice-automated billing system designed for a cafeteria. It allows users to interact with the system through voice commands to order items, generate bills, and calculate daily sales. The system uses various Python libraries to handle speech recognition, text-to-speech, database operations, and generating PDF bills.

**Features**

1.**Voice Input**: Users can place orders using voice commands.
2.**Text-to-Speech**: The system provides spoken feedback to the user.
3.**Database Integration**: Items and sales are recorded in a MySQL database.
4.**Bill Generation**: Generates a PDF bill for the orders.
5.**Daily Sales Calculation**: Calculates and displays daily sales.
6.**CustomTkinter GUI**: A graphical user interface for user interaction.
7.**Accessibility**: Integrates with NVDA screen reader.

**Requirements**

- Python 3.x
- MySQL
- NVDA screen reader
- Python libraries: `speech_recognition`, `pyttsx3`, `mysql-connector-python`, `customtkinter`, `reportlab`, `pandas`, `openpyxl`, `AppOpener`, `psutil`, `subprocess`

## Installation

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/yourusername/cafeteria-billing-system.git
    cd cafeteria-billing-system
    ```

2. **Install Python Libraries**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Set Up MySQL Database**:
    - Create a MySQL database named `cafeteria`.
    - Create the necessary tables:
        ```sql
        CREATE TABLE items (
            item_id INT AUTO_INCREMENT PRIMARY KEY,
            item_name VARCHAR(255) NOT NULL,
            price DECIMAL(10, 2) NOT NULL
        );

        CREATE TABLE sales (
            sale_id INT AUTO_INCREMENT PRIMARY KEY,
            item_id INT,
            quantity INT NOT NULL,
            total_price DECIMAL(10, 2) NOT NULL,
            sale_date DATE DEFAULT (CURRENT_DATE),
            FOREIGN KEY (item_id) REFERENCES items(item_id)
        );
        ```

4. **Run the Application**:
    ```sh
    python main.py
    ```

**Usage**

1.**Start Voice Input**: Press the "Start Voice Input" button or press the space bar.
2.**Calculate Daily Sales**: Press the "Calculate Daily Sales" button or press the 'f' key.
3.**Add Item**: Press the "Add Item" button to add new items to the database.
4.**Generate Bill**: Press the "Generate Bill" button to generate a PDF bill for the current order.
5.**Exit**: Press the "Exit" button or press the 'j' key to exit the application.

**Notes**

- Ensure NVDA screen reader is installed and accessible at `C:/Program Files (x86)/NVDA/nvda.exe`.
- Modify the MySQL connection parameters in the script as needed.

**Acknowledgements**

- [NVDA Screen Reader](https://www.nvaccess.org/)
