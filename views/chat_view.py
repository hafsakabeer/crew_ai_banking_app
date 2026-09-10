"""
views/chat_view.py - Chat Interface Component for Multi-Agent Banking Assistant
"""

import streamlit as st
from controllers.banking_controller import run_banking_assistant

def render_chat_interface(user_id: str = "USER101"):
    """Renders the main chat header, prompt chips, message list, and handles query submission."""
    st.markdown("<div class='main-header'>Apex AI Banking Operations Assistant</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Powered by CrewAI Multi-Agent Hierarchy & Model Context Protocol (MCP)</div>", unsafe_allow_html=True)

    # Quick Prompt Chips
    st.markdown("**Try asking:**")
    col1, col2, col3, col4 = st.columns(4)

    prompt_input = None

    with col1:
        if st.button("💰 Account Balances", use_container_width=True):
            prompt_input = "What are my current account balances for savings and checking?"

    with col2:
        if st.button("📊 Recent Transactions", use_container_width=True):
            prompt_input = "Show my recent transactions for account ACC1001."

    with col3:
        if st.button("📈 Spending Analysis", use_container_width=True):
            prompt_input = "Analyze my spending by category for account ACC1001."

    with col4:
        if st.button("✉️ Request Cheque Book", use_container_width=True):
            prompt_input = "I want to request a new cheque book for my account ACC1001."

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello Alex! I am your AI Banking Assistant. I can help you check balances, analyze transactions, or submit service requests. How can I assist you today?"}
        ]

    # Render existing chat messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Capture user prompt from chat input or chip click
    user_query = st.chat_input("Ask a banking question (e.g. 'Show my account balance' or 'Update my address')...")
    if prompt_input:
        user_query = prompt_input

    if user_query:
        # Append user message to history
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        # Process through CrewAI Multi-Agent system via Banking Controller
        with st.chat_message("assistant"):
            with st.spinner("🤖 Coordinator Agent routing task to specialized MCP Agents (Accounts, Transactions, Service)..."):
                try:
                    response = run_banking_assistant(user_prompt=user_query, user_id=user_id)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as ex:
                    err_msg = f"⚠️ **Application Error**: Unable to complete request.\n\n`{str(ex)}`"
                    st.error(err_msg)
                    st.session_state.messages.append({"role": "assistant", "content": err_msg})
