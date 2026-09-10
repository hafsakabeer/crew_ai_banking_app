"""
models/banking_model.py - Data Access Model for Banking Operations
"""

import uuid
from datetime import datetime
from models.database import get_connection

def get_user_accounts(user_id: str = "USER101") -> list:
    """Fetches all accounts for a specific user ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT account_id, user_id, account_type, balance, currency, status, created_at FROM accounts WHERE user_id = ?",
        (user_id,)
    )
    rows = cursor.fetchall()
    conn.close()

    accounts = []
    for r in rows:
        accounts.append({
            "account_id": r[0],
            "user_id": r[1],
            "account_type": r[2],
            "balance": r[3],
            "currency": r[4],
            "status": r[5],
            "created_at": r[6]
        })
    return accounts

def get_account_balance_info(account_id: str = "ACC1001") -> dict:
    """Fetches balance information for a specific account ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT account_id, account_type, balance, currency, status FROM accounts WHERE account_id = ?",
        (account_id,)
    )
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "account_id": row[0],
        "account_type": row[1],
        "balance": row[2],
        "currency": row[3],
        "status": row[4]
    }

def get_account_transactions(account_id: str = "ACC1001", limit: int = 10) -> list:
    """Fetches transaction history for a specific account ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT transaction_id, date, amount, transaction_type, category, description FROM transactions WHERE account_id = ? ORDER BY date DESC LIMIT ?",
        (account_id, limit)
    )
    rows = cursor.fetchall()
    conn.close()

    transactions = []
    for r in rows:
        transactions.append({
            "transaction_id": r[0],
            "date": r[1],
            "amount": r[2],
            "type": r[3],
            "category": r[4],
            "description": r[5]
        })
    return transactions

def get_category_spending(account_id: str = "ACC1001") -> list:
    """Calculates category spending breakdown for DEBIT transactions."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT category, SUM(ABS(amount)) as total_spent, COUNT(*) as count FROM transactions WHERE account_id = ? AND transaction_type = 'DEBIT' GROUP BY category ORDER BY total_spent DESC",
        (account_id,)
    )
    rows = cursor.fetchall()
    conn.close()

    breakdown = []
    for r in rows:
        breakdown.append({
            "category": r[0],
            "total_spent": round(r[1], 2),
            "transaction_count": r[2]
        })
    return breakdown

def create_new_service_request(request_type: str, details: str, account_id: str = "ACC1001", user_id: str = "USER101") -> dict:
    """Creates a new service request record."""
    request_id = f"SR{uuid.uuid4().hex[:4].upper()}"
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "SUBMITTED"

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO service_requests VALUES (?, ?, ?, ?, ?, ?, ?)",
        (request_id, user_id, account_id, request_type, status, details, created_at)
    )
    conn.commit()
    conn.close()

    return {
        "request_id": request_id,
        "user_id": user_id,
        "account_id": account_id,
        "request_type": request_type,
        "status": status,
        "details": details,
        "created_at": created_at
    }

def get_user_service_requests(user_id: str = "USER101") -> list:
    """Fetches service request tickets for a specific user ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT request_id, account_id, request_type, status, details, created_at FROM service_requests WHERE user_id = ? ORDER BY created_at DESC",
        (user_id,)
    )
    rows = cursor.fetchall()
    conn.close()

    requests = []
    for r in rows:
        requests.append({
            "request_id": r[0],
            "account_id": r[1],
            "request_type": r[2],
            "status": r[3],
            "details": r[4],
            "created_at": r[5]
        })
    return requests
