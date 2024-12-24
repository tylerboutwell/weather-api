import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4, UUID
import requests
from dotenv import load_dotenv
import redis
import json
from contextlib import asynccontextmanager

load_dotenv()
api_key = os.getenv("api_key")
rd = redis.Redis(host='localhost', port=6379, db=0)
app = FastAPI()

@app.get("/current/")
def get_current_weather(city: str):
    if not api_key:
        raise HTTPException(status_code=404, detail=f"No API key provided. Showing {api_key}")
    cache = rd.get(city)
    if cache:
        print("Cache hit")
        print(rd.ttl(city))
        return json.loads(cache)
    else:
        print("Cache miss")
        curr = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}")
        if curr.status_code != 200:
            raise HTTPException(status_code=curr.status_code, detail=f"Forecast not found, api = {api_key}")
        rd.set(city, curr.text)
        rd.expire(city, 3600)
        return curr.json()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

