from pydantic import BaseModel
from typing import Optional

class PlanRequest(BaseModel):
    origin: str                # IATA code, e.g. "ABV"
    destination: str           # IATA code, e.g. "LOS"
    earliest_date: str         # YYYY-MM-DD
    latest_date: str           # YYYY-MM-DD
    trip_length_days: int = 2
    travelers: int = 1
    preferences: str = ""      # free text prompt, e.g. "cheapest, morning flights, 4-star hotel"

class PlanResponse(BaseModel):
    free_days: list
    flight_options: list
    hotel_options: list
    recommendation: str
