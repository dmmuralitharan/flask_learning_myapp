from flask import Blueprint, jsonify, request
from flask.views import MethodView
from marshmallow import ValidationError
from src.dtos.todo_dtos import TodoCreateDTO, TodoQueryParams, TodoUpdateDTO
from src.utils.response import success_response, error_response

TODOS = {
    1: {"task": "Learn Flask", "completed": False},
    2: {"task": "Use MethodView", "completed": False},
}

todo_bp = Blueprint("todo_bp", __name__, url_prefix="/api/v1/todos")


class TodoAPI(MethodView):
    def get(self, todo_id=None):
        if todo_id is None:

            try:
                query_params_validated = TodoQueryParams().load(request.args)
            except ValidationError as err:
                return error_response(f"Params Error : {err.messages}")

            limit = query_params_validated["limit"]
            search = query_params_validated.get("search", "").lower()

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

    def post(self):
        data = request.get_json()

        try:
            validated = TodoCreateDTO().load(data)
        except ValidationError as err:
            return error_response(f"Validation failed : {err.messages}", 400)

        new_id = max(TODOS.keys()) + 1 if TODOS else 1

        TODOS[new_id] = {"task": data["task"], "completed": False}

        return success_response(
            {
                "id": new_id,
                "task": data["task"],
                "completed": TODOS[new_id]["completed"],
            }
        )

    def put(self, todo_id):
        data = request.get_json()

        if todo_id not in TODOS:
            return error_response("Todo not found")

        try:
            validated = TodoUpdateDTO().load(data)
        except ValidationError as err:
            return error_response(f"Validation failed : {err.messages}", 400)

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
