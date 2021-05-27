from marshmallow import fields, Schema
from config.config import db, ma
from models.users import Users
from marshmallow import fields, Schema

from marshmallow.validate import Length, Range
from schemas.roles_schema import GetAddRoleSchema

class UsersSchema(ma.ModelSchema):
    class Meta:
        model = Users
        sqla_session = db.session


class SuperAdminSignupSchema(ma.ModelSchema):
    class Meta:
        model = Users
        fields = ('id', "mobileNumber", "businessEmail", "roleId", "password","userName")
        sqla_session = db.session

class SignUpSchemaValidator(Schema):
    userName = fields.Str(required=True)
    mobileNumber = fields.Str(required=True)
    businessEmail = fields.Str(required=True)
    subscriberTitle = fields.Str(required=True)

class LoginValidator(Schema):
    businessEmail = fields.Str(required=True)
    password = fields.Str(required=True)


class AddUserSchema(ma.ModelSchema):
    class Meta:
        model = Users
        fields = ("id", "name", "mobileNumber", "businessEmail",  "roleId", "status", "password","userName")
        sqla_session = db.session


class GetUsersSchema(ma.ModelSchema):
    class Meta:
        model = Users
        fields = ("id", "name", "mobileNumber", "businessEmail","userName", "emailVerified",  "roleId", "status")
        sqla_session = db.session

class UserValidator(Schema):
    name = fields.Str(required=True)
    userName = fields.Str(required=True)
    mobileNumber = fields.Str(required=True)
    businessEmail = fields.Str(required=True)
    password = fields.Str(required=True)
    roleId = fields.Int(required=True)


class UserUpdateValidator(Schema):
    name = fields.Str(required=True)
    mobileNumber = fields.Str(required=True)
    businessEmail = fields.Str(required=True)
    subscriberId = fields.Int(required=True)
    roleId = fields.Int(required=True)


class NestedUserSchema(Schema):
    roles = ma.Nested(GetAddRoleSchema)
    class Meta:
        model = Users
        fields = ("id", "name", "mobileNumber", "businessEmail","userName",
                  "emailVerified", "roles", "status")
        sqla_session = db.session


class LoginNestedSchema(Schema):
    roles = ma.Nested(GetAddRoleSchema)

    class Meta:
        model = Users
        fields = ("id", "name", "mobileNumber", "businessEmail","userName",
                   "roles", "status", "password", "roleId")
        sqla_session = db.session


class GetUserNameSchema(ma.ModelSchema):
    class Meta:
        model = Users
        fields = ("id", "name")
        sqla_session = db.session

class UserForNotificationSchema(ma.ModelSchema):
    class Meta:
        model = Users
        fields = ("id", "name")
        sqla_session = db.session



