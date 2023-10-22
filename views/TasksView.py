import os
from flask import request
from flask_restful import Resource
from flask_jwt_extended import current_user ,jwt_required
from celery import Celery
from .BaseView import upload_folder, task_schema
from models import db, Task, Formats, User

broker = os.environ.get("REDIS_CONN", "redis://localhost:6379/0")
celery = Celery("tasks", broker=broker)

@celery.task(name="process_video")
def process_video(*args):
    pass


class TasksView(Resource):
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
        limit = params['max'] or None
        order = params['order'] or None 
        if order is not None and int(order)  == 1:
            print('entro 1')
            tasks = (
                db.session.query(Task)
                .join(User, User.id == Task.user_id)
                .filter(User.id == current_user['sub'] )
                .order_by(Task.id.desc())
                .limit(limit)
                .all()
            )
        elif order is not None and int(order) > 1:
            return 'Ingrese un valor valido para order', 401
        else:
            tasks = (
                db.session.query(Task)
                .join(User, User.id == Task.user_id)
                .filter(User.id == current_user['sub'] )
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
        user_id = current_user['sub'] 
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

        os.makedirs(os.path.join(upload_folder, str(user_id), "input"), exist_ok=True)
        input_file_path = os.path.join(
            upload_folder,
            str(user_id),
            "input",
            "{}.{}".format(new_task.id, input_format.value),
        )
        input_file.save(input_file_path)
        args = (new_task.id,)
        process_video.apply_async(args=args)
        return task_schema.dump(new_task)
