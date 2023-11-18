import os
from flask import request
from flask_restful import Resource
from flask_jwt_extended import current_user, jwt_required
from celery import Celery

from gcp.cloud_storage import BLOB_FORMAT, upload_to_bucket
from google.cloud import pubsub_v1
from .BaseView import upload_folder, task_schema
from models import db, Task, Formats, User


class TasksView(Resource):
    credentials_path = './cloud-uniandes-private-key.json'
    os.environ['GOOGLE_APLICATION_CREDENTIALS'] = credentials_path

    def publisher_gcp(self, data):
        publisher = pubsub_v1.PublisherClient()
        topic_path = 'projects/cloud-uniandes-403120/topics/conversion'
        data = data.encode('utf-8')
        future = publisher.publish(topic_path, data)
        print(future.result())

    def extract_extension(self, filename):
        return filename.rsplit(".", 1)[1]

    def extract_filename(self, filename):
        return filename.rsplit(".", 1)[0]

    def allowed_file(self, filename):
        return (
            "." in filename
            and self.get_format(self.extract_extension(filename)) is not None
        )

    def get_format(self, ext):
        return next((member for member in Formats if member.value == ext), None)

    @jwt_required()
    def get(self):
        params = request.args
        limit = params["max"] if params.__contains__("max") and params["max"] else None
        order = (
            params["order"]
            if params.__contains__("order") and params["order"]
            else None
        )
        if order is not None and int(order) == 1:
            tasks = (
                db.session.query(Task)
                .join(User, User.id == Task.user_id)
                .filter(User.id == current_user["sub"])
                .order_by(Task.id.desc())
                .limit(limit)
                .all()
            )
        elif order is not None and int(order) > 1:
            return "Ingrese un valor valido para order", 401
        else:
            tasks = (
                db.session.query(Task)
                .join(User, User.id == Task.user_id)
                .filter(User.id == current_user["sub"])
                .order_by(Task.id.asc())
                .limit(limit)
                .all()
            )
        resultado = [task_schema.dump(task) for task in tasks]
        return resultado

    @jwt_required()
    def post(self):
        if "inputFile" not in request.files:
            return "El archivo para la conversión es requerido", 400

        input_file = request.files["inputFile"]
        new_format = request.form["newFormat"]
        user_id = current_user["sub"]
        if input_file.filename == "":
            return "Nombre de archivo no válido", 400
        input_format = self.get_format(self.extract_extension(input_file.filename))
        if not self.allowed_file(input_file.filename):
            return "Formato de archivo de entrada no soportado", 400
        output_format = self.get_format(new_format)
        if self.get_format(new_format) is None:
            return "Formato de archivo de salida no soportado", 400

        new_task = Task(
            filename=self.extract_filename(input_file.filename),
            input_format=input_format,
            output_format=output_format,
            user_id=user_id,
        )
        db.session.add(new_task)
        db.session.commit()

        blob_name = BLOB_FORMAT.format(
            upload_folder, str(user_id), "input", new_task.id, input_format.value
        )
        upload_to_bucket(blob_name, input_file)
        self.publisher_gcp(str(new_task.id))
        return task_schema.dump(new_task)
