import os
from flask import send_file
from flask_restful import Resource

from models import Task, db
from .BaseView import upload_folder


class FilesView(Resource):
    # @jwt_required()
    def get(self, type, task_id):
        user_id = 1  ##TODO change user id
        task = db.session.query(Task).filter_by(id=task_id, user_id=user_id).first()
        if task is not None and (type == "input" or type == "output"):
            file_name = os.path.join(
                upload_folder,
                str(user_id),
                type,
                "{}.{}".format(
                    task.id,
                    task.input_format.value
                    if type == "input"
                    else task.output_format.value,
                ),
            )
            return send_file(file_name, as_attachment=True)
        else:
            return "Archivo no encontrado", 404
