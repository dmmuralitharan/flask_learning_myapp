from flask import Blueprint
from flask.views import MethodView
from src.controllers.todo_controller import (
    create_todo_controller,
    delete_todo_controller,
    fetch_todos_controller,
    update_todo_controller,
)
from src.dtos.todo_dtos import TodoCreateDTO, TodoQueryParams, TodoUpdateDTO
from src.utils.request_validation import (
    validate_request_body,
    validate_request_query_params,
)


todo_bp = Blueprint("todo_bp", __name__, url_prefix="/api/v1/todos")


class TodoAPI(MethodView):
    @validate_request_query_params(TodoQueryParams)
    def get(self, todo_id=None):
        return fetch_todos_controller(todo_id)

    @validate_request_body(TodoCreateDTO)
    def post(self):
        return create_todo_controller()

    @validate_request_body(TodoUpdateDTO)
    def put(self, todo_id):
        return update_todo_controller(todo_id)

    def delete(self, todo_id):
        return delete_todo_controller(todo_id)


todo_view = TodoAPI.as_view("todo_api")
todo_bp.add_url_rule(
    "/", defaults={"todo_id": None}, view_func=todo_view, methods=["GET"]
)
todo_bp.add_url_rule("/", view_func=todo_view, methods=["POST"])
todo_bp.add_url_rule(
    "/<int:todo_id>", view_func=todo_view, methods=["GET", "PUT", "DELETE"]
)
