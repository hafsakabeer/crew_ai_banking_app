"""
app.py - Streamlit Main Entry Point (MVC Bootstrapper)

Run with:
    streamlit run app.py
"""

import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import MVC Components
from models.database import init_database
from views.styles import inject_custom_css
from views.sidebar_view import render_sidebar
from views.chat_view import render_chat_interface

def main():
    """Application main entrypoint."""
    # 1. Page Configuration
    st.set_page_config(
        page_title="Apex Financial - AI Banking Assistant",
        page_icon="🏦",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # 2. Inject CSS Styling
    inject_custom_css()

    # 3. Model: Initialize Database & Tables
    init_database()

    # 4. View: Render Sidebar
    render_sidebar(user_id="USER101")

    # 5. View & Controller: Render Main Chat Interface
    render_chat_interface(user_id="USER101")

if __name__ == "__main__":
    main()
