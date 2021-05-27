import datetime
from config.config import db
from models.permissions import Permission

# Views Details model


class View(db.Model):
    __tablename__ = "views"

    """
    Represents views 

    field id: Primary key
    type id: Integer
    

    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(220), nullable=False)
    aliyasName = db.Column(db.String(220), nullable = False)
    description = db.Column(db.String(220), nullable = True)
    status = db.Column(db.Boolean, default=True)
    createdBy = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=True)
    updatedBy = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=True)
    createdAt = db.Column(db.DateTime,default=datetime.datetime.utcnow())
    updatedAt =  db.Column(db.DateTime, onupdate=datetime.datetime.utcnow())


    viewPermission = db.relationship(
        "Permission", backref=db.backref("PermissionView"), uselist=False)

