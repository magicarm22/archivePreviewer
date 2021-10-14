"""
Create SQLAlchemy object to avoid circular imports in __init__.py file
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
