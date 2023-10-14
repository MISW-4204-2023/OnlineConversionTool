from flask_jwt_extended import jwt_required
from flask_restful import Resource


class TaskView(Resource):
    @jwt_required()
    def get(self, task_id):
        return "No implementado", 500

    @jwt_required()
    def delete(self, task_id):
        return "No implementado", 500
