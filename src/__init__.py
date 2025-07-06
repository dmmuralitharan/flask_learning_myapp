import os
import logging
from dotenv import load_dotenv
from flask import Flask, current_app, send_from_directory
from flask_cors import CORS
from flask_smorest import Api

from src.extensions import db, migrate
from src.error_handlers import register_error_handlers
from src.routes import register_blueprints
from src.cli import register_commands


def create_app():

    # Config: Logging
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(message)s"
    )

    # Config: App
    app = Flask(__name__)

    # Config: CORS
    CORS(app)

    # Config: ENV
    load_dotenv()

    try:
        env = os.environ.get("FLASK_ENV", "development")

        if env == "production":
            from .config import ProductionConfig

            app.config.from_object(ProductionConfig)
        elif env == "development":
            from .config import DevelopmentConfig

            app.config.from_object(DevelopmentConfig)

        logging.info("ENV Configured Successfully.")

    except Exception as e:
        logging.error(f"DB Initialize Failed, {e}")

    # Config: Extensions
    try:
        db.init_app(app)
        logging.info("DB Initialized Successfully.")
    except Exception as e:
        logging.error(f"DB Initialize Failed, {e}")

    try:
        migrate.init_app(app, db)
        logging.info("Migrate Initialized Successfully.")
    except Exception as e:
        logging.error(f"Migrate Initialize Failed, {e}")

    # Config: Blueprints
    try:

        @app.route("/src/assets/<path:filename>")
        def serve_static(filename):
            return send_from_directory(
                current_app.config["SERVE_STATIC_FOLDER"], filename
            )
        
        api = Api(app)
        register_blueprints(api)
        logging.info("Routes Initialized Successfully.")
    except Exception as e:
        logging.error(f"Routes Initialize Failed ,{e}")


    # Config: Error handlers
    register_error_handlers(app)

    # Config: CLI Commands
    register_commands(app)

    return app
