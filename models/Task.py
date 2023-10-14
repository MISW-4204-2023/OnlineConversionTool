from datetime import datetime
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemySchema

from .Extensions import Extensions
from .Status import Status
from .Base import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    input_filename = db.Column(db.String(50), nullable=False)
    input_extension = db.Column(db.Enum(Extensions), nullable=False)
    output_filename = db.Column(db.String(50))
    output_extension = db.Column(db.Enum(Extensions))
    status = db.Column(db.Enum(Status), nullable=False, default=Status.UPLOADED)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class TaskSchema(SQLAlchemySchema):
    class Meta:
        model = Task
        include_relationships = True
        load_instance = True

    id = fields.Integer()
    created = fields.DateTime()
    input_filename = fields.String()
    output_filename = fields.String()
    input_extension = fields.Function(lambda obj: obj.rol.value)
    output_extension = fields.Function(lambda obj: obj.rol.value)
    status = fields.Function(lambda obj: obj.rol.value)
