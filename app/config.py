import os
import json
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

DUFFEL_API_KEY = os.getenv("DUFFEL_API_KEY", "")
DUFFEL_API_URL = os.getenv("DUFFEL_API_URL", "https://api.duffel.com")

TIMEZONE = os.getenv("TIMEZONE", "Africa/Lagos")

def _load_json_env(var_name: str) -> dict:
    raw = os.getenv(var_name, "")
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # allow path-to-file fallback for local dev
        if os.path.exists(raw):
            with open(raw, "r") as f:
                return json.load(f)
        return {}

GOOGLE_CREDENTIALS_JSON = _load_json_env("GOOGLE_CREDENTIALS_JSON")
GOOGLE_TOKEN_JSON = _load_json_env("GOOGLE_TOKEN_JSON")
