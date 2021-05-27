# from config.modules import Resource, request, Response, PermissionModel, get_jwt_identity, db, jwt_required
from config.config import *
from flask_restful import Resource
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from config.logger import Logger
from schemas.permission_schema import GetAddPermissionSchema, AddPermissionValidator, UpdatePermissionValidator,PermissionSchema
from models.roles import Roles
from schemas.roles_schema import ViewPermissionRoleSchme
from sqlalchemy import and_

class GetAddPermission(Resource):
    def __init__(self):
        pass
    # Permission get call

    def get(self):
        try:
            obj = db.session.query(PermissionModel).order_by(PermissionModel.id.desc()).all()
            if obj:
                schema = GetAddPermissionSchema(many=True)
                data = schema.dump(obj).data
                return Response.return_response('success', data, 200)
            else:
                return Response.return_response('success', [], 200,"No data found")
        except Exception as e:
            Logger.create_error_log("getaddpermission", str(e))
            return Response.return_response('Error', None, 500)

    # Permission post call
    @jwt_required
    def post(self):
        try:
            current_user = get_jwt_identity()
            req_data = request.get_json()
            req_data['createdBy'] = current_user['userId']
            per_exist = db.session.query(PermissionModel).filter(and_(PermissionModel.roleId==req_data['roleId'],PermissionModel.viewId==req_data['viewId'])).one_or_none()
            if per_exist is not None:
                return Response.return_response('Error', {}, 200,"Permission already exists")
            validate_schema = AddPermissionValidator()
            errors = validate_schema.validate(req_data)
            if errors:
                return Response.return_response('Error', errors, 400, 'Bad request')
            schema = GetAddPermissionSchema()
            obj = schema.load(req_data, session=db.session).data
            db.session.add(obj)
            db.session.commit()
            data = schema.dump(obj).data
            return Response.return_response('success', data, 200)
        except Exception as e:
            Logger.create_error_log("getaddpermission", str(e))
            return Response.return_response('Error', None, 500)


class GetUpdatePermission(Resource):
    def __init__(self):
        pass

    # Permission get call by id
    def get(self, id):
        try:
            obj = PermissionModel.query.filter(PermissionModel.id == id).one_or_none()
            if obj is not None:
                schema = GetAddPermissionSchema()
                data = schema.dump(obj).data
                return Response.return_response('success', data, 200)
            else:
                return Response.return_response('success', [], 200,"No data found")
        except Exception as e:
            Logger.create_error_log("getupdatepermission", str(e))
            return Response.return_response('Error', None, 500)

    # Permission update call
    @jwt_required
    def put(self, id):
        try:
            current_user = get_jwt_identity()
            req_data= request.get_json()
            req_data['updatedBy'] = current_user['userId']
            obj = db.session.query(PermissionModel).filter_by(id = id).first()
            if obj:
                # role_exist = RoleUtility.check_updatecall_role_name_exist(req_data['name'],id)
                # if role_exist:
                #     return Response.return_response('Error', {}, 200,"Role already exists")
                validate_schema = UpdatePermissionValidator()
                errors = validate_schema.validate(req_data)
                if errors:
                    return Response.return_response('Error', errors, 400, 'Bad request')
                permission_obj = db.session.query(PermissionModel).filter_by(id = id).update(req_data)
                db.session.commit()
                obj_permission = PermissionModel.query.filter(PermissionModel.id == id).one()
                permission_schema = GetAddPermissionSchema()
                data = permission_schema.dump(obj_permission).data
                return Response.return_response('success', data, 200)
            else:
                return Response.return_response('success', [], 200,"No data found")
        except Exception as e:
            Logger.create_error_log("getupdatepermission", str(e))
            return Response.return_response('Error', None, 500)


class PermissionsByRole(Resource):
    def __init__(self):
        pass
    # Permission get call
    @jwt_required
    def get(self,id):
        try:
            # current_user = get_jwt_identity()
            obj = db.session.query(Roles).filter(Roles.id==id).all()
            if obj:
                schema = ViewPermissionRoleSchme(many=True)
                data = schema.dump(obj).data
                return Response.return_response('success', data, 200)
            else:
                return Response.return_response('success', [], 200,"No data found")
        except Exception as e:
            Logger.create_error_log("getaddpermission", str(e))
            return Response.return_response('Error', None, 500)            
