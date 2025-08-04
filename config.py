from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    test_database_url: str
    api_key: str  

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
