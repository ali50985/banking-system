import sqlite3
import random
import hashlib
import re

# Create or connect to the database
def create_db():
    conn = sqlite3.connect('banking_system.db')
    cursor = conn.cursor()

    # Create users table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        account_number INTEGER UNIQUE,
        dob TEXT,
        city TEXT,
        password TEXT,
        balance REAL,  -- Ensure balance is stored as REAL (float)
        contact_number TEXT,
        email TEXT,
        address TEXT
    );
    ''')

    # Create login table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS login (
        account_number INTEGER,
        password TEXT,
        is_active BOOLEAN,
        FOREIGN KEY(account_number) REFERENCES users(account_number)
    );
    ''')

    # Rename the table 'transaction' to 'user_transactions'
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_transactions (
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_number INTEGER,
        transaction_type TEXT,
        amount REAL,
        balance REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(account_number) REFERENCES users(account_number)
    );
    ''')

    conn.commit()
    conn.close()

# Hash password for security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Validate email format
def validate_email(email):
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    return re.match(regex, email) is not None

# Validate contact number (10 digits)
def validate_contact_number(contact_number):
    return contact_number.isdigit() and len(contact_number) == 10

# Add user function
def add_user():
    conn = sqlite3.connect('banking_system.db')
    cursor = conn.cursor()

    # User input
    name = input("Enter your name: ")
    account_number = random.randint(1000000000, 9999999999)  # Generate a 10-digit random number
    dob = input("Enter your date of birth (DD/MM/YYYY): ")
    city = input("Enter your city: ")

    # Password input with validation
    password = input("Enter a password: ")
    password = hash_password(password)  # Hash the password

    # Balance input (minimum 2000)
    balance = float(input("Enter an initial balance (minimum 2000): "))
    while balance < 2000:
        print("Initial balance must be at least 2000!")
        balance = float(input("Enter an initial balance (minimum 2000): "))

    # Validate contact number
    contact_number = input("Enter your contact number: ")
    while not validate_contact_number(contact_number):
        print("Invalid contact number. Please enter a 10-digit number.")
        contact_number = input("Enter your contact number: ")

    # Validate email
    email = input("Enter your email: ")
    while not validate_email(email):
        print("Invalid email. Please enter a valid email address.")
        email = input("Enter your email: ")

    address = input("Enter your address: ")

    # Insert into users table
    cursor.execute('''
    INSERT INTO users (name, account_number, dob, city, password, balance, contact_number, email, address)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, account_number, dob, city, password, balance, contact_number, email, address))

    # Insert into login table with active status
    cursor.execute('''
    INSERT INTO login (account_number, password, is_active)
    VALUES (?, ?, ?)
    ''', (account_number, password, True))

    conn.commit()
    print(f"User created successfully! Your account number is {account_number}")
    conn.close()

# Show all users
def show_users():
    conn = sqlite3.connect('banking_system.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()

    for user in users:
        print(f"Name: {user[1]}, Account Number: {user[2]}, Balance: {user[6]:.2f}, Active: {user[7]}")

    conn.close()

# Login function
def login():
    conn = sqlite3.connect('banking_system.db')
    cursor = conn.cursor()

    account_number = int(input("Enter account number: "))
    password = input("Enter password: ")
    password = hash_password(password)

    cursor.execute('SELECT * FROM login WHERE account_number = ? AND password = ?', (account_number, password))
    user = cursor.fetchone()

    if user:
        print("Login successful!")
        print(f"Welcome {user[1]}!")
        display_balance(account_number)
        # Further actions like transaction, deactivation, etc. can be added here
    else:
        print("Invalid account number or password.")
    conn.close()

# Display balance for logged-in user
def display_balance(account_number):
    conn = sqlite3.connect('banking_system.db')
    cursor = conn.cursor()

    cursor.execute('SELECT balance FROM users WHERE account_number = ?', (account_number,))
    balance = cursor.fetchone()

    if balance:
        print(f"Your current balance is: {balance[0]:.2f}")
    else:
        print("Account not found.")

    conn.close()

# Main function
def main():
    create_db()
    
    while True:
        print("\n1. Add User")
        print("2. Show Users")
        print("3. Login")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_user()
        elif choice == '2':
            show_users()
        elif choice == '3':
            login()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
