from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "Good"}

@app.get("/weather/current")
def current_weather(city: str):
    return {
        "city": "chicago",
        "temperature": "32"
    }
