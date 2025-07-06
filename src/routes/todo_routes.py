from flask import Blueprint, jsonify, request
from flask.views import MethodView
from marshmallow import ValidationError
from src.dtos.todo_dtos import TodoCreateDTO, TodoQueryParams, TodoUpdateDTO
from src.utils.request_validation import (
    validate_request_body,
    validate_request_query_params,
)
from src.utils.response import success_response, error_response

TODOS = {
    1: {"task": "Learn Flask", "completed": False},
    2: {"task": "Use MethodView", "completed": False},
}

todo_bp = Blueprint("todo_bp", __name__, url_prefix="/api/v1/todos")


class TodoAPI(MethodView):
    @validate_request_query_params(TodoQueryParams)
    def get(self, todo_id=None):
        if todo_id is None:

            query = request.validated_query
            limit = query["limit"]
            search = query.get("search", "").lower()

            print(limit, search)

            todos = [
                {"id": tid, **task}
                for tid, task in TODOS.items()
                if search in task["task"].lower()
            ][:limit]

            return success_response(
                data=todos,
                message=f"{len(todos)} todos fetched successfully",
            )

        todo = TODOS.get(todo_id)

        if not todo:
            return error_response("Todo not found")

        return success_response({"id": todo_id, **todo})

    @validate_request_body(TodoCreateDTO)
    def post(self):
        data = request.get_json()

        new_id = max(TODOS.keys()) + 1 if TODOS else 1

        TODOS[new_id] = {"task": data["task"], "completed": False}

        return success_response(
            {
                "id": new_id,
                "task": data["task"],
                "completed": TODOS[new_id]["completed"],
            }
        )

    @validate_request_body(TodoUpdateDTO)
    def put(self, todo_id):
        data = request.get_json()

        if todo_id not in TODOS:
            return error_response("Todo not found")

        TODOS[todo_id]["task"] = data["task"]
        TODOS[todo_id]["completed"] = data["completed"]

        return success_response(
            {"id": todo_id, "task": data["task"], "completed": data["completed"]}
        )

    def delete(self, todo_id):
        if todo_id not in TODOS:
            return error_response("Todo not found")

        del TODOS[todo_id]

        return success_response({"message": "Todo deleted successfully"}, 204)


todo_view = TodoAPI.as_view("todo_api")
todo_bp.add_url_rule(
    "/", defaults={"todo_id": None}, view_func=todo_view, methods=["GET"]
)
todo_bp.add_url_rule("/", view_func=todo_view, methods=["POST"])
todo_bp.add_url_rule(
    "/<int:todo_id>", view_func=todo_view, methods=["GET", "PUT", "DELETE"]
)
