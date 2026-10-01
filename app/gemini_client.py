import os
from dotenv import load_dotenv
from google import genai

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(ROOT_DIR, ".env"), override=True)

PRO_MODEL = os.getenv("PRO_MODEL", "gemini-3.8-flash")
FLASH_MODEL = os.getenv("FLASH_MODEL", "gemini-3.8-flash")

_client = None


def _get_client():
    global _client
    if _client is None:
        key = (os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or "").strip().strip('"').strip("'")
        if not key:
            raise RuntimeError("GEMINI_API_KEY .env file-la illa")
        _client = genai.Client(api_key=key)
    return _client


def ask_gemini(model: str, prompt: str) -> str:
    response = _get_client().models.generate_content(model=model, contents=prompt)
    return (response.text or "").strip()
