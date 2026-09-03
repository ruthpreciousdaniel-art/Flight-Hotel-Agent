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
        print(f"DEBUG: {var_name} is EMPTY", flush=True)
        return {}

    print(f"DEBUG: {var_name} raw length = {len(raw)}", flush=True)

    try:
        data = json.loads(raw)
        print(f"DEBUG: {var_name} parsed successfully, keys = {list(data.keys())}", flush=True)
        return data

    except json.JSONDecodeError as e:
        print(f"ERROR: {var_name} JSON parsing failed: {e}", flush=True)

        if os.path.exists(raw):
            with open(raw, "r") as f:
                return json.load(f)

        return {}


GOOGLE_CREDENTIALS_JSON = _load_json_env("GOOGLE_CREDENTIALS_JSON")
GOOGLE_TOKEN_JSON = _load_json_env("GOOGLE_TOKEN_JSON")
