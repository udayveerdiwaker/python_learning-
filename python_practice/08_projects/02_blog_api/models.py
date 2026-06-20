# models.py
import sys
from pathlib import Path

# Add parent directory for imports
sys.path.append(str(Path(__file__).resolve().parent.parent))

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from db_helper import Base

class DBCategory(Base):
    """
    SQLAlchemy Model mapping to the 'proj_categories' MySQL table.
    """
    __tablename__ = "proj_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    
    # Establish a relationship link: one category can have many blog posts
    blogs = relationship("DBBlog", back_populates="category")

class DBBlog(Base):
    """
    SQLAlchemy Model mapping to the 'proj_blogs' MySQL table.
    """
    __tablename__ = "proj_blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    category_id = Column(Integer, ForeignKey("proj_categories.id", ondelete="SET NULL"), nullable=True)
    author_id = Column(Integer, nullable=False)  # User ID of the blog author
    created_at = Column(DateTime, server_default=func.now())

    # Establish relationship to category model
    category = relationship("DBCategory", back_populates="blogs")
