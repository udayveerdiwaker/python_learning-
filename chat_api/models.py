import datetime
# pyrefly: ignore [missing-import]
from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String, nullable=False)
    message = Column(String, nullable=False)
    room = Column(String, default="general", index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
