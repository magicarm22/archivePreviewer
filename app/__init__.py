"""
File initialize database, is importing views and modules.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# pylint: disable=wrong-import-position
from app import views
from app import models


def create_app(config_name: str) -> Flask:
    """
    Create Flask application, initialize database, register views of the project
    and return Flask application object
    :param config_name: name of configuration. app.config.<ConfigName>
    :type config_name: str
    :return: Flask application object
    :rtype: Flask
    """
    app = Flask(__name__)
    app.config.from_object(config_name)

    db.init_app(app)

    app.register_blueprint(views.app)

    return app
