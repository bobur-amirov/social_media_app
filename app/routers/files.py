import tempfile

from fastapi import APIRouter, Depends, UploadFile, File

MINIO_ACCESS_KEY = "hWsPsXVwT7SJQ9QM1TSx"
MINIO_SECRET_KEY = "lYQ892hXcU7KAVYsOPHn21ItTIBWl3rlGKTcrXGY"

router = APIRouter(prefix="/files", tags=["files"])

from minio import Minio

client = Minio("127.0.0.1:9000",
               access_key=MINIO_ACCESS_KEY,
               secret_key=MINIO_SECRET_KEY,
               secure=False
               )


@router.post("/")
def file_upload(file: UploadFile = File(...)):
    handler, path = tempfile.mkstemp(suffix=f"{file.filename.split('.')[-1]}")
    with open(path, "wb") as f:
        f.write(file.file.read())
    client.fput_object(
        'images', file.filename, path
    )

    return {'file': file.filename, 'message': "ok"}
