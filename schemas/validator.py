from functools import wraps

from flask import abort, request
from marshmallow import Schema, ValidationError


def validate_json(schema: type[Schema]):
    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                schema().load(data=request.json)
            except ValidationError:
                abort(400)
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator