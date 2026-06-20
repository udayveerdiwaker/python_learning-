# models.py
import sys
from pathlib import Path

# Add parent directory to sys.path to enable importing db_helper
sys.path.append(str(Path(__file__).resolve().parent.parent))

from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from db_helper import Base

class DBUser(Base):
    """
    SQLAlchemy ORM Model mapping to the 'proj_users' MySQL table.
    """
    __tablename__ = "proj_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(150), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="User")
    is_active = Column(Boolean, default=True)
    refresh_token = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
