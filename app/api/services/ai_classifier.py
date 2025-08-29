import httpx
from fastapi import HTTPException

from app.core.config import settings


class AIClassifierService:
    LABEL_MAP = {
        "solicitação de suporte técnico": "Produtivo",
        "pedido de atualização ou status": "Produtivo",
        "dúvida sobre produto ou serviço": "Produtivo",
        "reclamação ou problema técnico": "Produtivo",
        "agradecimento pessoal": "Improdutivo",
        "conversa informal ou social": "Improdutivo",
        "felicitações ou cumprimentos": "Improdutivo",
        "spam ou mensagem irrelevante": "Improdutivo"
    }

    PRODUCTIVE_KEYWORDS = [
        'problema', 'erro', 'não funciona', 'ajuda', 'suporte', 'dúvida',
        'como fazer', 'não consigo', 'preciso', 'urgente', 'status',
        'atualização', 'prazo', 'quando', 'onde', 'por que não',
        'falha', 'bug', 'solicito', 'gostaria de', 'poderia',
        'informação', 'esclarecimento', 'orientação'
    ]

    UNPRODUCTIVE_KEYWORDS = [
        'obrigado', 'obrigada', 'valeu', 'muito obrigado', 'agradeço',
        'parabéns', 'feliz', 'felicidades', 'felicitações', 'aniversário',
        'natal', 'ano novo', 'feriado', 'oi', 'olá', 'tudo bem',
        'biscoito', 'bolo', 'comida', 'receita', 'pessoal',
        'abraço', 'beijo', 'tchau', 'até logo', 'bom dia',
        'boa tarde', 'boa noite', 'fim de semana'
    ]

    async def _query_hf_model(self, payload: dict) -> dict:
        if not settings.HF_API_TOKEN:
            raise HTTPException(
                status_code=503,
                detail="Serviço de IA indisponível (API token não configurado)."
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

    def _preprocess_and_classify_keywords(self, content: str) -> str:
        content_lower = content.lower()

        productive_score = sum(1 for keyword in self.PRODUCTIVE_KEYWORDS
                               if keyword in content_lower)
        unproductive_score = sum(1 for keyword in self.UNPRODUCTIVE_KEYWORDS
                                 if keyword in content_lower)

        if unproductive_score > productive_score and unproductive_score >= 1:
            return "Improdutivo"
        elif productive_score > unproductive_score and productive_score >= 2:
            return "Produtivo"

        if len(content.strip().split()) <= 5:
            simple_patterns = ['obrigado', 'valeu', 'oi', 'olá', 'tchau', 'biscoito', 'bolo']
            if any(pattern in content_lower for pattern in simple_patterns):
                return "Improdutivo"

        return None

    async def classify_and_respond(self, content: str) -> dict:
        if len(content.strip().split()) < 3:
            return {
                "classification": "Improdutivo",
                "response": self._generate_response("Improdutivo")
            }

        keyword_classification = self._preprocess_and_classify_keywords(content)
        if keyword_classification:
            return {
                "classification": keyword_classification,
                "response": self._generate_response(keyword_classification)
            }

        truncated_content = content[:512]
        candidate_labels = list(self.LABEL_MAP.keys())

        payload = {
            "inputs": truncated_content,
            "parameters": {"candidate_labels": candidate_labels}
        }

        try:
            result = await self._query_hf_model(payload)
        except Exception as e:
            if any(word in content.lower() for word in ['obrigado', 'biscoito', 'bolo', 'oi', 'olá']):
                return {
                    "classification": "Improdutivo",
                    "response": self._generate_response("Improdutivo")
                }
            raise e

        if isinstance(result, dict) and result.get('error'):
            error_message = result.get('error')
            if 'is currently loading' in error_message:
                raise HTTPException(
                    status_code=503,
                    detail="O modelo de IA está sendo preparado. Por favor, tente novamente em alguns segundos."
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

        if hasattr(result, 'scores') and len(result.get('scores', [])) > 0:
            confidence = result['scores'][0]
            if confidence < 0.7 and any(word in content.lower()
                                        for word in ['obrigado', 'biscoito', 'bolo', 'valeu']):
                classification = "Improdutivo"

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
