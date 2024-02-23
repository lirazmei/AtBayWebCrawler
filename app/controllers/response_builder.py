import json
from flask import current_app
from flask import json

JSON_TYPE = (dict, list)

UTF8 = "utf8"

APP_JSON = 'application/json'
OK = 200
INTERNAL_SERVER_ERROR = 500


def ok(body, status_code=OK):
    return response(body, status_code)


def server_error(body, status_code=INTERNAL_SERVER_ERROR):
    return response(body, status_code)


def response(body, status_code):
    validate_message(body)

    json_message = json.dumps(body, indent=2, separators=(', ', ':')).encode(UTF8)

    return current_app.response_class(response=json_message, status=status_code,
                                      mimetype=APP_JSON,
                                      content_type=f'{APP_JSON}; charset={UTF8}')


def validate_message(body):
    if not isinstance(body, JSON_TYPE):
        raise TypeError("response body must be dict or array")
