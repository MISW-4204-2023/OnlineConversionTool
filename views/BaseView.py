import os
from models import (
    TaskSchema,
    UserSchema
)


task_schema = TaskSchema()
upload_folder = os.environ.get("UPLOAD_FOLDER", "files")
user_schema = UserSchema()