import os


class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY", "default")
    DEBUG = False
    TESTING = False
    UPLOAD_FOLDER = "src/assets/"
    SERVE_STATIC_FOLDER = os.path.abspath("src/assets")


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    ENV = "development"
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(BaseConfig):
    DEBUG = False
    ENV = "production"
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
