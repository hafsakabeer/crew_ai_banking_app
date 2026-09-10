"""
controllers/llm_controller.py - Groq LLM Setup & LiteLLM Patching
"""

import os
from dotenv import load_dotenv
from crewai import LLM
from langchain_groq import ChatGroq
import litellm

# Patch litellm completion to strip cache_breakpoint flag (unsupported by Groq API)
_original_litellm_completion = litellm.completion
def _patched_litellm_completion(*args, **kwargs):
    if "messages" in kwargs and kwargs["messages"]:
        for msg in kwargs["messages"]:
            if isinstance(msg, dict):
                msg.pop("cache_breakpoint", None)
    return _original_litellm_completion(*args, **kwargs)

litellm.completion = _patched_litellm_completion

def is_rate_limit_error(exception: Exception) -> bool:
    """Returns True if the exception indicates HTTP 429 / Rate Limit error."""
    err_str = str(exception).lower()
    return "429" in err_str or "rate limit" in err_str or "too many requests" in err_str or "quota" in err_str

def get_llm_instance() -> LLM:
    """
    Initializes ChatGroq LLM reading model name and API key dynamically from environment or Streamlit secrets.
    """
    load_dotenv(override=True)

    # Sync Streamlit secrets to os.environ for Streamlit Cloud deployment
    try:
        import streamlit as st
        if hasattr(st, "secrets"):
            for key, val in st.secrets.items():
                if isinstance(val, str) and not os.getenv(key):
                    os.environ[key] = val
    except Exception:
        pass

    model_name = os.getenv("GROQ_MODEL") or os.getenv("MODEL_NAME") or "qwen/qwen3.6-27b"
    if model_name.startswith("groq/"):
        model_name = model_name.replace("groq/", "")
        
    api_key = (
        os.getenv("GROQ_API_KEY") or
        os.getenv("API_KEY") or
        os.getenv("OPENAI_API_KEY") or
        "gsk_dummy_groq_key"
    )

    # Initialize ChatGroq instance for LangChain / ChatGroq compatibility
    chat_groq = ChatGroq(
        model=model_name,
        groq_api_key=api_key,
        temperature=0.2,
        max_tokens=2048
    )

    # Return LLM wrapper for CrewAI Agents
    return LLM(
        model=f"groq/{model_name}",
        api_key=api_key,
        temperature=0.2,
        max_tokens=2048
    )
