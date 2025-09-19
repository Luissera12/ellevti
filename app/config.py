import os

class Config:
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    TESTING = False
    PORT = int(os.getenv("PORT", 5000))
    DATABASE = os.getenv("DATABASE", "tarefas.db")
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
