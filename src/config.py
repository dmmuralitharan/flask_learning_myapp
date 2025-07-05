import os


class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY", "default")
    DEBUG = False
    TESTING = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    ENV = "development"


class ProductionConfig(BaseConfig):
    DEBUG = False
    ENV = "production"
