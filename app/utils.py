from flask import request
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request
from flask_expects_json import expects_json


def jwt_required_for_change(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if request.method in ['POST', 'PUT', 'DELETE']:
            verify_jwt_in_request()
        return func(*args, **kwargs)
    return wrapped


def json_validate_for_change(schema):
    def inner_function(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if request.method in ['POST', 'PUT']:
                return expects_json(schema)(func)(*args, **kwargs)
            return func(*args, **kwargs)
        return wrapped
    return inner_function
