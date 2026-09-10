"""
agents_and_tasks.py - Backward Compatibility Wrapper for Controllers Layer
Refactored into controllers/ package (MVC Architecture).
"""

from controllers.llm_controller import get_llm_instance, is_rate_limit_error
from controllers.agent_controller import create_banking_agents, kickoff_crew_with_retry as _kickoff_crew_with_retry, MAX_RPM_LIMIT
from controllers.banking_controller import run_banking_assistant

__all__ = [
    "get_llm_instance",
    "is_rate_limit_error",
    "create_banking_agents",
    "MAX_RPM_LIMIT",
    "_kickoff_crew_with_retry",
    "run_banking_assistant"
]
