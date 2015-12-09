import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'app secret key')

    @staticmethod
    def init_app(app):
        pass

class DevelopConfig(Config):
    DEBUG = True

class TestConfig(Config):
    TESTING = True


class ProdConfig(Config):
    pass

config = {
    'develop': DevelopConfig(),
    'test': TestConfig(),
    'prod': ProdConfig(),
    'default': DevelopConfig(),
}
