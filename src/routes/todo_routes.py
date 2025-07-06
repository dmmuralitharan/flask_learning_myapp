from flask import Blueprint, request
from src.extensions import db
from flask.views import MethodView
from src.dtos.todo_dtos import TodoCreateDTO, TodoQueryParams, TodoUpdateDTO
from src.models.todo_model import Todo
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

            todo_query = Todo.query

            if search:
                todo_query = todo_query.filter(Todo.task.ilike(f"%{search}%"))

            todos = todo_query.limit(limit).all()

            data = [todo.to_dict() for todo in todos]


            return success_response(
                data=data,
                message=f"{len(data)} todos fetched successfully",
            )

        todo = Todo.query.get(todo_id)

        if not todo:
            return error_response("Todo not found")

        return success_response(todo.to_dict())

    @validate_request_body(TodoCreateDTO)
    def post(self):
        data = request.validated_body

        new_todo = Todo(task=data["task"], completed=False)

        db.session.add(new_todo)
        db.session.commit()

        return success_response(new_todo.to_dict(), "Todo Created")

    @validate_request_body(TodoUpdateDTO)
    def put(self, todo_id):
        data = request.validated_body

        todo = Todo.query.get(todo_id)

        if not todo:
            return error_response("Todo not found")

        todo.task = data.get("task", todo.task)
        todo.completed = data.get("completed", todo.completed)

        db.session.commit()

        return success_response(todo.to_dict(), "Todo Updated")

    def delete(self, todo_id):

        todo = Todo.query.get(todo_id)

        if not todo:
            return error_response("Todo not found")
        
        db.session.delete(todo)
        db.session.commit()

        return success_response({"message": "Todo deleted successfully"}, 204)


todo_view = TodoAPI.as_view("todo_api")
todo_bp.add_url_rule(
    "/", defaults={"todo_id": None}, view_func=todo_view, methods=["GET"]
)
todo_bp.add_url_rule("/", view_func=todo_view, methods=["POST"])
todo_bp.add_url_rule(
    "/<int:todo_id>", view_func=todo_view, methods=["GET", "PUT", "DELETE"]
)
