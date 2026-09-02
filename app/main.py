from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from app.models import PlanRequest, PlanResponse
from app.calendar_service import get_free_days
from app.duffel_service import search_flights, search_hotels
from app.agent import recommend

app = FastAPI(title="Flight & Stay Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return FileResponse("static/index.html")

@app.post("/api/plan", response_model=PlanResponse)
def plan_trip(req: PlanRequest):
    free_days = get_free_days(req.earliest_date, req.latest_date)

    flight_options = []
    for day in free_days:
        flight_options.extend(search_flights(req.origin, req.destination, day, req.travelers))

    hotel_options = []
    if free_days:
        check_in = free_days[0]
        check_out_dt = free_days[0]
        hotel_options = search_hotels(req.destination, check_in, check_out_dt, req.travelers)

    if not flight_options and not free_days:
        recommendation = "No free days found in your calendar for this date range."
    else:
        recommendation = recommend(free_days, flight_options, hotel_options, req.preferences)

    return PlanResponse(
        free_days=free_days,
        flight_options=flight_options,
        hotel_options=hotel_options,
        recommendation=recommendation,
    )
