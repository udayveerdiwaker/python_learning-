# ==============================================================================
# db_helper.py - Shared SQLAlchemy Configuration for Projects
# ==============================================================================
# This helper initializes the database engine and provides a session generator dependency.

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL for local MySQL instance
# Format: mysql+mysqlconnector://<username>:<password>@<host>/<database_name>
DATABASE_URL = "mysql+mysqlconnector://root:@127.0.0.1:3306/python_practice_db"

# Create the SQLAlchemy Engine
# pool_recycle reconnects inactive connections automatically to prevent timeout errors
engine = create_engine(
    DATABASE_URL,
    pool_recycle=3600,
    pool_pre_ping=True
)

# SessionLocal class is the factory that makes new database session objects
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class: all ORM model classes will inherit from this
Base = declarative_base()

def get_db():
    """
    FastAPI Dependency: Opens a database session for a request and closes it
    automatically after the response is completed.
    
    Usage: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
