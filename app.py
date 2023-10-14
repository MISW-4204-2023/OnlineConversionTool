from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from sqlalchemy import create_engine
from views import LoginView, SignUpView, TaskView, TasksView
from models import db

import os

db_conn = os.environ.get(
    "DB_CONN", "postgresql://postgres:postgres@127.0.0.1:15432/oct"
)

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "a-super-secret-phrase"
app.config["SQLALCHEMY_DATABASE_URI"] = db_conn
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True

app_context = app.app_context()
app_context.push()
engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
db.session.configure(bind=engine)
db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(SignUpView, "/api/auth/signup")
api.add_resource(LoginView, "/api/auth/login")
api.add_resource(TasksView, "/api/tasks")
api.add_resource(TaskView, "/api/<int:task_id>")

jwt = JWTManager(app)


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user["id"]


@jwt.user_lookup_loader
def user_lookup_callback(_, jwt_data):
    return jwt_data


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
