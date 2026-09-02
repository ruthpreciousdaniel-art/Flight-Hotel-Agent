import requests
from app.config import DUFFEL_API_KEY, DUFFEL_API_URL

HEADERS = {
    "Authorization": f"Bearer {DUFFEL_API_KEY}",
    "Duffel-Version": "v2",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

def search_flights(origin: str, destination: str, date: str, travelers: int = 1) -> list:
    """
    Creates an offer request for a one-way slice on a given date and returns
    the top offers sorted by price.
    """
    payload = {
        "data": {
            "slices": [
                {"origin": origin, "destination": destination, "departure_date": date}
            ],
            "passengers": [{"type": "adult"} for _ in range(travelers)],
            "cabin_class": "economy",
        }
    }

    resp = requests.post(
        f"{DUFFEL_API_URL}/air/offer_requests",
        headers=HEADERS,
        json=payload,
        params={"return_offers": "true"},
    )
    resp.raise_for_status()
    data = resp.json()["data"]
    offers = data.get("offers", [])

    simplified = []
    for offer in offers[:10]:
        simplified.append({
            "id": offer["id"],
            "total_amount": offer["total_amount"],
            "total_currency": offer["total_currency"],
            "airline": offer["owner"]["name"],
            "departure": offer["slices"][0]["segments"][0]["departing_at"],
            "arrival": offer["slices"][0]["segments"][-1]["arriving_at"],
        })

    simplified.sort(key=lambda x: float(x["total_amount"]))
    return simplified


def search_hotels(location: str, check_in: str, check_out: str, guests: int = 1) -> list:
    """
    Searches Duffel Stays for accommodation near a location.
    'location' should be a city name or IATA code Duffel Stays accepts.
    """
    payload = {
        "data": {
            "check_in_date": check_in,
            "check_out_date": check_out,
            "guests": [{"type": "adult"} for _ in range(guests)],
            "location": {"radius": 15, "geographic_coordinates": None, "search_term": location},
        }
    }

    resp = requests.post(
        f"{DUFFEL_API_URL}/stays/search",
        headers=HEADERS,
        json=payload,
    )
    resp.raise_for_status()
    data = resp.json()["data"]
    results = data.get("results", [])

    simplified = []
    for hotel in results[:10]:
        simplified.append({
            "id": hotel.get("id"),
            "name": hotel.get("accommodation", {}).get("name"),
            "rating": hotel.get("accommodation", {}).get("rating"),
            "cheapest_rate": hotel.get("cheapest_rate_total_amount"),
            "currency": hotel.get("cheapest_rate_currency"),
        })

    return simplified
