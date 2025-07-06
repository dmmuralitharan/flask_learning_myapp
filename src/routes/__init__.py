from .todo_routes import todo_bp


def register_blueprints(app):
    app.register_blueprint(todo_bp)
