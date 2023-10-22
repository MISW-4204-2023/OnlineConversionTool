from flask_jwt_extended import jwt_required, current_user
from flask_restful import Resource
from models import db, Task, User
from .BaseView import task_schema



class TaskView(Resource):
    @jwt_required()
    def get(self, task_id):
        task = (
            db.session.query(Task)
            .join(User, User.id == Task.user_id)
            .filter(Task.id == task_id, User.id == current_user['sub'])
            .first_or_404('La tarea no existe para el usuario actual')
        )
        return task_schema.dump(task)
       
    @jwt_required()
    def delete(self, task_id):
        task = (
            db.session.query(Task)
            .join(User, User.id == Task.user_id)
            .filter(Task.id == task_id, Task.user_id == current_user["sub"])
            .first()
        )
        if task is None:
            return {"message": "La tarea no existe o no tienes permiso para eliminarla"}, 404
        else:
            db.session.delete(task)
            db.session.commit()
            return {"message": "Tarea eliminada exitosamente"}, 200
