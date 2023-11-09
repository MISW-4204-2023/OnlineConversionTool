import os
from flask import send_file
from flask_restful import Resource
from gcp.cloud_storage import BLOB_FORMAT, download_file_from_bucket

from models import Task, db
from .BaseView import upload_folder
from flask_jwt_extended import current_user, jwt_required


class FilesView(Resource):
    @jwt_required()
    def get(self, type, task_id):
        user_id = current_user["sub"]
        task = db.session.query(Task).filter_by(id=task_id, user_id=user_id).first()
        if task is not None and (type == "input" or type == "output"):
            format_task = (
                task.input_format.value if type == "input" else task.output_format.value
            )

            blob_name = BLOB_FORMAT.format(
                upload_folder, str(user_id), type, task.id, format_task
            )

            return send_file(
                download_file_from_bucket(blob_name),
                download_name="{}.{}".format(task.filename, format_task),
                as_attachment=True,
            )
        else:
            return "Archivo no encontrado", 404
