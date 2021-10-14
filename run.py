"""
Flask application entry point
"""

from app import create_app

if __name__ == "__main__":
    app = create_app("app.config.Config")
    app.run()
