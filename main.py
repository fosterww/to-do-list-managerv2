from fastapi import FastAPI
from routes import router as task_router
from database import init_db
from models import Task

app = FastAPI(title="Task Manager API")

# Initialize database tables
init_db()

# Include task routes
app.include_router(task_router, prefix="/tasks", tags=["tasks"])

@app.get("/")
def read_root():
    return {"message": "Task Manager API"}

