from fastapi import APIRouter, UploadFile, File
import os

router = APIRouter()

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload/{file_type}")
async def upload_file(file_type: str, file: UploadFile = File(...)):
    save_path = os.path.join(UPLOAD_DIR, f"{file_type}_{file.filename}")
    with open(save_path, "wb") as f:
        f.write(await file.read())
    return {"message": f"{file_type} report uploaded successfully!"}
