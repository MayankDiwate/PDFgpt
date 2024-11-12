# app/db/crud.py
from sqlalchemy.orm import Session
from schemas.document import DocumentCreate
from db.models import Document

def create_document(db: Session, document: DocumentCreate) -> Document:
    db_document = Document(
        name=document.name,
        content=document.content,
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

def get_document_by_id(db: Session, document_id: int) -> Document:
    return db.query(Document).filter(Document.id == document_id).first()
