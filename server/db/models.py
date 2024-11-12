from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone
import uuid

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    name = Column(String, index=True)
    content = Column(String)  # Storing extracted text from the PDF
    uploaded_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))  # Corrected for timezone awareness
