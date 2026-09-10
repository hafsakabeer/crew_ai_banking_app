import json
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import sqlite3

from models.banking_model import (
    get_user_accounts,
    get_account_balance_info,
    get_account_transactions,
    get_category_spending,
    create_new_service_request,
    get_user_service_requests
)

# Try importing tool from crewai.tools or langchain_core.tools
try:
    from crewai.tools import tool
except ImportError:
    try:
        from crewai_tools import tool
    except ImportError:
        from langchain_core.tools import tool

# Retry policy for DB operations to manage potential database locks or transient errors
def db_retry():
    return retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=5),
        retry=retry_if_exception_type(sqlite3.OperationalError)
    )

# ---------------------------------------------------------------------------
# 1. ACCOUNTS MCP SERVER TOOLS
# ---------------------------------------------------------------------------

@tool("Accounts MCP - Fetch User Account Details")
@db_retry()
def get_account_details(user_id: str = "USER101") -> str:
    """
    Simulates endpoint: GET mcp://accounts-server/user/{user_id}/accounts
    Fetches profile information, account IDs, account types, balances, and status for a given user.
    Default user_id is hardcoded to 'USER101'.
    """
    try:
        accounts = get_user_accounts(user_id)
        if not accounts:
            return json.dumps({"status": "error", "message": f"No accounts found for user_id: {user_id}"})
        return json.dumps({"status": "success", "accounts": accounts}, indent=2)
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

@tool("Accounts MCP - Fetch Specific Account Balance")
@db_retry()
def get_account_balance(account_id: str = "ACC1001") -> str:
    """
    Simulates endpoint: GET mcp://accounts-server/account/{account_id}/balance
    Fetches current available balance and currency for a single account ID.
    Default account_id is 'ACC1001'.
    """
    try:
        acc_info = get_account_balance_info(account_id)
        if not acc_info:
            return json.dumps({"status": "error", "message": f"Account {account_id} not found."})

        return json.dumps({
            "status": "success",
            "account_id": acc_info["account_id"],
            "account_type": acc_info["account_type"],
            "balance": acc_info["balance"],
            "currency": acc_info["currency"],
            "account_status": acc_info["status"]
        }, indent=2)
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

# ---------------------------------------------------------------------------
# 2. TRANSACTIONS MCP SERVER TOOLS
# ---------------------------------------------------------------------------

@tool("Transactions MCP - Fetch Transaction History")
@db_retry()
def get_transaction_history(account_id: str = "ACC1001", limit: int = 10) -> str:
    """
    Simulates endpoint: GET mcp://transactions-server/account/{account_id}/history
    Fetches the recent transaction history for an account up to the specified limit (default 10).
    """
    try:
        tx_list = get_account_transactions(account_id, limit)
        if not tx_list:
            return json.dumps({"status": "success", "message": f"No transactions found for account {account_id}", "transactions": []})

        return json.dumps({"status": "success", "account_id": account_id, "count": len(tx_list), "transactions": tx_list}, indent=2)
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

@tool("Transactions MCP - Analyze Spending by Category")
@db_retry()
def analyze_spending_by_category(account_id: str = "ACC1001") -> str:
    """
    Simulates endpoint: GET mcp://transactions-server/account/{account_id}/spending-analysis
    Calculates total expenditures grouped by spending category for DEBIT transactions on an account.
    """
    try:
        spending_breakdown = get_category_spending(account_id)
        if not spending_breakdown:
            return json.dumps({"status": "success", "message": f"No debit transactions found for category analysis on account {account_id}", "spending": []})

        total_debit = sum(item["total_spent"] for item in spending_breakdown)
        return json.dumps({
            "status": "success",
            "account_id": account_id,
            "total_spending": round(total_debit, 2),
            "breakdown": spending_breakdown
        }, indent=2)
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

# ---------------------------------------------------------------------------
# 3. SERVICE REQUESTS MCP SERVER TOOLS
# ---------------------------------------------------------------------------

@tool("Service MCP - Create Customer Service Request")
@db_retry()
def create_service_request(request_type: str, details: str, account_id: str = "ACC1001", user_id: str = "USER101") -> str:
    """
    Simulates endpoint: POST mcp://service-server/requests/create
    Submits a service ticket such as 'Cheque Book Request', 'Address Update', or 'KYC Detail Update'.
    Returns generated request ID and status.
    """
    try:
        sr_data = create_new_service_request(request_type, details, account_id, user_id)
        return json.dumps({
            "status": "success",
            "message": "Service request submitted successfully.",
            "request_id": sr_data["request_id"],
            "request_type": sr_data["request_type"],
            "account_id": sr_data["account_id"],
            "request_status": sr_data["status"],
            "details": sr_data["details"],
            "created_at": sr_data["created_at"]
        }, indent=2)
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

@tool("Service MCP - Fetch Service Request Status")
@db_retry()
def get_service_request_status(user_id: str = "USER101") -> str:
    """
    Simulates endpoint: GET mcp://service-server/user/{user_id}/requests
    Retrieves status of existing service requests submitted by the user.
    """
    try:
        req_list = get_user_service_requests(user_id)
        if not req_list:
            return json.dumps({"status": "success", "message": f"No service requests found for user {user_id}", "requests": []})

        return json.dumps({"status": "success", "user_id": user_id, "requests": req_list}, indent=2)
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})
