"""
views/styles.py - Custom CSS & Aesthetic Styling for Banking Assistant UI
"""

import streamlit as st

def inject_custom_css():
    """Injects custom CSS styling for Apex Financial theme."""
    st.markdown("""
    <style>
        .main-header {
            font-size: 2.2rem;
            font-weight: 700;
            background: linear-gradient(135deg, #1E3C72 0%, #2A5298 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0px;
        }
        .sub-header {
            font-size: 1.0rem;
            color: #6c757d;
            margin-bottom: 20px;
        }
        .stat-card {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 15px;
            border-left: 4px solid #2A5298;
            margin-bottom: 12px;
        }
        .stat-title {
            font-size: 0.85rem;
            color: #6c757d;
            font-weight: 600;
            text-transform: uppercase;
        }
        .stat-value {
            font-size: 1.3rem;
            font-weight: 700;
            color: #1E3C72;
        }
        .badge-active {
            background-color: #d4edda;
            color: #155724;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
        }
    </style>
    """, unsafe_allow_html=True)
