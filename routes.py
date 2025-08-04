from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from typing import List
from schemas import TaskCreate, TaskUpdate, TaskResponse
from database import get_db
from sqlalchemy import select
from models import Task
from config import settings
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

api_key_header = APIKeyHeader(name="X-API-Key")

async def get_api_key(api_key: str = Security(api_key_header)):
    logger.debug(f"Received API key: {api_key[:4]}...")  # Log partial key for security
    if api_key != settings.api_key:
        logger.warning("Invalid API key received")
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return api_key

@router.post("/", response_model=TaskResponse, status_code=201, dependencies=[Depends(get_api_key)])
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating task with title: {task.title}")
    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/", response_model=List[TaskResponse], dependencies=[Depends(get_api_key)])
def get_tasks(status: str | None = None, db: Session = Depends(get_db)):
    logger.info(f"Fetching tasks with status filter: {status}")
    query = select(Task)
    if status:
        query = query.where(Task.status == status)
    tasks = db.execute(query).scalars().all()
    return tasks

@router.get("/{task_id}", response_model=TaskResponse, dependencies=[Depends(get_api_key)])
def get_task(task_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching task with ID: {task_id}")
    task = db.get(Task, task_id)
    if not task:
        logger.warning(f"Task not found: {task_id}")
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskResponse, dependencies=[Depends(get_api_key)])
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    logger.info(f"Updating task with ID: {task_id}")
    task = db.get(Task, task_id)
    if not task:
        logger.warning(f"Task not found: {task_id}")
        raise HTTPException(status_code=404, detail="Task not found")
    update_data = task_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}", status_code=204, dependencies=[Depends(get_api_key)])
def delete_task(task_id: int, db: Session = Depends(get_db)):
    logger.info(f"Deleting task with ID: {task_id}")
    task = db.get(Task, task_id)
    if not task:
        logger.warning(f"Task not found: {task_id}")
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return None