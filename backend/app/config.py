class BaseConfig:
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class DefaultConfig(BaseConfig):
    ...


class TestingConfig(BaseConfig):
    TESTING = True
    DEBUG = True


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    ...
