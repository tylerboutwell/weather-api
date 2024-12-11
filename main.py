from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List
from uuid import uuid4, UUID

api_key = "YOUR_API_KEY"
app = FastAPI()

class Task(BaseModel):
    id: Optional[UUID] = None
    title: str
    description: Optional[str] = None
    completed: bool = False

tasks = []

@app.post("/tasks/", response_model=Task)
def create_task(task: Task):
    task.id = uuid4()
    tasks.append(task)
    return task

@app.get("/tasks/", response_model = List[Task])
def get_tasks():
    return tasks

if __name__ == "__main__":
    import  uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

