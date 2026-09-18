import os
from dotenv import load_dotenv

load_dotenv()


class Settings():
    DATABASE_URL = os.getenv("DATABASE_URL")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-5")
    MCP_TRANSPORT = os.getenv("MCP_TRANSPORT", "stdio")
    MCP_HOST = os.getenv("MCP_HOST", "0.0.0.0")
    MCP_PORT = int(os.getenv("MCP_PORT", "8000"))
    SERPAPI_KEY = os.getenv("SERPAPI_KEY")


settings = Settings()

