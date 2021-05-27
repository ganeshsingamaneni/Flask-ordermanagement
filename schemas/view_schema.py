from marshmallow import fields, Schema
from config.config import db, ma
from models.views import View
from marshmallow.validate import Length, Range

class GetAddViewSchema(ma.ModelSchema):
    class Meta:
        model = View
        fields = ('id', "name", "createdBy","aliyasName", "updatedBy")
        sqla_session = db.session

class AddViewValidator(Schema):
    name = fields.Str(required=True)
    createdBy = fields.Int(required=True)

class UpdateViewValidator(Schema):
    name = fields.Str(required=True)
    updatedBy = fields.Int(required=True)

class LoginViewSchema(ma.ModelSchema):
    class Meta:
        model = View
        fields = ('id', "name", "aliyasName", "description")
        sqla_session = db.session