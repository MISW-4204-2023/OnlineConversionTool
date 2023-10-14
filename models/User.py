from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemySchema

from models.Task import TaskSchema

from .Base import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    email = db.Column(db.String(50))
    tasks = db.relationship("Task", cascade="all, delete, delete-orphan")
    __table_args__ = (
        db.UniqueConstraint("email", name="email_unique"),
    )

class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True

    id = fields.Integer()
    user = fields.String()
    email = fields.String()
    tasks = fields.List(fields.Nested(TaskSchema()))
