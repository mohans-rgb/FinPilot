
from datetime import date, datetime, timedelta
import requests
from .settings import settings


API_URL = "https://serpapi.com/search.json"


CITY_TO_IATA = {
    "bhopal": "BHO", "mumbai": "BOM", "delhi": "DEL", "new delhi": "DEL",
    "bengaluru": "BLR", "bangalore": "BLR", "chennai": "MAA", "kolkata": "CCU",
    "hyderabad": "HYD", "pune": "PNQ", "goa": "GOI",
}
FLIGHTS_CURRENCY = "INR"
FLIGHTS_MAX_RESULTS = 10

def _fmt_duration(minutes:int) -> str:
    return f"{minutes//60}H {minutes%60}m"

def _fmt_option(opt: dict) -> str:
    legs = opt.get("flights", [])
    if not legs:
        return ""
    first, last = legs[0], legs[-1]
    airlines = sorted({leg.get("airline", "") for leg in legs})
    airline = airlines[0] if len(airlines) == 1 else "Multiple"
    stops = len(legs) - 1
    stops_txt = "non-stop" if stops == 0 else f"{stops} stop" + ("s" if stops > 1 else "")
    dep = first.get("departure_airport", {})
    arr = last.get("arrival_airport", {})
    price = opt.get("price")
    price_txt = f"{price} {FLIGHTS_CURRENCY}" if price is not None else "price N/A"
    numbers = ", ".join(leg.get("flight_number", "") for leg in legs)
    return (f"- {airline} | {price_txt} | {stops_txt} | {_fmt_duration(opt.get('total_duration', 0))}\n"
            f"    {dep.get('id','?')} {dep.get('time','')}  →  {arr.get('id','?')} {arr.get('time','')}  [{numbers}]")




def search_flights(from_city:str, to_city:str, travel_date:str = "") -> str:
    dep = CITY_TO_IATA.get(from_city.lower(), "")
    arr = CITY_TO_IATA.get(to_city.lower(), "")
    
    if not dep or not arr:
        return "Not Flight found b/w this route"
    
    
    when = travel_date.strip() or (date.today() + timedelta(days=7)).strftime("%Y-%m-%d")

    params = {
        "engine": "google_flights",
        "departure_id": dep,
        "arrival_id": arr,
        "currency": FLIGHTS_CURRENCY,
        "type": "2",
        "outbound_date": when,
        "api_key":settings.SERPAPI_KEY
        }
    
    
    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()
    except Exception as Exc:
        return f"Flight Search Failed {Exc}"
    

    if data.get("error"):
        return f"Flight search error: {data['error']}"

    options = (data.get("best_flights") or []) + (data.get("other_flights") or [])
    if not options:
        return f"No flights found from {dep} to {arr} on {when}."

    lines = [f"Flights {dep} → {arr} on {when} (one way):"]
    for opt in options[:FLIGHTS_MAX_RESULTS]:
        line = _fmt_option(opt)
        if line:
            lines.append(line)
            
    return "\n\n".join(lines)
    