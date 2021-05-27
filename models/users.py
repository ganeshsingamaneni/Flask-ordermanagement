import datetime
from config.config import db
from sqlalchemy.orm import validates

# Users Details  model


class Users(db.Model):
    __tablename__ = "users"

    """
    Represents users 

    field id: Primary key
    type id: Integer
    

    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(220), nullable=True)
    userName = db.Column(db.String(220), nullable=True,unique=True)
    password = db.Column(db.String(220), nullable=True)
    mobileNumber = db.Column(db.String(10), nullable=False)
    businessEmail = db.Column(db.String(220), nullable=False)
    roleId = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    status = db.Column(db.Boolean, default=True)
    createdAt = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updatedAt = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)

    

    @validates('businessEmail')
    def validate_email(self, key, address):
        assert '@' in address
        return address
