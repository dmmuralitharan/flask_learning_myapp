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

    # global error handles
    @app.errorhandler(404)
    def not_found(e):
        from .utils.response import error_response

        return error_response("Resource not found", 404)

    @app.errorhandler(500)
    def internal_error(e):
        from .utils.response import error_response

        return error_response("Internal Server Error", 500)

    @app.errorhandler(400)
    def bad_request(e):
        from .utils.response import error_response

        return error_response("Bad Request", 400)

    return app
