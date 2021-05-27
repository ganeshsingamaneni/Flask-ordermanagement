from flask import request
from config.config import db
from config.logger import Logger
# from seeder.seed import seedRoles
from models.roles import Roles
from schemas.roles_schema import GetAddRoleSchema
from flask_restful import Resource
from models.permissions import Permission
from schemas.permission_schema import PermissionSchema
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)



class GetAddRoles(Resource):
    # def __init__(self):
        # pass
    # Roles get call
    # @jwt_required
    def get():
        try:
            obj = db.session.query(Roles).order_by(Roles.id).all()
            if obj:
                schema = GetAddRoleSchema(many=True)
                data = schema.dump(obj).data
                return {"success":True,"data":data}
            else:
                return {"success":False,"message":"No data found"}
        except Exception as e:
            Logger.create_error_log("getaddroles", str(e))
            return {"success":False,"message":str(e)}

    # Roles post call
    # @jwt_required
    def post():
        try:
            # current_user = get_jwt_identity()
            request_json_data = request.get_json()
            is_exist = db.session.query(Roles).filter(Roles.name == request_json_data['name']).first()
            if is_exist:
                return {"success": False,"message":"Role  already exists"}
            schema = GetAddRoleSchema()
            obj = schema.load(
                request_json_data, session=db.session).data
            db.session.add(obj)
            db.session.commit()
            data = schema.dump(obj).data
            return {"success":True,"data":data}
        except Exception as e:
            Logger.create_error_log("getaddroles", str(e))
            return {"success":False,"message":str(e)}


class GetUpdateRoles(Resource):
    def __init__(self):
        pass

    # Roles get call based on id
    def get(self, id):
        try:
            obj = Roles.query.filter(Roles.id == id).one_or_none()
            if obj is not None:
                schema = GetAddRoleSchema()
                data = schema.dump(obj).data
                return Response.return_response('success', data, 200)
            else:
                return Response.return_response('success', [], 200,"No data found")
        except Exception as e:
            Logger.create_error_log("getupdateroles", str(e))
            return Response.return_response('Error', None, 500)



    # call to update the roles based on roles_id

    @jwt_required
    def put(self, id):
        try:
            current_user = get_jwt_identity()
            request_json_data= request.get_json()
            role_exist = RoleUtility.check_updatecall_role_name_exist(
                request_json_data['name'], current_user['subscriberId'], id)
            if role_exist:
                return Response.return_response('Error', {}, 200,"Role already exists")
            obj = db.session.query(Roles).filter_by(id = id).update(request_json_data)
            if obj:
                db.session.commit()
                roles_obj = Roles.query.filter(Roles.id == id).one()
                role_schema = GetAddRoleSchema()
                data = role_schema.dump(roles_obj).data
                return Response.return_response('success', data, 200)
            else:
                return Response.return_response('success', [], 200,"No data found")
        except Exception as e:
            Logger.create_error_log("getupdateroles", str(e))
            return Response.return_response('Error', None, 500)


class RolesSeed(Resource):
    '''
    call to seed the role data
    '''
    def get(self):
        try:
            a = seedRoles()
            if a:
                return Response.return_response('success',[],200,"Roles seeded")
            return Response.return_response('success',[],200,'no data seeded')
        except Exception as e:
            # Logger.create_error_log("getupdateroles", str(e))
            return Response.return_response('Error', None, 500)  


class GetSubscriberRoles(Resource):
    def __init__(self):
        pass
    # Roles get call
    @jwt_required
    def get(self):
        try:
            current_user = get_jwt_identity()
            obj = db.session.query(Roles).filter(Roles.subscriberId==current_user['subscriberId']).all()
            if obj:
                schema = GetAddRoleSchema(many=True)
                data = schema.dump(obj).data
                return Response.return_response('success', data, 200)
            else:
                return Response.return_response('success', [], 200,"No data found")
        except Exception as e:
            Logger.create_error_log("getaddroles", str(e))
            return Response.return_response('Error', None, 500)                  
