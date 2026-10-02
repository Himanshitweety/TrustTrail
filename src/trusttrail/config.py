import os
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env")


def _get_list(name: str, default: str = "") -> list[str]:

    raw = os.getenv(name, default)
    return [item.strip().lower() for item in raw.split(",") if item.strip()]


def require(name: str) -> str:
    
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required setting: {name}. Add it to your .env file.")
    return value


LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")



# 

DATA_DIR = ROOT_DIR / os.getenv("DATA_DIR", "data")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "800"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "100"))
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "20"))
ALLOWED_EXTENSIONS = _get_list("ALLOWED_EXTENSIONS", ".pdf,.docx,.txt")
