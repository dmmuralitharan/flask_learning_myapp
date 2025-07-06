from .todo_routes import todo_bp


def register_blueprints(api):
    api.register_blueprint(todo_bp)
