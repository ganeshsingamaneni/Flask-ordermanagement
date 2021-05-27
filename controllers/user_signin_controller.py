import datetime
import jwt
from flask import request, session
from flask_restful import Resource
from werkzeug.security import check_password_hash
from config.config import *
from config.logger import Logger
from config.jwt import encode_auth_token, jwt_token,jwt_response_token
from models.users import Users
from schemas.users_schema import SignUpSchemaValidator, LoginValidator,LoginNestedSchema
from models.revokeToken import BlockTokenModel
from models.permissions import Permission
from models.userToken import UserToken
from models.revokeToken import BlockTokenModel
from schemas.permission_schema import LoginPermissionSchema
from schemas.usertoken_schema import GetUserTokenSchema
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

class UserSignin(Resource):
    def __init__(self):
        pass

    def post(self):
        # try:
        request_json_data = request.get_json()
        validate_schema = LoginValidator()
        errors = validate_schema.validate(request_json_data)
        # if '@' in request_json_data['businessEmail']:
        #     userNameType = businessEmail
        # else:
        #     userNameType = 'userName'
        if errors:
            return{"success":False,"message":"Bad Request"}
        check_user_exist = db.session.query(Users).filter(Users.businessEmail == request_json_data['businessEmail']).first()
        # have to check portal
        print(check_user_exist,"/////////")
        if check_user_exist != False:
            schema = LoginNestedSchema()
            check_user_exist = schema.dump(check_user_exist).data

            checkuserstatus = db.session.query(Users).filter(Users.businessEmail == request_json_data['businessEmail'], Users.status == False).first()
            if checkuserstatus:
                return {"success": False,"message":"You can't have right to login"}
            # password_check = db.session.query(Users.password).filter(Users.id == id).first()
            # if password_check[0]== None:
            #     return {"success": False,"message":'Please set your password'}
            if check_password_hash(check_user_exist['password'], request_json_data['password']):
                # token = jwt_token(check_user_exist['id'],check_user_exist['subscriberId'])
                # check_user_exist['access_token'] = token['accessToken']
                # check_user_exist['refresh_token'] = token['refreshToken']
                del check_user_exist["password"]
                # # permissionObj = db.session.query(Permission).filter(Permission.roleId==check_user_exist['roleId']).all()
                # if permissionObj:
                #     perSchema = LoginPermissionSchema(many=True)
                #     permissionData = perSchema.dump(permissionObj).data
                #     check_user_exist['permissions'] = permissionData
                token = jwt_token(check_user_exist,check_user_exist['id'])
                data = {}
                data['access_token'] = token['accessToken']
                data["refresh_token"] = token["refreshToken"]

                tokenobj = db.session.query(UserToken).filter(UserToken.userId == check_user_exist['id']).one_or_none()
                if tokenobj:
                    usertokenupdate = db.session.query(UserToken).filter(UserToken.userId == check_user_exist["id"]).update({"token": token['accessToken']})
                    db.session.commit()
                else:
                    schema = GetUserTokenSchema()
                    token_obj = schema.load({"userId":check_user_exist["id"], "token": token['accessToken']}, session=db.session).data
                    db.session.add(token_obj)
                    db.session.commit()
                return {"success":True,"message":'Login successfully',"data":data}
            return {"success":False,"message":'Incorrect username or password'}
        return {"success":False,"message":'Incorrect username or password'}
        # except Exception as e:
        #     Logger.create_error_log("usersignin", str(e))
        #     return {"success":False,"message":str(e)}


class TokenRefresh(Resource):

    def get(self):
        ''' 
        create access token using refresh token
        
        '''
        try:
            current_user = request.headers.get('refreshtoken')
            payload = jwt.decode(current_user, 'ILOVECARATRED',)
            access_expires = datetime.timedelta(hours=24)
            access_token = create_access_token(identity=payload["identity"],expires_delta=access_expires)
            return Response.return_response("success", {"access_token": access_token}, "access token")
        except jwt.ExpiredSignature:
            return Response.return_response('Error', {}, 401, "Token Expired")
        except Exception as e:
            Logger.create_error_log("TokenRefresh", str(e))
            return Response.return_response('Error', {}, 500)

class Logout(Resource):
    @jwt_required
    def get(self):
        try:
            jti = get_raw_jwt()['jti']
            revoked_token = BlockTokenModel(jti=jti)
            revoked_token.add()
            return{'success':True, "message":"Successfully logged out"}
        except Exception as e:
            Logger.create_error_log("Logout", str(e))
            return {'success':False, "message":str(e)}
