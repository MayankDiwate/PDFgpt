# app/services/pdf_processing.py
from fastapi import UploadFile
import fitz  # PyMuPDF

async def extract_text_from_pdf(file: UploadFile) -> str:
    content = await file.read()  # Read file content
    pdf_text = ""

    # Open PDF with PyMuPDF
    with fitz.open("pdf", content) as pdf:
        for page in pdf:
            pdf_text += page.get_text()

    return pdf_text
