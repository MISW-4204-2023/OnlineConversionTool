from flask_restful import Resource
from flask_jwt_extended import jwt_required

class TasksView(Resource):
    @jwt_required()
    def get(self):
        return "No implementado", 500

    @jwt_required()
    def post(self):
        return "No implementado", 500
