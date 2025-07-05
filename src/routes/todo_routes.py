from flask import Blueprint, jsonify, request
from flask.views import MethodView

TODOS = {1: {"task": "Learn Flask"}, 2: {"task": "Use MethodView"}}

todo_bp = Blueprint("todo_bp", __name__, url_prefix="/api/v1/todos")


class TodoAPI(MethodView):
    def get(self, todo_id=None):
        if todo_id is None:
            return jsonify([{"id": tid, **task} for tid, task in TODOS.items()])

        todo = TODOS.get(todo_id)

        if not todo:
            return jsonify({"message": "Todo not found"})

        return jsonify({"id": todo_id, **todo})

    def post(self):
        data = request.get_json()

        if not data or "task" not in data:
            return jsonify({"message": "Task is required"})

        new_id = max(TODOS.keys()) + 1 if TODOS else 1

        TODOS[new_id] = {"task": data["task"]}

        return jsonify({"id": new_id, "task": data["task"]}), 201

    def put(self, todo_id):
        data = request.get_json()

        if todo_id not in TODOS:
            return jsonify({"message": "Todo not found"})

        if not data or "task" not in data:
            return jsonify({"message": "Task is required"})

        TODOS[todo_id]["task"] = data["task"]

        return jsonify({"id": todo_id, "task": data["task"]})

    def delete(self, todo_id):
        if todo_id not in TODOS:
            return jsonify({"message": "Todo not found"})

        del TODOS[todo_id]

        return jsonify({"message": "Todo deleted successfully"}), 204


todo_view = TodoAPI.as_view("todo_api")
todo_bp.add_url_rule(
    "/", defaults={"todo_id": None}, view_func=todo_view, methods=["GET"]
)
todo_bp.add_url_rule("/", view_func=todo_view, methods=["POST"])
todo_bp.add_url_rule(
    "/<int:todo_id>", view_func=todo_view, methods=["GET", "PUT", "DELETE"]
)
