import datetime
from config.config import db
from models.users import Users
from models.permissions import Permission


# Roles Details Model


class Roles(db.Model):
    __tablename__ = "roles"

    """
    Represents Roles 

    field id: Primary key
    type id: Integer
    

    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(220), nullable=False)
    type = db.Column(db.Boolean, default=False)
    status = db.Column(db.Boolean, default=True)
    createdAt = db.Column(db.DateTime,default=datetime.datetime.utcnow())
    updatedAt =  db.Column(db.DateTime, onupdate=datetime.datetime.utcnow())

    user_roles = db.relationship(
        "Users", backref=db.backref('roles'), uselist=False)

    rolePermission = db.relationship(
        "Permission", backref=db.backref('permissionRoles'), uselist=False)    

    permissions =  db.relationship(
        "Permission", backref=db.backref('permission_roles2'), uselist=True)    
