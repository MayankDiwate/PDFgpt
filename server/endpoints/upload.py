from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from sqlalchemy.orm import Session
import logging
from db.crud import create_document
from db.base import get_db
from services.pdf_processing import extract_text_from_pdf
from schemas.document import DocumentCreate
from db.models import Document

# Initialize APIRouter instance
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # Check file extension
        if not file.filename.endswith(".pdf"):
            logger.warning("Attempted to upload a non-PDF file: %s", file.filename)
            raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        
        # Check file size (20 MB limit)
        if file.size > 20 * 1024 * 1024:
            logger.warning("File size limit exceeded for file: %s", file.filename)
            raise HTTPException(status_code=400, detail="PDF file size limit exceeded.")
        
        # Check if document with the same name exists
        existing_document = db.query(Document).filter(Document.name == file.filename).first()
        if existing_document:
            logger.info("Document with name %s already exists in database.", file.filename)
            return existing_document
        
        # Extract text from PDF
        pdf_text = await extract_text_from_pdf(file)
        
        # Prepare and save new document data
        document_data = DocumentCreate(name=file.filename, content=pdf_text)
        db_document = create_document(db, document_data)

        logger.info("New document %s saved to database successfully.", file.filename)
        return db_document

    except HTTPException as e:
        logger.error("HTTPException: %s", e.detail)
        raise  # Re-raise to maintain behavior for FastAPI error handling
    except Exception as e:
        logger.exception("An unexpected error occurred while uploading PDF: %s", e)
        raise HTTPException(status_code=500, detail="An internal error occurred. Please try again later.")
