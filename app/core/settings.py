import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self):
        self.ENV = os.getenv("ENV", "development")

        self.DB_HOST = os.getenv("DB_HOST")
        self.DB_PORT = os.getenv("DB_PORT")
        self.DB_USER = os.getenv("DB_USER")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD")
        self.DB_NAME = os.getenv("DB_NAME")

        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    @property
    def database_url(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
settings = Settings()