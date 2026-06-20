# models.py
import sys
from pathlib import Path

# Add parent directory for imports
sys.path.append(str(Path(__file__).resolve().parent.parent))

from sqlalchemy import Column, Integer, String, Text, Boolean, Date, DateTime, func
from db_helper import Base

class DBTask(Base):
    """
    SQLAlchemy Model mapping to the 'proj_tasks' MySQL table.
    """
    __tablename__ = "proj_tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(String(20), default="Medium")  # Low, Medium, High
    due_date = Column(Date, nullable=True)
    completed = Column(Boolean, default=False)
    assignee_id = Column(Integer, nullable=True)  # Links to User ID
    created_at = Column(DateTime, server_default=func.now())
