"""
controllers/banking_controller.py - Primary Controller Orchestrator for Banking Operations
"""

import time
from crewai import Task, Crew, Process
from controllers.llm_controller import get_llm_instance, is_rate_limit_error
from controllers.agent_controller import create_banking_agents, kickoff_crew_with_retry, MAX_RPM_LIMIT

def run_banking_assistant(user_prompt: str, user_id: str = "USER101") -> str:
    """
    Main entrypoint for processing user prompts through the multi-agent banking crew.
    """
    llm = get_llm_instance()
    coordinator, accounts_spec, tx_spec, service_spec = create_banking_agents(llm)

    # Define task
    t1 = Task(
        description=(
            f"Process the following customer query for user_id '{user_id}':\n"
            f"Query: '{user_prompt}'\n\n"
            f"Steps:\n"
            f"1. Identify if the query involves account balance/details, transaction history/spending analysis, or customer service requests (address, cheque book, KYC).\n"
            f"2. Delegate to or execute using the appropriate specialist agent and MCP tools.\n"
            f"3. Return a clean, helpful, structured response with financial amounts clearly formatted."
        ),
        expected_output="A helpful, structured, customer-facing answer addressing the user's banking query.",
        agent=coordinator
    )

    banking_crew = Crew(
        agents=[coordinator, accounts_spec, tx_spec, service_spec],
        tasks=[t1],
        process=Process.sequential,
        verbose=True,
        max_rpm=MAX_RPM_LIMIT
    )

    # Micro-delay to avoid bursting API limits
    time.sleep(0.2)

    try:
        response = kickoff_crew_with_retry(banking_crew)
        return response
    except Exception as e:
        err_str = str(e)
        if "decommissioned" in err_str.lower():
            return f"⚠️ **Groq Model Decommissioned Error**: The specified model is decommissioned or unavailable on Groq.\n\nPlease update the Groq Model Name input in the sidebar (or `.env` file) to an active model (e.g. `qwen/qwen3.6-27b`, `qwen/qwen3.8-27b`, or `llama-3.3-70b-versatile`).\n\n*Error details: {err_str}*"
        elif "invalid_api_key" in err_str.lower() or "401" in err_str:
            return f"⚠️ **Invalid Groq API Key**: Please enter a valid `GROQ_API_KEY` in the sidebar or update your `.env` file.\n\n*Error details: {err_str}*"
        elif is_rate_limit_error(e):
            return f"⚠️ **Rate Limit Alert (HTTP 429)**: The Groq LLM API request threshold was hit. Retried multiple times. Please wait a moment and try again.\n\n*Error details: {err_str}*"
        return f"⚠️ **Execution Error**: {err_str}"
