from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Manages application settings and environment variables.
    """
    HF_API_TOKEN: str = ""
    HF_API_URL: str = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"

settings = Settings()