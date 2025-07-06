from flask import jsonify
from .utils.response import error_response

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(e):
        return error_response("Resource not found", 404)

    @app.errorhandler(500)
    def internal_error(e):
        return error_response("Internal Server Error", 500)

    @app.errorhandler(400)
    def bad_request(e):
        return error_response("Bad Request", 400)
    