from flask import request
# from config import *
import json
import re
import jwt
from werkzeug.wrappers import Request, Response
from sqlalchemy import and_
from models.users import Users
from models.permissions import Permission



class PermissionMiddleware(object):
    def __init__(self, app):
        self.app = app
    def __call__(self, environ, start_response):
        request = Request(environ)
        method = request.method
        decoded_token = jwt.decode(request.headers['Authorization'][7:], 'ILOVECARATRED', algorithms=['HS256'])
        user_id = decoded_token['identity']['userId']
        get_user_data = Users.query.filter(Users.id==user_id).one_or_none()
        # role_id = get_user_data.__dict__['roleId']
        get_permission_data = Permission.query.filter(and_(Permission.roleId==2,Permission.viewId==1)).one_or_none()
        if get_permission_data.__dict__[method.lower()]==1:
            return self.app(environ, start_response)
        else:
            response = Response(json.dumps({
                        'success':False,
                        'message':'You have no access',
                    }))
            return response(environ, start_response)