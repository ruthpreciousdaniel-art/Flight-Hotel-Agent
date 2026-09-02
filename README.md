# Flight & Stay Agent

## Local setup
1. `pip install -r requirements.txt`
2. Place `client_secret.json` (from Google Cloud Console) in the project root.
3. `python scripts/generate_token.py` → generates `token.json` (does a one-time browser login).
4. Copy `.env.example` to `.env` and fill in:
   - GROQ_API_KEY
   - DUFFEL_API_KEY
   - GOOGLE_CREDENTIALS_JSON (paste raw contents of client_secret.json)
   - GOOGLE_TOKEN_JSON (paste raw contents of token.json)
5. Run: `uvicorn app.main:app --reload`
6. Open http://localhost:8000

## Deploy to Railway
1. Push this repo to GitHub.
2. In Railway: New Project → Deploy from GitHub repo.
3. Railway auto-detects the Dockerfile.
4. In Railway → Variables, add all vars from `.env.example` (as raw JSON strings for the Google ones).
5. Railway sets `PORT` automatically — the Dockerfile already reads it.
