from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    HF_API_TOKEN: str = ""
    HF_API_URL: str = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"

settings = Settings()