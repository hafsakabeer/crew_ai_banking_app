"""
controllers/agent_controller.py - CrewAI Multi-Agent Definition & Kickoff Logic
"""

import os
from crewai import Agent, Crew
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception

from controllers.llm_controller import is_rate_limit_error
from mcp_tools import (
    get_account_details,
    get_account_balance,
    get_transaction_history,
    analyze_spending_by_category,
    create_service_request,
    get_service_request_status
)

MAX_RPM_LIMIT = int(os.getenv("MAX_RPM_LIMIT", "900"))  # Set below 1000 RPM for safety margin

def create_banking_agents(llm):
    """
    Constructs the 4 CrewAI agents with rate limiting safeguards and MCP tool bindings.
    """
    # 1. Coordinator Agent (Manager)
    coordinator_agent = Agent(
        role="Banking Operations Manager",
        goal=(
            "Coordinate customer banking inquiries. Analyze customer prompt, call appropriate MCP tools "
            "(Accounts, Transactions, or Customer Service), and construct a polite, comprehensive response."
        ),
        backstory=(
            "You are an experienced Banking Operations Manager with over 15 years in customer banking. "
            "You query account balances, transaction analysis, and customer service requests via MCP tools "
            "and synthesize figures into clean, professional financial advice."
        ),
        tools=[
            get_account_details,
            get_account_balance,
            get_transaction_history,
            analyze_spending_by_category,
            create_service_request,
            get_service_request_status
        ],
        verbose=True,
        allow_delegation=False,
        max_rpm=MAX_RPM_LIMIT,
        llm=llm
    )

    # 2. Accounts Agent
    accounts_agent = Agent(
        role="Account Details Specialist",
        goal=(
            "Retrieve and analyze account balances, profile info, and account statuses "
            "using Accounts MCP Server tools for user_id 'USER101'."
        ),
        backstory=(
            "You are a dedicated Account Details Specialist. Your sole focus is querying "
            "account records via the Accounts MCP tool endpoints, validating account statuses, "
            "and providing accurate snapshot figures of customer accounts."
        ),
        tools=[get_account_details, get_account_balance],
        verbose=True,
        allow_delegation=False,
        max_rpm=MAX_RPM_LIMIT,
        llm=llm
    )

    # 3. Transaction Agent
    transaction_agent = Agent(
        role="Transaction & Statement Specialist",
        goal=(
            "Fetch recent transaction records and analyze spending habits by category "
            "using Transactions MCP Server tools."
        ),
        backstory=(
            "You are a financial analyst specializing in ledger audit and consumer spending patterns. "
            "You query the Transactions MCP tool endpoints to provide transaction histories "
            "and category spending breakdowns."
        ),
        tools=[get_transaction_history, analyze_spending_by_category],
        verbose=True,
        allow_delegation=False,
        max_rpm=MAX_RPM_LIMIT,
        llm=llm
    )

    # 4. Service Agent
    service_agent = Agent(
        role="Customer Service Specialist",
        goal=(
            "Process service requests such as Address Update, Cheque Book Issuance, "
            "and KYC updates, and query ticket statuses using Service MCP Server tools."
        ),
        backstory=(
            "You are a Customer Service Specialist managing bank fulfillment requests. "
            "You create new service tickets or report on existing ticket statuses using "
            "the Service MCP tool endpoints."
        ),
        tools=[create_service_request, get_service_request_status],
        verbose=True,
        allow_delegation=False,
        max_rpm=MAX_RPM_LIMIT,
        llm=llm
    )

    return coordinator_agent, accounts_agent, transaction_agent, service_agent

@retry(
    reraise=True,
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=2, min=2, max=15),
    retry=retry_if_exception(is_rate_limit_error)
)
def kickoff_crew_with_retry(crew: Crew) -> str:
    """Executes crew kickoff with exponential backoff retries on rate limit (429) errors."""
    result = crew.kickoff()
    return str(result)
