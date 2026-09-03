import os
import datetime
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from app.config import GOOGLE_TOKEN_JSON, GOOGLE_CREDENTIALS_JSON, TIMEZONE

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def _get_credentials() -> Credentials:
    raw_len = len(os.getenv("GOOGLE_TOKEN_JSON", ""))
    print(f"DEBUG: GOOGLE_TOKEN_JSON raw length = {raw_len}", flush=True)
    print(
        f"DEBUG: parsed GOOGLE_TOKEN_JSON keys = {list(GOOGLE_TOKEN_JSON.keys())}",
        flush=True,
    )

    if not GOOGLE_TOKEN_JSON:
        raise RuntimeError(
            "GOOGLE_TOKEN_JSON is not set. Run scripts/generate_token.py first."
        )

    creds = Credentials(
        token=GOOGLE_TOKEN_JSON.get("token"),
        refresh_token=GOOGLE_TOKEN_JSON.get("refresh_token"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=GOOGLE_CREDENTIALS_JSON.get(
            "installed",
            GOOGLE_CREDENTIALS_JSON.get("web", {})
        ).get("client_id"),
        client_secret=GOOGLE_CREDENTIALS_JSON.get(
            "installed",
            GOOGLE_CREDENTIALS_JSON.get("web", {})
        ).get("client_secret"),
        scopes=SCOPES,
    )

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())

    return creds


def get_free_days(start_date: str, end_date: str) -> list:
    creds = _get_credentials()
    service = build("calendar", "v3", credentials=creds)

    start_dt = datetime.datetime.fromisoformat(start_date)
    end_dt = datetime.datetime.fromisoformat(end_date) + datetime.timedelta(days=1)

    body = {
        "timeMin": start_dt.isoformat() + "Z",
        "timeMax": end_dt.isoformat() + "Z",
        "timeZone": TIMEZONE,
        "items": [{"id": "primary"}],
    }

    result = service.freebusy().query(body=body).execute()
    busy_slots = result["calendars"]["primary"]["busy"]

    busy_days = set()

    for slot in busy_slots:
        day = slot["start"][:10]
        busy_days.add(day)

    free_days = []
    current = start_dt

    while current.date() <= (end_dt - datetime.timedelta(days=1)).date():
        day_str = current.strftime("%Y-%m-%d")

        if day_str not in busy_days:
            free_days.append(day_str)

        current += datetime.timedelta(days=1)

    return free_days
