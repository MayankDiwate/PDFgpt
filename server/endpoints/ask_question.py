# server/api/endpoints/ask_question.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.question import QuestionRequest, AnswerResponse
from db.crud import get_document_by_id
from services.question_answering import generate_answer
from db.base import get_db

router = APIRouter()

@router.post("/ask-question", response_model=AnswerResponse)
async def ask_question(question_request: QuestionRequest, db: Session = Depends(get_db)):
    # Fetch the document by ID
    document = get_document_by_id(db, question_request.document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Generate an answer based on the document content and question
    answer = generate_answer(question_request.question, document.content)

    return AnswerResponse(
        content=answer
        # document_id=question_request.document_id,
        # question=question_request.question,
    )
