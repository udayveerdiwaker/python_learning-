# schemas.py
from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=150)
    description: Optional[str] = None
    priority: str = Field(default="Medium", pattern="^(Low|Medium|High)$")
    due_date: Optional[date] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=2, max_length=150)
    description: Optional[str] = None
    priority: Optional[str] = Field(None, pattern="^(Low|Medium|High)$")
    due_date: Optional[date] = None
    completed: Optional[bool] = None
    assignee_id: Optional[int] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    priority: str
    due_date: Optional[date]
    completed: bool
    assignee_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True
