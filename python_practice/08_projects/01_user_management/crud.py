# crud.py
import sys
from pathlib import Path

# Add parent directory for imports
sys.path.append(str(Path(__file__).resolve().parent.parent))

from sqlalchemy.orm import Session
from models import DBUser
from schemas import UserCreate, UserUpdate
from security_helper import hash_password

def get_user_by_id(db: Session, user_id: int):
    """
    Fetches a user record by ID.
    """
    return db.query(DBUser).filter(DBUser.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    """
    Fetches a user record by their username.
    """
    return db.query(DBUser).filter(DBUser.username == username).first()

def get_user_by_email(db: Session, email: str):
    """
    Fetches a user record by their email address.
    """
    return db.query(DBUser).filter(DBUser.email == email).first()

def create_user(db: Session, user: UserCreate):
    """
    Hashes password and saves a new user record.
    """
    hashed_pwd = hash_password(user.password)
    db_user = DBUser(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pwd,
        role="User"  # Standard default role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_details(db: Session, user_id: int, user_update: UserUpdate):
    """
    Updates the email and/or password of a user.
    """
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
        
    # Update fields only if they are supplied in the request body
    if user_update.email:
        db_user.email = user_update.email
    if user_update.password:
        db_user.hashed_password = hash_password(user_update.password)
        
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user_record(db: Session, user_id: int):
    """
    Deletes the user record from the database.
    """
    db_user = get_db_user = get_user_by_id(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False
