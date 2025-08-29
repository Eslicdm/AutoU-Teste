import io
from typing import Optional, Callable, Awaitable, Dict

from fastapi import UploadFile, HTTPException
from pypdf import PdfReader

AsyncFileParser = Callable[[UploadFile], Awaitable[str]]

async def _parse_txt(file: UploadFile) -> str:
    content_bytes = await file.read()
    return content_bytes.decode('utf-8')

async def _parse_pdf(file: UploadFile) -> str:
    try:
        pdf_bytes = await file.read()
        pdf_stream = io.BytesIO(pdf_bytes)
        reader = PdfReader(pdf_stream)
        return "".join(page.extract_text() or "" for page in reader.pages)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao processar o arquivo PDF: {e}")

FILE_PARSERS: Dict[str, AsyncFileParser] = {
    'text/plain': _parse_txt,
    'application/pdf': _parse_pdf,
}

async def extract_text_from_source(
    email_text: Optional[str],
    email_file: Optional[UploadFile]
) -> str:
    content = ""
    if email_text:
        content = email_text
    elif email_file:
        parser = FILE_PARSERS.get(email_file.content_type)
        if not parser:
            raise HTTPException(status_code=400, detail="Tipo de arquivo não suportado")
        
        content = await parser(email_file)
    else:
        raise HTTPException(status_code=400, detail="Nenhum texto de e-mail ou arquivo fornecido.")

    if not content.strip():
        raise HTTPException(status_code=400, detail="O conteúdo do email está vazio.")
        
    return content