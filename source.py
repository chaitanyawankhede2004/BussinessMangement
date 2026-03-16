import mysql.connector
from mysql.connector import Error

def setup_global_business_db():
    con = None
    try:
        # Connecting to MySQL server
        con = mysql.connector.connect(
            host="localhost",
            user='root',
            password='password',
            auth_plugin='mysql_native_password'
        )
        
        if con.is_connected():
            cur = con.cursor()
            cur.execute("CREATE DATABASE IF NOT EXISTS GlobalBusinessDB")
            cur.execute("USE GlobalBusinessDB")

            print("Resetting Global Business Database schema...")
            cur.execute("SET FOREIGN_KEY_CHECKS = 0")
            cur.execute("DROP TABLE IF EXISTS expenses")
            cur.execute("DROP TABLE IF EXISTS business_accounts")
            cur.execute("SET FOREIGN_KEY_CHECKS = 1")

            # 1. Table for Business Entities (Accounts)
            cur.execute("""
                CREATE TABLE business_accounts(
                    account_id INT AUTO_INCREMENT PRIMARY KEY,
                    business_name VARCHAR(150) NOT NULL,
                    region VARCHAR(50),
                    base_currency CHAR(3) DEFAULT 'USD',
                    total_budget DECIMAL(15, 2) DEFAULT 0.00
                )
            """)

            # 2. Table for Expenses
            cur.execute("""
                CREATE TABLE expenses(
                    expense_id INT AUTO_INCREMENT PRIMARY KEY,
                    account_id INT,
                    category VARCHAR(100),
                    amount DECIMAL(15, 2) NOT NULL,
                    currency CHAR(3),
                    description TEXT,
                    expense_date DATE,
                    FOREIGN KEY(account_id) REFERENCES business_accounts(account_id) ON DELETE CASCADE
                )
            """)

            # Seed initial Global Accounts
            business_data = [
                ('TechNova Solutions', 'North America', 'USD', 500000.00),
                ('EuroLogistics GmbH', 'Europe', 'EUR', 350000.00),
                ('Orient Trading Co.', 'Asia-Pacific', 'SGD', 200000.00),
                ('Andean Mining Group', 'South America', 'CLP', 1000000.00)
            ]
            
            cur.executemany("""
                INSERT INTO business_accounts(business_name, region, base_currency, total_budget) 
                VALUES (%s, %s, %s, %s)
            """, business_data)

            # Seed some initial expenses
            expense_data = [
                (1, 'Cloud Services', 12500.00, 'USD', 'AWS Monthly Billing', '2023-10-01'),
                (2, 'Warehouse Rent', 8000.00, 'EUR', 'Berlin Hub Rental', '2023-10-05'),
                (3, 'Logistics', 4500.00, 'SGD', 'Shipping Port Fees', '2023-10-10')
            ]

            cur.executemany("""
                INSERT INTO expenses(account_id, category, amount, currency, description, expense_date)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, expense_data)

            con.commit()
            print("Global Business Management System database ready.")
            
    except Error as e:
        print(f"Error: {e}")
    finally:
        if con and con.is_connected():
            con.close()

if __name__ == "__main__":
    setup_global_business_db()
