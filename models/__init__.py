"""
Models package for Banking Assistant application.
Contains database schema setup and banking data access functions.
"""
from models.database import init_database, DB_PATH
from models.banking_model import (
    get_user_accounts,
    get_account_balance_info,
    get_account_transactions,
    get_category_spending,
    create_new_service_request,
    get_user_service_requests
)

__all__ = [
    "init_database",
    "DB_PATH",
    "get_user_accounts",
    "get_account_balance_info",
    "get_account_transactions",
    "get_category_spending",
    "create_new_service_request",
    "get_user_service_requests"
]
