from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil

router = APIRouter()
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/upload/{file_type}")
def upload_file(file_type: str, file: UploadFile = File(...)):
    if file_type not in ["pnl", "invoice", "cvr"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
    dest = UPLOAD_DIR / f"{file_type}.csv"
    with open(dest, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"message": f"{file_type} uploaded successfully."}