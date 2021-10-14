"""
File with configurations. Has basic and testing configuration
"""


class Config:  # pylint: disable=too-few-public-methods
    """
    Basic config with standart params:
        DEBUG - enabling debug mode
        SQLALCHEMY_DATABASE_URI - path, where SQLite database should be kept
        SQLALCHEMY_TRACK_MODIFICATIONS - track modifications of objects and emit signals.
        If false - show warning after start
        TESTING - enabling testing mode.
    """
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///archivePreviewer.db'  # os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    TESTING = False


class TestingConfig(Config):  # pylint: disable=too-few-public-methods
    """
    Testing configuration with changed database uri and testing mode
    """
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tests/files/testdb.db'
    TESTING = True
