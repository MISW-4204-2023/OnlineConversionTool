from datetime import datetime
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemySchema

from .Formats import Formats
from .Status import Status
from .Base import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    filename = db.Column(db.String(50), nullable=False)
    input_format = db.Column(db.Enum(Formats), nullable=False)
    output_format = db.Column(db.Enum(Formats))
    processed = db.Column(db.DateTime)
    inprocess = db.Column(db.DateTime)
    status = db.Column(db.Enum(Status), nullable=False, default=Status.UPLOADED)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class TaskSchema(SQLAlchemySchema):
    class Meta:
        model = Task
        include_relationships = True
        load_instance = True

    id = fields.Integer()
    created = fields.DateTime()
    processed = fields.DateTime()
    inprocess = fields.DateTime()
    filename = fields.String()
    input_file = fields.Function(lambda obj: "/files/input/{}".format(obj.id))
    output_file = fields.Function(
        lambda obj: "/files/output/{}".format(obj.id)
        if obj.status == Status.PROCESSED
        else None
    )
    status = fields.Function(lambda obj: obj.status.value)
