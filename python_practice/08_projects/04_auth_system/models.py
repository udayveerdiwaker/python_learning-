# models.py
import sys
from pathlib import Path

# Add parent directory for imports
sys.path.append(str(Path(__file__).resolve().parent.parent))

from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from db_helper import Base

class DBUser(Base):
    """
    SQLAlchemy Model mapping to the 'proj_users' table.
    Contains support for role-based controls and token refresh cycles.
    """
    __tablename__ = "proj_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(150), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="User")  # 'User' or 'Admin'
    is_active = Column(Boolean, default=True)
    refresh_token = Column(String(255), nullable=True)  # Stores active refresh token hash/string
    created_at = Column(DateTime, server_default=func.now())
