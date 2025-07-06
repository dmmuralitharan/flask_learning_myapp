from flask import request

from src.extensions import db
from src.models.todo_model import Todo
from src.utils.response import error_response, success_response


def fetch_todos_controller(query):

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


def create_todo_controller(data):

    new_todo = Todo(task=data["task"], completed=False)

    db.session.add(new_todo)
    db.session.commit()

    return success_response(new_todo.to_dict(), "Todo Created")


def fetch_todo_controller(todo_id):
    todo = Todo.query.get(todo_id)

    if not todo:
        return error_response("Todo not found")

    return success_response(todo.to_dict())


def update_todo_controller(todo_id, data):

    todo = Todo.query.get(todo_id)

    if not todo:
        return error_response("Todo not found")

    todo.task = data.get("task", todo.task)
    todo.completed = data.get("completed", todo.completed)

    db.session.commit()

    return success_response(todo.to_dict(), "Todo Updated")


def delete_todo_controller(todo_id):
    todo = Todo.query.get(todo_id)

    if not todo:
        return error_response("Todo not found")

    db.session.delete(todo)
    db.session.commit()

    return success_response({"message": "Todo deleted successfully"}, 204)
