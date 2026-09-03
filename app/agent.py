import json
import httpx
from groq import Groq
from app.config import GROQ_API_KEY, GROQ_MODEL

client = Groq(
    api_key=GROQ_API_KEY,
    http_client=httpx.Client(),
)

SYSTEM_PROMPT = """You are a travel-planning reasoning agent.
You are given:
- The user's free calendar days
- A list of flight options (with price, airline, departure/arrival times)
- A list of hotel options (with price, rating)
- The user's free-text preferences

Your job: pick the single best flight + hotel combination that fits the user's
free days and preferences, and explain your reasoning briefly (3-5 sentences).
If nothing fits well, say so clearly and suggest the closest alternative.
Respond in plain, direct language. Do not invent data not given to you.
"""

def recommend(free_days: list, flight_options: list, hotel_options: list, preferences: str) -> str:
    user_content = f"""
Free calendar days: {json.dumps(free_days)}

Flight options: {json.dumps(flight_options, indent=2)}

Hotel options: {json.dumps(hotel_options, indent=2)}

User preferences: {preferences}

Recommend the best flight + hotel combo and explain why.
"""

    completion = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
        temperature=0.3,
        max_tokens=700,
    )

    return completion.choices[0].message.content
