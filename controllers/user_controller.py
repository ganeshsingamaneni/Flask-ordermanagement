import datetime
import random
import string
import jwt,json
import short_url
import requests
from flask import request
from flask_restful import Resource
from werkzeug.security import generate_password_hash
from config.config import *
from sqlalchemy import and_
from config.logger import Logger
from models.roles import Roles
from schemas.roles_schema import GetAddRoleSchema
from models.users import Users
from models.userToken import UserToken
from models.revokeToken import BlockTokenModel
from schemas.users_schema import SuperAdminSignupSchema, SignUpSchemaValidator, GetUsersSchema, UserValidator, AddUserSchema, UserUpdateValidator, NestedUserSchema

from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)




class GetAddUsers(Resource):
    def __init__():
        pass
    # Users get call
    # @jwt_required
    def get():
        try:
            # current_user = get_jwt_identity()
            obj = db.session.query(Users).order_by(Users.id.desc()).all()
            if obj:
                schema = AddUserSchema(many=True)
                data = schema.dump(obj).data
                
                return {"success":True,"data":data}
            else:
                return {"success":True,"message":"No data found"}
        except Exception as e:
            Logger.create_error_log("getaddusers", str(e))
            return {"success":False,"message":str(e)}

    # @jwt_required
    def post():
        try:
            # current_user = get_jwt_identity()
            request_json_data = request.get_json()
            validate_schema = UserValidator()
            errors = validate_schema.validate(request_json_data)
            if errors:
                return {"success": False,"messge":"Bad Request"}
            # mobilemail_exist = UserUtility.check_email_mobile(request_json_data['businessEmail'], request_json_data["mobileNumber"],current_user['subscriberId'],request_json_data['userName'])
            # if mobilemail_exist["mobile"] == True and mobilemail_exist["email"] == True:
            #     return Response.return_response('Error', {}, 200,"Mobile number and Email already exists")
            # if mobilemail_exist["email"] == True:
            #     return Response.return_response('Error', {}, 200,"Email already exists")
            # if mobilemail_exist["mobile"] == True:
            #     return Response.return_response('Error', {}, 200,"Mobile already exists")
            # if mobilemail_exist["userName"] == True:
            #     return Response.return_response('Error', {}, 200,"UserName already exists")    
            request_json_data['password'] = generate_password_hash(
                request_json_data['password'])
            schema = AddUserSchema()
            obj = schema.load(
                request_json_data, session=db.session).data
            db.session.add(obj)
            db.session.commit()
            data = schema.dump(obj).data
            return {"success":True,"data":data}  

        except Exception as e:
            Logger.create_error_log("getaddusers", str(e))
            return {"success":False,"message":str(e)}


class GetUpdateUsers(Resource):
    def __init__(self):
        pass

    # Users get call based on id
    def get(self, id):
        try:
            obj = Users.query.filter(Users.id == id).one_or_none()
            if obj is not None:
                schema = NestedUserSchema()
                data = schema.dump(obj).data
                return Response.return_response('success', data, 200)
            else:
                return Response.return_response('success', [], 200,"No data found")
        except Exception as e:
            Logger.create_error_log("getupdateusers", str(e))
            return Response.return_response('Error', None, 500)



    # Users update call
    @jwt_required
    def put(self, id):
        try:
            current_user = get_jwt_identity()
            request_json_data= request.get_json()
            request_json_data["subscriberId"] = current_user["subscriberId"]
            user_obj = db.session.query(Users).filter_by(id = id).first()
            if user_obj:
                validate_schema = UserUpdateValidator()
                errors = validate_schema.validate(request_json_data)
                if errors:
                    return Response.return_response('error', str(errors), 400,"Bad Request")
                mobilemail_exist = UserUtility.check_mobile_email_for_update(request_json_data['businessEmail'], request_json_data["mobileNumber"], id,current_user['subscriberId'], request_json_data['userName'])
                if mobilemail_exist["mobile"] == True and mobilemail_exist["email"] == True:
                    return Response.return_response('Error', {}, 200,"Mobile number and Email already exists")
                if mobilemail_exist["email"] == True:
                    return Response.return_response('Error', {}, 200,"Email already exists")
                if mobilemail_exist["mobile"] == True:
                    return Response.return_response('Error', {}, 200,"Mobile already exists")
                if mobilemail_exist["userName"] == True:
                        return Response.return_response('Error', {}, 200,"UserName already exists")
                outlets = request_json_data["newoutlets"]
                checkuser = UserUtility.checkUserExistInOutlet(id, outlets, current_user["subscriberId"],request_json_data["deleteoutlets"])
                if checkuser:
                    return Response.return_response('Error', {}, 200, "Adding the same existing outlet to this User")
                deletedoutlets = request_json_data["deleteoutlets"]
                del request_json_data["newoutlets"]
                del request_json_data["deleteoutlets"]
                useroutletids = []
                try: 
                    for each in outlets:
                        input_data = {"userId": id, "outletId": each, "subscriberId": current_user["subscriberId"], "createdBy": current_user["userId"]}
                        map_schema = AddUserOutletSchema()
                        map_obj = map_schema.load(
                            input_data, session=db.session).data
                        db.session.add(map_obj)
                        db.session.commit()
                        useroutletids.append(map_obj.id)
                    obj = db.session.query(Users).filter_by(id = id).update(request_json_data)
                    deletedobjects = UserOutletMapping.__table__.delete().where(UserOutletMapping.id.in_(deletedoutlets))
                    db.session.execute(deletedobjects)
                except Exception as e:
                    db.session.rollback()
                    deleted_objects = UserOutletMapping.__table__.delete().where(UserOutletMapping.id.in_(useroutletids))
                    db.session.execute(deleted_objects)
                    db.session.commit()
                    Logger.create_error_log("getupdateusers", str(e))
                    return Response.return_response('Error', None, 500)
                db.session.commit()
                # user_obj = Users.query.filter(Users.id == id).one()
                # user_schema = GetUsersSchema()
                # data = user_schema.dump(user_obj).data
                return Response.return_response('success', {}, 200, "User updated successfully")
            else:
                return Response.return_response('Error', {}, 200,"No data found")
        except Exception as e:
            Logger.create_error_log("getupdateusers", str(e))
            return Response.return_response('Error', None, 500)


class ChangeUserPassword(Resource):
    def __init__(self):
        pass

    # Change User Password
    def put(self,id):
        try:
            request_json_data= request.get_json()
            request_json_data['password'] = generate_password_hash(
                request_json_data['password'])
            obj = db.session.query(Users).filter_by(id = id).update(request_json_data)
            if obj:
                db.session.commit()
                user_obj = Users.query.filter(Users.id == id).one()
                user_schema = GetUsersSchema()
                data = user_schema.dump(user_obj).data
                return Response.return_response('success', data, 200)
            else:
                return Response.return_response('Error', [], 200, "No data found")
        except Exception as e:
            Logger.create_error_log("changeuserpassword", str(e))
            return Response.return_response('Error', None, 500)


class ResetPassword(Resource):
    def __init__(self):
        pass

    # User Reset Password
    def post(self):
        try:
            pass
        except Exception as e:
            # logger.create_error_log('getupdateusers', str(e))
            return Response.return_response('Error', None, )



class UserOutlets(Resource):
    def __init__(self):
        pass

    # call to get user outlet data based on user id
    @jwt_required
    def get(self,id):
        try:
            current_user = get_jwt_identity()
            obj = db.session.query(UserOutletMapping).filter(and_(UserOutletMapping.userId==id,UserOutletMapping.subscriberId==current_user['subscriberId'], UserOutletMapping.status == True)).all()
            if obj:
                schema = GetUserOutletSchema(many=True)
                data = schema.dump(obj).data
                return Response.return_response('success', data, 200)
            else:
                return Response.return_response('success', [], 200, "No data found")
        except Exception as e:
            Logger.create_error_log("UserOutlets", str(e))
            return Response.return_response('Error', None, 500)


class UpdateUserStatus(Resource):
    def __init__(self):
        pass

    @jwt_required
    def put(self, id):
        try:
            current_user = get_jwt_identity()
            req_data = request.get_json()
            req_data.update({"subscriberId": current_user["subscriberId"]})
            obj = db.session.query(Users).filter(Users.id == id).update(req_data)
            if obj:
                useroutletobj = db.session.query(UserOutletMapping).filter(UserOutletMapping.userId == id).update(req_data)
                usertokenobj = db.session.query(UserToken).filter(UserToken.userId == id).one_or_none()
                if usertokenobj:
                    try:
                        payload = jwt.decode(usertokenobj.token, 'ILOVECARATRED',)
                        jti = payload["jti"]
                        revoked_token = BlockTokenModel(jti=jti)
                        revoked_token.add()
                        usertoken_obj = UserToken.query.filter_by(userId = id).delete()
                    except jwt.ExpiredSignature:
                        usertoken_obj = UserToken.query.filter_by(userId = id).delete()
                db.session.commit()
                return Response.return_response('success', {}, 200, "User status updated Successfully")
            else:
                return Response.return_response('success', {}, 200, "No data found")
        except Exception as e:
            Logger.create_error_log("UserOutlets", str(e))
            return Response.return_response('Error', None, 500)


class UserStatusFilter(Resource):
    def __init__(self):
        pass

    @jwt_required
    def get(self):
        try:
            current_user = get_jwt_identity()
            status = request.args.get('status')
            obj = db.session.query(Users).filter(Users.status == status, Users.subscriberId == current_user["subscriberId"]).order_by(Users.id.desc()).all()
            if obj:
                schema = NestedUserSchema(many=True)
                data = schema.dump(obj).data
                for x in data:
                    if len(x["outletmapping"]) > 0:
                        useroutletmap = []
                        for outlets in x["outletmapping"]:
                            if outlets["status"] == True:
                                useroutletmap.append(outlets)
                        x["outletmapping"] = useroutletmap
                return Response.return_response('success', data, 200)
            else:
                return Response.return_response('success', [], 200, "No data found")
        except Exception as e:
            Logger.create_error_log("UserStatusFilter", str(e))
            return Response.return_response('Error', None, 500)



# commented code

# try:
#     role_schema = GetAddRoleSchema()
#     role_data = {"name": "S-Admin", "subscriberId": subscriber_data["id"]}
#     role_obj = role_schema.load(role_data, session=db.session).data
#     db.session.add(role_obj)
#     db.session.commit()
#     roledata = role_schema.dump(role_obj).data
# except Exception as e:
#     db.session.rollback()
#     Subscribers.query.filter_by(
#         id=subscriber_data["id"]).delete()
#     db.session.commit()
#     return Response.return_response('Error', None, 500)
# if roledata:
#     try:
#         add_permissions = PermissionUtility.createPermissions(viewdata["Permission_Data"],subscriber_data['id'],roledata['id'])
#         if add_permissions['success'] == True:
#             pass
#         else:
#             return Response.return_response('Error',None,500)
#     except Exception as e:
#         db.session.rollback()
#         Subscribers.query.filter_by(
#             id=subscriber_data["id"]).delete()
#         db.session.commit()
#         return Response.return_response('Error', None, 500)
