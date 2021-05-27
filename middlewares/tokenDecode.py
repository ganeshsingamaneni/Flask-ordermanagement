from flask import request,g
from functools import wraps
from flask_jwt_extended import (jwt_required,get_jwt_identity)
from werkzeug.wrappers import Request



class TokenDecoder(Request):

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        # print(request.get_json())
        current_user = get_jwt_identity()
        return self.app(environ, start_response)


def decode_token(token):
    @wraps(f)
    def decode(*args, **kwargs):
        print(*args,**kwargs)
        # print(Request(environ,shallow=True))
        # Request(environ, shallow=True)
        print(request.get_json())
        # print('came to middleware')
        # current_user = get_jwt_identity()
        # print(current_user)
        # print(g.user)
        return f(*args, **kwargs)
    return decode
