import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
    INDEX_NAME = os.getenv("INDEX_NAME", "hdhdhdhd")
    ENABLE_LOGGING = os.getenv("ENABLE_LOGGING", "false").lower() == "true"
    
