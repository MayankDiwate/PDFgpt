# app/schemas/document.py
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class DocumentCreate(BaseModel):
    name: str
    content: str

class DocumentResponse(BaseModel):
    id: UUID
    name: str
    uploaded_at: datetime
