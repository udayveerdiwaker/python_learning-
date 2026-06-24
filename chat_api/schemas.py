from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class MessageCreate(BaseModel):
    sender: str
    message: str
    room: Optional[str] = "general"

class MessageResponse(BaseModel):
    id: int
    sender: str
    message: str
    room: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
