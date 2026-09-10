"""
Views package for Banking Assistant application.
Contains CSS styling, sidebar view, and chat view components.
"""
from views.styles import inject_custom_css
from views.sidebar_view import render_sidebar
from views.chat_view import render_chat_interface

__all__ = [
    "inject_custom_css",
    "render_sidebar",
    "render_chat_interface"
]
