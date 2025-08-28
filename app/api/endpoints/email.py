from typing import Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException

from app.services.ai_classifier import AIClassifierService
from app.services.email_parser import extract_text_from_source

router = APIRouter()

@router.post("/process-email/")
async def process_email(
    email_text: Optional[str] = Form(None),
    email_file: Optional[UploadFile] = File(None),
    ai_service: AIClassifierService = Depends(AIClassifierService)
):
    try:
        content = await extract_text_from_source(email_text, email_file)
        result = await ai_service.classify_and_respond(content)
        return result
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Erro inesperado no processamento do email: {str(e)}")