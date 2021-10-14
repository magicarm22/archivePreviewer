"""
Create SQLAlchemy object to avoid circular imports in __init__.py file
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app: Flask) -> None:
    """
    Initializate a new SQLite database if it didn't find
    :param app: Flask application instance
    :type app: Flask
    """
    with app.app_context():
        db.create_all()
