import os
import shutil
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from agents.orchestrator import Orchestrator
from api.dependencies import get_orchestrator
from core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()

UPLOAD_DIR = "./data/docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_document(file:UploadFile = File(...),
                          orchestrator:Orchestrator = Depends(get_orchestrator)):
    
    allowed_extensions = {".txt", ".pdf", ".docx"}
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {ext}"
        )
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    logger.info(f"File uploaded | name={file.filename}")
    orchestrator.add_documents(file_path)


    return {
        "status": "success",
        "filename": file.filename,
        "message": "Document uploaded and indexed successfully"
    }
    

