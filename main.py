import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4, UUID
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("api_key")
app = FastAPI()
@app.get("/current/")
def get_current_weather(lat: int, lon: int):
    if not api_key:
        raise HTTPException(status_code=404, detail=f"No API key provided. Showing {api_key}")
    curr = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=imperial")
    if curr.status_code != 200:
        raise HTTPException(status_code=curr.status_code, detail=f"Forecast not found, api = {api_key}")
    return curr.json()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

