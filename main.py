from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4, UUID

api_key = "YOUR_API_KEY"
app = FastAPI()

class Forecast(BaseModel):
    id: UUID | None = None
    title: str
    description: str | None = None
    completed: bool = False

forecasts = []

@app.post("/forecasts/", response_model=Forecast)
def create_task(forecast: Forecast):
    forecast.id = uuid4()
    forecasts.append(forecast)
    return forecasts

@app.get("/forecasts/", response_model = list[Forecast])
def get_tasks():
    return forecasts

@app.get("/forecasts/{task_id}", response_model=Forecast)
def get_task(forecast_id: UUID):
    for forecast in forecasts:
        if forecast.id == forecast_id:
            return forecast
    raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{task_id}", response_model=Forecast)
def update_task(task_id: UUID, forecast_update: Forecast):
    for ind, item in enumerate(forecasts):
        if item.id == task_id:
            forecasts[ind] = item.copy(update=forecast_update.model_dump(exclude_unset=True))
            return forecasts[ind]
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}", response_model=Forecast)
def delete_task(task_id: UUID):
    for ind, task in enumerate(forecasts):
        if task.id == task_id:
            return forecasts.pop(ind)
    raise HTTPException(status_code=404, detail="Task not found")

if __name__ == "__main__":
    import  uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

