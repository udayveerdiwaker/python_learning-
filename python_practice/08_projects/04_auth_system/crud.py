# crud.py
from sqlalchemy.orm import Session
from models import DBUser

def get_user_by_username(db: Session, username: str):
    return db.query(DBUser).filter(DBUser.username == username).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(DBUser).filter(DBUser.id == user_id).first()

def update_user_refresh_token(db: Session, user_id: int, refresh_token: str):
    """
    Saves a new active refresh token on the user's record.
    """
    db_user = get_user_by_id(db, user_id)
    if db_user:
        db_user.refresh_token = refresh_token
        db.commit()
        return True
    return False

def get_user_by_refresh_token(db: Session, refresh_token: str):
    """
    Fetches the user owning the specific active refresh token.
    """
    return db.query(DBUser).filter(DBUser.refresh_token == refresh_token).first()

def clear_user_refresh_token(db: Session, user_id: int):
    """
    Clears the refresh token from the database, effectively logging the user out.
    """
    db_user = get_user_by_id(db, user_id)
    if db_user:
        db_user.refresh_token = None
        db.commit()
        return True
    return False
