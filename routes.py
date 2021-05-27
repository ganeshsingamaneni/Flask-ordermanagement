from controllers.user_signin_controller import UserSignin, Logout, TokenRefresh
from flask import Flask
from flask_restful import Resource, Api
from config import config
from controllers.roles_controller import GetAddRoles, GetUpdateRoles
from controllers.user_controller import *

from controllers.permission_controller import GetAddPermission, GetUpdatePermission,PermissionsByRole

from controllers.roles_controller import RolesSeed, GetSubscriberRoles


app = config.app
api = Api(app)

api.add_resource(GetAddRoles, '/api/roles')
api.add_resource(GetUpdateRoles, '/api/roles/<int:id>')
api.add_resource(GetSubscriberRoles,"/api/subscriberroles")


api.add_resource(UserSignin, '/api/signin')
api.add_resource(TokenRefresh, '/api/tokenrefresh')
api.add_resource(Logout, '/api/logout')
api.add_resource(GetAddUsers, '/api/users')
api.add_resource(GetUpdateUsers, '/api/users/<int:id>')
api.add_resource(ChangeUserPassword, '/api/changepassword/<int:id>')
api.add_resource(UserOutlets,'/api/useroutlets/<int:id>')
api.add_resource(UpdateUserStatus, '/api/userstatus/<int:id>')
api.add_resource(UserStatusFilter, '/api/filteruserstatus')



api.add_resource(GetAddPermission, '/api/permission')
api.add_resource(GetUpdatePermission, '/api/permission/<int:id>')
api.add_resource(PermissionsByRole,"/api/permissionsbyrole/<int:id>")


api.add_resource(RolesSeed,'/api/seedroles')





