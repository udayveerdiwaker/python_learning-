# schemas.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)

class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class BlogCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=150)
    content: str = Field(..., min_length=10)
    category_id: Optional[int] = None

class BlogUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=150)
    content: Optional[str] = Field(None, min_length=10)
    category_id: Optional[int] = None

class BlogResponse(BaseModel):
    id: int
    title: str
    content: str
    category_id: Optional[int]
    author_id: int
    created_at: datetime
    category: Optional[CategoryResponse] = None

    class Config:
        from_attributes = True
