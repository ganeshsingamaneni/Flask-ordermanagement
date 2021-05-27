from marshmallow import fields, Schema
from marshmallow import fields, Schema
from marshmallow.validate import Length, Range
from config.config import db, ma
from models.roles import Roles
from schemas.permission_schema import PermissionSchema


class GetAddRoleSchema(ma.ModelSchema):
    class Meta:
        model = Roles
        fields = ('id', "name", "type")
        sqla_session = db.session


class ViewPermissionRoleSchme(ma.ModelSchema):
    permissions = ma.Nested(PermissionSchema,many=True)
    class Meta:
        fields = ("id", "permissions", "name", "type")
        model = Roles
        sqla_session = db.session 
