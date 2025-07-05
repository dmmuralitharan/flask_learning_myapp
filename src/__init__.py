import os
from dotenv import load_dotenv
from flask import Flask


def create_app():

    load_dotenv()

    app = Flask(__name__)

    # env
    env = os.environ.get("FLASK_ENV", "development")

    if env == "production":
        from .config import ProductionConfig

        app.config.from_object(ProductionConfig)
    elif env == "development":
        from .config import DevelopmentConfig

        app.config.from_object(DevelopmentConfig)

    # routes
    from .routes.todo_routes import todo_bp

    app.register_blueprint(todo_bp)


    return app
