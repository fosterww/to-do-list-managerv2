from pydantic import BaseModel, field_validator
from pydantic.types import StringConstraints
from datetime import datetime
from enum import Enum
from typing import Optional, Annotated

class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    

class TaskCreate(BaseModel):
    title: Annotated[str, StringConstraints(min_length=1, max_length=255)]
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO
    
    @field_validator('title')
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Title cannot be empty or whitespace")
        return v
    
class TaskUpdate(BaseModel):
    title: Optional[Annotated[str, StringConstraints(min_length=1, max_length=255)]] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    
    @field_validator('title')
    def title_not_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Title cannot be empty or whitespace")
        return v
    
class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True