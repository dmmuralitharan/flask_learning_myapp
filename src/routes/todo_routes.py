from flask_smorest import Blueprint
from flask.views import MethodView
from src.controllers.todo_controller import (
    create_todo_controller,
    delete_todo_controller,
    fetch_todo_controller,
    fetch_todos_controller,
    update_todo_controller,
)
from src.dtos.todo_dtos import TodoCreateDTO, TodoQueryParams, TodoUpdateDTO


todo_bp = Blueprint(
    "Todo",
    "todo",
    url_prefix="/api/v1/todos",
    description="Operations related to todos",
)


@todo_bp.route("/")
class TodoAPI(MethodView):
    @todo_bp.arguments(TodoQueryParams, location="query")
    def get(self, args):
        return fetch_todos_controller(query=args)

    @todo_bp.arguments(TodoCreateDTO)
    def post(self, json_data):
        return create_todo_controller(json_data)


@todo_bp.route("/<int:todo_id>")
class TodoWithIDRouteAPI(MethodView):
    def get(self, todo_id):
        return fetch_todo_controller(todo_id)

    @todo_bp.arguments(TodoUpdateDTO)
    def put(self, json_data, todo_id):
        return update_todo_controller(todo_id, json_data)

    def delete(self, todo_id):
        return delete_todo_controller(todo_id)
