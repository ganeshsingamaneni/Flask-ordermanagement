from marshmallow import fields, Schema
from marshmallow import fields, Schema
from marshmallow.validate import Length, Range
from config.config import db, ma
from models.roles import Roles


class RolesMapSchema(ma.ModelSchema):
    class Meta:
        model = Roles
        fields = ('id', "name")
        sqla_session = db.session