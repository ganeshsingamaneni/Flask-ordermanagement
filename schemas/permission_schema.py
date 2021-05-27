from config.config import *
from models.permissions import Permission
from marshmallow import fields, Schema

from marshmallow.validate import Length, Range
from schemas.rolesmapping_schema import RolesMapSchema
from schemas.view_schema import LoginViewSchema

class GetAddPermissionSchema(ma.ModelSchema):
    class Meta:
        model = Permission
        fields = ('id', "roleId", "viewId", "createdBy", "updatedBy", "permissionLevel")
        sqla_session = db.session

class AddPermissionValidator(Schema):
    permissionLevel = fields.Str(required=True)
    createdBy = fields.Int(required=True)
    
    roleId = fields.Int(required=True)
    viewId = fields.Int(required=True)

class UpdatePermissionValidator(Schema):
    permissionLevel = fields.Str(required=True)
    updatedBy = fields.Int(required=True)
    
    # roleId = fields.Int(required=True)
    # viewId = fields.Int(required=True)


class LoginPermissionSchema(ma.ModelSchema):
    # permissionRoles = ma.Nested(RolesMapSchema)
    PermissionView = ma.Nested(LoginViewSchema)
    class Meta:
        model = Permission
        fields = ('id',"PermissionView" ,"createdBy", "updatedBy","permissionLevel")
        sqla_session = db.session

class PermissionSchema(ma.ModelSchema):
    # permissionRoles = ma.Nested(RolesMapSchema)
    PermissionView = ma.Nested(LoginViewSchema)
    class Meta:
        model = Permission
        fields = ('id' ,"permissionLevel","PermissionView")
        sqla_session = db.session


  