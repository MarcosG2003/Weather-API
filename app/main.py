import os
import json
from fastapi import FastAPI, HTTPException
import requests
from typing import cast
from dotenv import load_dotenv
import redis


load_dotenv()

API_KEY = os.getenv("VISUAL_CROSSING_API_KEY")
BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
REDIS_URL = os.getenv("REDIS_URL")
if REDIS_URL is None:
    raise RuntimeError("REDIS_URL is not set")
r = redis.Redis.from_url(REDIS_URL, decode_responses=True)

CACHE_SECONDS = os.getenv("CACHE_SECONDS", "3600")

CACHE_SECONDS_INT: int = int(CACHE_SECONDS)




app = FastAPI()





@app.get("/health")
def health():
    return {"status": "Good"}

@app.get("/weather/current")
def current_weather(city: str):
    city = city.strip()
    if not API_KEY:
        raise HTTPException(status_code=500, detail="Missing api key")
    
    url = f"{BASE_URL}/{city}"

    cache_key = f"weather:{city.lower()}"
    
    cached = r.get(cache_key)

    if cached is not None:
        return json.loads(cast(str, cached))

    params = {
        "key": API_KEY,
        "contentType": "json",
        "unitGroup": "us",
    }

    response = requests.get(url, params=params, timeout=30)

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Invalid city or upstream error")
    
    data = response.json()

    current = data.get("currentConditions")
    if not current:
        raise HTTPException(status_code=502, detail="Upstream response missing current conditions")
    

    result = {
        "city": city,
        "temperature": current.get("temp"),
        "conditions": current.get("conditions")
    }

    r.set(
        cache_key,
        json.dumps(result),
        ex=CACHE_SECONDS_INT
    )

    return result


