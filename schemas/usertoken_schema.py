from marshmallow import fields, Schema
from marshmallow.validate import Length, Range

from config.config import db, ma
from models.userToken import UserToken


class GetUserTokenSchema(ma.ModelSchema):
    class Meta:
        model = UserToken
        fields = ("id", "userId", "token")
        sqla_session = db.session
