import datetime
from config.config import db

# choices = [0,1,2]

# Permission Details model

class Permission(db.Model):
    __tablename__ = "permissions"

    """
    Represents Permissions 

    field id: Primary key
    type id: Integer
    
    """
    id = db.Column(db.Integer, primary_key=True)
    permissionLevel = db.Column(db.Enum("0","1","2"),nullable=True)
    roleId= db.Column(db.Integer, db.ForeignKey("roles.id"))
    viewId = db.Column(db.Integer, db.ForeignKey("views.id"))
    status = db.Column(db.Boolean, default=True)
    createdBy = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=True)
    updatedBy = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=True)
    createdAt = db.Column(db.DateTime,default=datetime.datetime.utcnow())
    updatedAt =  db.Column(db.DateTime, default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())
