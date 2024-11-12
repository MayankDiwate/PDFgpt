from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from sqlalchemy.orm import Session

from db.crud import create_document
from db.base import get_db
from services.pdf_processing import extract_text_from_pdf
from schemas.document import DocumentCreate
from db.models import Document

# Initialize APIRouter instance
router = APIRouter()

@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    if file.size > 20 * 1024 * 1024:  # 20 MB size limit
        raise HTTPException(status_code=400, detail="PDF file size limit exceeded.")
    
    # Check if a document with the same name already exists in the database
    existing_document = db.query(Document).filter(Document.name == file.filename).first()

    if existing_document:
        # Document already exists, return it
        return existing_document

    # Document does not exist, proceed with extracting text and saving
    pdf_text = await extract_text_from_pdf(file)

    # Prepare and save new document data
    document_data = DocumentCreate(name=file.filename, content=pdf_text)
    db_document = create_document(db, document_data)

    return db_document
