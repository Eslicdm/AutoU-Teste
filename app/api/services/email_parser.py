import io
from typing import Optional

from fastapi import UploadFile, HTTPException
from pydantic import BaseModel
from pypdf import PdfReader

async def extract_text_from_source(
    email_text: Optional[str],
    email_file: Optional[UploadFile]
) -> str:
    content = ""
    if email_text:
        content = email_text
    elif email_file:
        if email_file.content_type == 'text/plain':
            content_bytes = await email_file.read()
            content = content_bytes.decode('utf-8')
        elif email_file.content_type == 'application/pdf':
            try:
                pdf_bytes = await email_file.read()
                pdf_stream = io.BytesIO(pdf_bytes)
                reader = PdfReader(pdf_stream)
                content = "".join(page.extract_text() or "" for page in reader.pages)
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Erro ao processar o arquivo PDF: {e}")
        else:
            raise HTTPException(status_code=400, detail="Tipo de arquivo não suportado. Por favor, envie um arquivo .txt ou .pdf.")
    else:
        raise HTTPException(status_code=400, detail="Nenhum texto de e-mail ou arquivo fornecido.")

    if not content.strip():
        raise HTTPException(status_code=400, detail="O conteúdo do email está vazio.")
        
    return content