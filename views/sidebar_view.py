"""
views/sidebar_view.py - Sidebar View Component for Profile, Accounts & LLM Settings
"""

import os
import streamlit as st
from models.banking_model import get_user_accounts
from controllers.agent_controller import MAX_RPM_LIMIT

def render_sidebar(user_id: str = "USER101"):
    """Renders the Streamlit sidebar with profile data, linked accounts, and LLM configuration."""
    with st.sidebar:
        st.markdown("### 🏦 Apex Bank Profile")
        st.markdown("**Customer**: Alex Johnson")
        st.markdown(f"**User ID**: `{user_id}` *(Hardcoded POC)*")
        st.markdown("---")

        # Fetch Linked Accounts Snapshot from Model layer
        st.markdown("#### 💳 Linked Accounts")
        try:
            accounts = get_user_accounts(user_id)
            for acc in accounts:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-title">{acc['account_type']} ({acc['account_id']})</div>
                    <div class="stat-value">${acc['balance']:,.2f} {acc['currency']}</div>
                    <span class="badge-active">{acc['status']}</span>
                </div>
                """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error loading account summary: {e}")

        st.markdown("---")
        st.markdown("#### ⚡ LLM & Rate Limits")
        
        active_model = os.getenv("GROQ_MODEL") or os.getenv("MODEL_NAME") or "qwen/qwen3.6-27b"
        env_api_key = os.getenv("GROQ_API_KEY") or os.getenv("API_KEY") or ""

        user_groq_key = st.text_input("Groq API Key:", value=env_api_key, type="password", help="Enter your Groq API Key if not loaded from .env")
        if user_groq_key:
            os.environ["GROQ_API_KEY"] = user_groq_key
            os.environ["API_KEY"] = user_groq_key

        user_model_name = st.text_input("Groq Model Name:", value=active_model, help="Enter active Groq model (e.g. qwen/qwen3.6-27b, qwen/qwen3.8-27b, etc.)")
        if user_model_name:
            os.environ["GROQ_MODEL"] = user_model_name
            os.environ["MODEL_NAME"] = user_model_name

        st.info(f"**LLM Model**: `ChatGroq ({user_model_name})`\n\n"
                f"**Max Rate Limit**: `{MAX_RPM_LIMIT} RPM`\n\n"
                f"**MCP Architecture**: CrewAI Tools + Tenacity Retries.")

        st.markdown("---")
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
