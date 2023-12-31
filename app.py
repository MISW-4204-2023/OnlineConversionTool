import signal
import sys
from types import FrameType
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from sqlalchemy import create_engine
from views import FilesView, LoginView, SignUpView, TaskView, TasksView
from models import User, db

from utils.logging import logger

import os

def add_initial_data():
    user = User.query.first()
    if not user:
        user = User(
            username="oscar", password="password", email="o.buitragov@uniandes.edu.co"
        )
        db.session.add(user)
        db.session.commit()
        
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
add_initial_data()

api = Api(app)
api.add_resource(SignUpView, "/api/auth/signup")
api.add_resource(LoginView, "/api/auth/login")
api.add_resource(TasksView, "/api/tasks")
api.add_resource(TaskView, "/api/tasks/<int:task_id>")
api.add_resource(FilesView, "/files/<string:type>/<int:task_id>")

@app.route('/health', methods=['GET'])
def health_check():
    return 'OK', 200

jwt = JWTManager(app)



@jwt.user_identity_loader
def user_identity_lookup(user):
    return user["id"]


@jwt.user_lookup_loader
def user_lookup_callback(_, jwt_data):
    return jwt_data


def shutdown_handler(signal_int: int, frame: FrameType) -> None:
    logger.info(f"Caught Signal {signal.strsignal(signal_int)}")

    from utils.logging import flush

    flush()

    # Safely exit program
    sys.exit(0)


if __name__ == "__main__":
    # Running application locally, outside of a Google Cloud Environment

    # handles Ctrl-C termination
    signal.signal(signal.SIGINT, shutdown_handler)

    app.run(host="localhost", port=8080, debug=True)
else:
    # handles Cloud Run container termination
    signal.signal(signal.SIGTERM, shutdown_handler)