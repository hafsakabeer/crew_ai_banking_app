"""
models/database.py - SQLite Database Setup and Connection Management
"""

import sqlite3
import os
from datetime import datetime, timedelta

DB_PATH = "bank_data.db"

def get_connection(db_path=DB_PATH):
    """Returns a SQLite database connection."""
    return sqlite3.connect(db_path)

def init_database(db_path=DB_PATH):
    """
    Initializes the SQLite database with mock banking tables and populates seed data.
    Hardcoded for dummy user_id: 'USER101'
    """
    conn = get_connection(db_path)
    cursor = conn.cursor()

    # 1. Accounts Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        account_id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        account_type TEXT NOT NULL,
        balance REAL NOT NULL,
        currency TEXT NOT NULL,
        status TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)

    # 2. Transactions Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        transaction_id TEXT PRIMARY KEY,
        account_id TEXT NOT NULL,
        date TEXT NOT NULL,
        amount REAL NOT NULL,
        transaction_type TEXT NOT NULL,
        category TEXT NOT NULL,
        description TEXT NOT NULL,
        FOREIGN KEY (account_id) REFERENCES accounts (account_id)
    )
    """)

    # 3. Service Requests Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS service_requests (
        request_id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        account_id TEXT NOT NULL,
        request_type TEXT NOT NULL,
        status TEXT NOT NULL,
        details TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (account_id) REFERENCES accounts (account_id)
    )
    """)

    # Check if data already exists to prevent duplicate insertion
    cursor.execute("SELECT COUNT(*) FROM accounts")
    if cursor.fetchone()[0] == 0:
        print("[Database Setup] Seeding database with initial dummy data...")

        # Seed Accounts for USER101
        accounts = [
            ("ACC1001", "USER101", "Premium Savings Account", 12450.75, "USD", "ACTIVE", "2024-01-15"),
            ("ACC1002", "USER101", "Checking Account", 3210.50, "USD", "ACTIVE", "2024-02-01"),
        ]
        cursor.executemany("INSERT INTO accounts VALUES (?, ?, ?, ?, ?, ?, ?)", accounts)

        # Seed Transactions for ACC1001 & ACC1002
        today = datetime.now()
        transactions = [
            ("TXN9001", "ACC1001", (today - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"), 2500.00, "CREDIT", "Salary", "Monthly Salary Deposit from Acme Corp"),
            ("TXN9002", "ACC1001", (today - timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S"), -85.50, "DEBIT", "Dining & Groceries", "Trader Joe's Supermarket"),
            ("TXN9003", "ACC1001", (today - timedelta(days=4)).strftime("%Y-%m-%d %H:%M:%S"), -120.00, "DEBIT", "Utilities", "City Power & Light Electric Bill"),
            ("TXN9004", "ACC1001", (today - timedelta(days=6)).strftime("%Y-%m-%d %H:%M:%S"), -45.00, "DEBIT", "Gasoline", "Shell Gas Station"),
            ("TXN9005", "ACC1001", (today - timedelta(days=8)).strftime("%Y-%m-%d %H:%M:%S"), -15.99, "DEBIT", "Subscriptions", "Netflix Monthly Subscription"),
            ("TXN9006", "ACC1002", (today - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"), -250.00, "DEBIT", "Shopping", "Amazon Electronics Purchase"),
            ("TXN9007", "ACC1002", (today - timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S"), 500.00, "CREDIT", "Transfer", "Incoming Zelle Transfer from John Doe"),
            ("TXN9008", "ACC1002", (today - timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S"), -64.20, "DEBIT", "Dining & Groceries", "Starbucks Coffee & Snacks"),
            ("TXN9009", "ACC1002", (today - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S"), -35.00, "DEBIT", "Entertainment", "AMC Movie Theater"),
        ]
        cursor.executemany("INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?, ?)", transactions)

        # Seed Service Requests for USER101
        service_requests = [
            ("SR5001", "USER101", "ACC1001", "Cheque Book Request", "COMPLETED", "25-leaf Cheque Book dispatched to registered address", "2026-08-15 10:30:00"),
            ("SR5002", "USER101", "ACC1001", "Address Update", "IN_PROGRESS", "Update residential address to 742 Evergreen Terrace", "2026-09-02 14:15:00"),
        ]
        cursor.executemany("INSERT INTO service_requests VALUES (?, ?, ?, ?, ?, ?, ?)", service_requests)

        conn.commit()
        print("[Database Setup] Mock banking database successfully created and seeded.")
    else:
        print("[Database Setup] Database already initialized.")

    conn.close()

if __name__ == "__main__":
    init_database()
