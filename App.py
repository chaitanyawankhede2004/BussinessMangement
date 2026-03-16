import mysql.connector as myc
from mysql.connector import Error
from datetime import datetime

def get_connection():
    try:
        return myc.connect(
            host="localhost",
            user="root",
            password="password",
            database='GlobalBusinessDB',
            auth_plugin='mysql_native_password'
        )
    except Error as e:
        print(f"Connection Error: {e}")
        return None

def view_business_accounts():
    con = get_connection()
    if not con: return
    cur = con.cursor()
    print("\n" + "="*80)
    print(f"{'ID':<4} | {'BUSINESS NAME':<25} | {'REGION':<15} | {'CURRENCY':<8} | {'BUDGET':>15}")
    print("="*80)
    cur.execute("SELECT * FROM business_accounts")
    for r in cur:
        print(f"{r[0]:<4} | {r[1]:<25} | {r[2]:<15} | {r[3]:<8} | {r[4]:>15,.2f}")
    cur.close()
    con.close()

def log_expense():
    con = get_connection()
    if not con: return
    cur = con.cursor()
    
    view_business_accounts()
    try:
        acc_id = int(input("\nEnter Account ID to log expense for: "))
        category = input("Expense Category (e.g., Marketing, Payroll): ")
        amount = float(input("Amount: "))
        currency = input("Currency (3-letter code): ").upper()
        desc = input("Description: ")
        date = input("Date (YYYY-MM-DD) or press enter for today: ")
        
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')

        query = """
            INSERT INTO expenses (account_id, category, amount, currency, description, expense_date)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cur.execute(query, (acc_id, category, amount, currency, desc, date))
        con.commit()
        print("\n[SUCCESS] Expense logged successfully.")
    except ValueError:
        print("\n[ERROR] Invalid numerical input.")
    except Error as e:
        print(f"\n[ERROR] Database error: {e}")
    finally:
        cur.close()
        con.close()

def financial_summary():
    con = get_connection()
    if not con: return
    cur = con.cursor()
    
    print("\n" + "="*60)
    print("      GLOBAL EXPENDITURE SUMMARY")
    print("="*60)
    
    query = """
        SELECT b.business_name, b.base_currency, SUM(e.amount), b.total_budget
        FROM business_accounts b
        LEFT JOIN expenses e ON b.account_id = e.account_id
        GROUP BY b.account_id
    """
    cur.execute(query)
    results = cur.fetchall()
    
    for r in results:
        spent = r[2] if r[2] else 0.0
        remaining = float(r[3]) - float(spent)
        status = "HEALTHY" if remaining > 0 else "OVER BUDGET"
        
        print(f"\nBusiness: {r[0].upper()}")
        print(f"Total Spent: {spent:,.2f} {r[1]}")
        print(f"Remaining  : {remaining:,.2f} {r[1]}")
        print(f"Status     : {status}")
        print("-" * 30)
    
    cur.close()
    con.close()

def create_new_account():
    con = get_connection()
    if not con: return
    cur = con.cursor()
    print("\n--- Register New Global Entity ---")
    name = input("Business Name: ")
    region = input("Region (e.g., EMEA, LATAM): ")
    currency = input("Base Currency (e.g., USD, GBP): ").upper()
    try:
        budget = float(input("Allocated Budget: "))
        cur.execute("INSERT INTO business_accounts (business_name, region, base_currency, total_budget) VALUES (%s, %s, %s, %s)", 
                    (name, region, currency, budget))
        con.commit()
        print(f"\n[SUCCESS] {name} has been registered.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()
        con.close()

def menu():
    while True:
        print('\n' + '█'*45)
        print('   GLOBAL BUSINESS MANAGEMENT DASHBOARD')
        print('█'*45)
        print('1: View Active Business Accounts')
        print('2: Log New Expense (Multi-Currency)')
        print('3: Financial Summary & Budget Tracking')
        print('4: Register New Business Entity')
        print('5: Exit')
        
        choice = input('\nEnter Choice: ')
        
        if choice == '1': view_business_accounts()
        elif choice == '2': log_expense()
        elif choice == '3': financial_summary()
        elif choice == '4': create_new_account()
        elif choice == '5': break
        else: print("Invalid entry, try again.")

if __name__ == "__main__":
    menu()
