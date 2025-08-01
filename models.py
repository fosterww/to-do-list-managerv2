from sqlalchemy import Column, Integer, String, Enum, DateTime
from database import Base
from datetime import datetime
from schemas import TaskStatus


task_status_enum = Enum(
    TaskStatus,
    name="taskstatus",
    create_type=True,
    metadata=Base.metadata
)

class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(task_status_enum, default=TaskStatus.TODO, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    

    

    