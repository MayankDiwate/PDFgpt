# app/schemas/question.py
from pydantic import BaseModel

class QuestionRequest(BaseModel):
    document_id: str
    question: str

class AnswerResponse(BaseModel):
    # document_id: str
    # question: str
    content: str
