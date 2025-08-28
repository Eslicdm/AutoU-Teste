import httpx
from fastapi import HTTPException

from app.core.config import settings

class AIClassifierService:
    LABEL_MAP = {
        "Email de trabalho que exige uma ação ou resposta específica.": "Produtivo",
        "Email puramente informativo, como um anúncio ou newsletter.": "Improdutivo",
        "Email social ou de cortesia, como um agradecimento ou felicitação.": "Improdutivo"
    }

    async def _query_hf_model(self, payload: dict) -> dict:
        if not settings.HF_API_TOKEN:
            raise HTTPException(
                status_code=503,
                detail="Serviço de IA indisponível (API token não configurado no ambiente)."
            )

        headers = {"Authorization": f"Bearer {settings.HF_API_TOKEN}"}
        async with httpx.AsyncClient() as client:
            response = await client.post(settings.HF_API_URL, headers=headers, json=payload)
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Erro na API da Hugging Face: {response.text}"
                )
            return response.json()

    async def classify_and_respond(self, content: str) -> dict:
        min_words = 3
        if len(content.strip().split()) < min_words:
            return {
                "classification": "Improdutivo",
                "response": self._generate_response("Improdutivo")
            }

        truncated_content = content[:512]
        candidate_labels = list(self.LABEL_MAP.keys())

        payload = {
            "inputs": truncated_content,
            "parameters": {"candidate_labels": candidate_labels}
        }
        result = await self._query_hf_model(payload)

        if isinstance(result, dict) and result.get('error'):
            error_message = result.get('error')
            if 'is currently loading' in error_message:
                raise HTTPException(
                    status_code=503,
                    detail=f"Serviço de IA indisponível no momento. (Erro: {error_message})"
                )
            raise HTTPException(
                status_code=500,
                detail=f"A API da Hugging Face retornou um erro: {error_message}"
            )

        if not isinstance(result, dict) or 'labels' not in result or not result.get('labels'):
            raise HTTPException(
                status_code=500,
                detail=f"Resposta inesperada da API de IA. Resposta recebida: {str(result)[:200]}"
            )

        best_email_description = result['labels'][0]
        classification = self.LABEL_MAP.get(best_email_description, "Improdutivo")
        response_text = self._generate_response(classification)

        return {"classification": classification, "response": response_text}

    def _generate_response(self, classification: str) -> str:
        if classification == "Produtivo":
            return ("Olá!\n\nObrigado pelo seu email."
                    " Recebemos sua solicitação e nossa equipe já está analisando."
                    " Retornaremos em breve com uma atualização."
                    "\n\nAtenciosamente,\nEquipe de Suporte")
        else:
            return ("Olá!\n\nObrigado pela sua mensagem."
                    " Agradecemos o contato."
                    "\n\nAtenciosamente,\nEquipe AutoU")