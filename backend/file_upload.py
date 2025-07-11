from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from pathlib import Path
import shutil

router = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload/{file_type}")
async def upload_file(file_type: str, file: UploadFile = File(...)):
    valid_types = {"pnl", "invoice", "cvr"}
    if file_type not in valid_types:
        return JSONResponse(status_code=400, content={"detail": "Invalid file type"})

    filename = f"{file_type}_{file.filename}"
    file_path = UPLOAD_DIR / filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": f"{file_type.upper()} file uploaded successfully!"}
