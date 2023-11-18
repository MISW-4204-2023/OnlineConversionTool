import io
import os
from google.cloud import storage


bucket_name = os.environ.get("BUCKET_NAME", "proyecto-conversion")
credentials_path = './cloud-uniandes-private-key.json'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
storage_client = storage.Client()

BLOB_FORMAT = "{}/{}/{}/{}.{}"


def upload_to_bucket(blob_name, file):
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_file(file)
        return True
    except Exception as e:
        print(e)
        return False


def download_file_from_bucket(blob_name):
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        download_file = io.BytesIO()
        blob.download_to_file(download_file)
        download_file.seek(0)

        return download_file
    except Exception as e:
        print(e)
        return None
