"""Useful decorators"""

from flask import request
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request
from flask_expects_json import expects_json


def jwt_required_for_change(func):
    """This decorator verifies that for every and only POST, PUT and DELETE
    requests jwt token verification will be performed.
    If request is of type POST, PUT or DELETE, the jwt from request header
    will be extracted and verified. GET's requests jwt token is not verified
    and not required.
    """
    @wraps(func)
    def wrapped(*args, **kwargs):
        if request.method in ['POST', 'PUT', 'DELETE']:
            verify_jwt_in_request()
        return func(*args, **kwargs)
    return wrapped


def json_validate_for_change(schema):
    """This decorator validates json body by certain schema. Json body is
    required for PUT and POST requests. If json validation fails, the response
    will be 400 BAD REQUEST. Other than PUT and POST requests are not checked
    for json and it's correctness
    """
    def inner_function(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if request.method in ['POST', 'PUT']:
                return expects_json(schema)(func)(*args, **kwargs)
            return func(*args, **kwargs)
        return wrapped
    return inner_function
