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
    API_TITLE = "My Todo API"
    API_VERSION = "1.0"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/api_docs"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"


class ProductionConfig(BaseConfig):
    DEBUG = False
    ENV = "production"
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
