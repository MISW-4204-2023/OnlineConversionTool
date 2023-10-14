import os
from models import TaskSchema


task_schema = TaskSchema()
upload_folder = os.environ.get("UPLOAD_FOLDER", "files")
