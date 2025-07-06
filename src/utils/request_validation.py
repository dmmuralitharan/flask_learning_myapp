from functools import wraps

from flask import request
from marshmallow import ValidationError

from src.utils.response import error_response


def validate_request_body(schema_class):
    """
    Validate request JSON or FORM body using the provided Marshmallow schema.
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if request.is_json:
                raw_data = request.get_json()
            else:
                form_data = request.form.to_dict()
                file_data = {
                    key: file.filename
                    for key, file in request.files.items()
                    if file.filename
                }
                raw_data = {**form_data, **file_data}

            if not raw_data:
                return error_response("Missing body data", 400)

            try:
                validated = schema_class().load(raw_data)
                request.validated_body = validated
                request.uploaded_files = request.files

            except ValidationError as err:
                return error_response(f"Validation failed {err.messages}", 400)

            return f(*args, **kwargs)

        return wrapper

    return decorator


def validate_request_query_params(schema_class):
    """
    Validate query parameters using the provided Marshmallow schema.
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                validated = schema_class().load(request.args)
                request.validated_query = validated
            except ValidationError as err:
                return error_response("Invalid query parameters", 400, err.messages)

            return f(*args, **kwargs)

        return wrapper

    return decorator
