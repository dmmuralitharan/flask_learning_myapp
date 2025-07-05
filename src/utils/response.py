from flask import jsonify


def success_response(
    data=None, message="Success", status_message_code=1, status_code=200
):
    return (
        jsonify(
            {
                "status": status_message_code,
                "success": True,
                "message": message,
                "data": data,
            }
        ),
        status_code,
    )


def error_response(
    message="Something went wrong", status_message_code=0, status_code=400
):
    return (
        jsonify({"status": status_message_code, "success": False, "message": message}),
        status_code,
    )
