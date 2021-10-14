class Config:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///archivePreviewer.db'  # os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    TESTING = False


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tests/files/testdb.db'
    TESTING = True
