"""
database_setup.py - Backward Compatibility Wrapper for Models Layer
Refactored into models/ package (MVC Architecture).
"""

from models.database import init_database, DB_PATH

if __name__ == "__main__":
    init_database()
