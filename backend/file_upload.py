import os
import shutil
from fastapi import UploadFile
from pathlib import Path

UPLOAD_DIR = Path("backend/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".csv", ".xlsx"}

# This function saves file to the uploads folder
def save_uploaded_file(uploaded_file: UploadFile, save_as: str) -> str:
    ext = Path(uploaded_file.filename).suffix
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError("Unsupported file type")

    destination = UPLOAD_DIR / f"{save_as}{ext}"
    with destination.open("wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)

    return str(destination)

# Helper to list files by prefix
def list_uploaded_files(prefix: str = ""):
    return [f.name for f in UPLOAD_DIR.glob(f"{prefix}*")]

# Helper to delete uploaded file
def delete_uploaded_file(filename: str):
    file_path = UPLOAD_DIR / filename
    if file_path.exists():
        file_path.unlink()
        return True
    return False
