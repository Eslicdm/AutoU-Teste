# AutoU - Teste - Analisador de Emails com IA

Este projeto é uma solução para o case prático da AutoU. Trata-se de uma aplicação web que utiliza Inteligência Artificial para classificar emails como "Produtivo" ou "Improdutivo" e sugerir uma resposta automática com base na classificação.

**Link da Aplicação na Nuvem: https://autou-teste.onrender.com

## Tecnologias Utilizadas

- **Backend:** Python com [FastAPI](https://fastapi.tiangolo.com/) para uma API de alta performance.
- **Frontend:** HTML, CSS, e JavaScript modular, com [Bootstrap](https://getbootstrap.com/) para um design responsivo.
- **Inteligência Artificial:** API de Inferência da [Hugging Face](https://huggingface.co/inference-api) com o modelo `facebook/bart-large-mnli` para classificação Zero-Shot.
- **Processamento de PDF:** Biblioteca pypdf.
- **Gerenciamento de Configuração:** Pydantic Settings com arquivos `.env` para carregar segredos de forma segura.

## Arquitetura

O projeto segue uma arquitetura em camadas para garantir um código limpo, organizado e escalável:

- `app/api/`: Contém os endpoints da API, separando a lógica de roteamento.
- `app/services/`: Isola a lógica de negócio, como a comunicação com a API de IA e a extração de texto de arquivos.
- `app/core/`: Gerencia as configurações da aplicação.
- `frontend/`: Contém todos os arquivos da interface do usuário (HTML, CSS, JS), com o JavaScript organizado em módulos.

## Funcionalidades

- Classificação de emails em **Produtivo** ou **Improdutivo**.
- Geração de uma **resposta automática** sugerida com base na classificação.
- Exibição da **justificativa da IA** para a classificação, aumentando a transparência.
- Interface web para inserir texto diretamente ou fazer **upload de arquivos `.txt` e `.pdf`**.
- Validação para impedir o envio de texto e arquivo simultaneamente.
- Botão para limpar os campos e reiniciar a interface.

---

## Como Executar Localmente

Siga os passos abaixo para rodar a aplicação na sua máquina.

### Pré-requisitos

- Python 3.9+
- Git

### 1. Clone o Repositório
```bash
git clone https://github.com/Eslicdm/AutoU-Teste.git
cd AutoU-Teste
```

### 2. Crie e Ative um Ambiente Virtual
```bash
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Instale as Dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as Variáveis de Ambiente
Crie um arquivo chamado `.env` na raiz do projeto e adicione seu token da Hugging Face:
```
HF_API_TOKEN="hf_SEU_TOKEN_AQUI"
```

### 5. Inicie a Aplicação
```bash
uvicorn app.main:app --reload
```

Acesse a aplicação em `http://127.0.0.1:8000` no seu navegador.