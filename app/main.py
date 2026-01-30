import os
from fastapi import FastAPI, HTTPException
import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("VISUAL_CROSSING_API_KEY")
BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

app = FastAPI()





@app.get("/health")
def health():
    return {"status": "Good"}

@app.get("/weather/current")
def current_weather(city: str):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="Missing api key")
    
    url = f"{BASE_URL}/{city}"

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
    

    return {
        "city": city,
        "temperature": current.get("temp"),
        "conditions": current.get("conditions")
    }

