# main.py
import sys
from pathlib import Path
from datetime import timedelta

# Add parent directory for imports
sys.path.append(str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from db_helper import get_db
import crud
import schemas
from security_helper import (
    verify_password,
    create_access_token,
    get_current_user_from_token
)

app = FastAPI(
    title="Role-Based JWT Auth Service",
    description="Project 4: Access/Refresh tokens, Token Rotation, and role-based route access controls.",
    version="1.0.0"
)

# ------------------------------------------------------------------------------
# Role Authorization Dependencies
# ------------------------------------------------------------------------------
def require_admin(current_user: dict = Depends(get_current_user_from_token)):
    """
    Dependency: Restricts route access to Admins only.
    """
    if current_user["role"] != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: Admin privileges required."
        )
    return current_user


# ------------------------------------------------------------------------------
# Auth Endpoints
# ------------------------------------------------------------------------------

@app.post("/login", response_model=schemas.TokenResponse, tags=["Auth"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticates username/password and issues access & refresh tokens.
    Saves the refresh token to the database.
    """
    user = crud.get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
        
    # Generate short-lived access token (30 mins)
    access_token = create_access_token(data={
        "sub": user.username,
        "role": user.role,
        "user_id": user.id
    }, expires_delta=timedelta(minutes=30))
    
    # Generate long-lived refresh token (7 days)
    refresh_token = create_access_token(data={
        "sub": user.username,
        "user_id": user.id
    }, expires_delta=timedelta(days=7))
    
    # Save refresh token in database for verification later
    crud.update_user_refresh_token(db, user.id, refresh_token)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@app.post("/refresh", response_model=schemas.TokenResponse, tags=["Auth"])
def refresh_token(payload: schemas.RefreshRequest, db: Session = Depends(get_db)):
    """
    Validates a refresh token against the database and issues a new access/refresh pair.
    """
    # 1. Fetch user by active refresh token
    user = crud.get_user_by_refresh_token(db, payload.refresh_token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token."
        )
        
    # 2. Issue new token pair (Token Rotation)
    new_access = create_access_token(data={
        "sub": user.username,
        "role": user.role,
        "user_id": user.id
    }, expires_delta=timedelta(minutes=30))
    
    new_refresh = create_access_token(data={
        "sub": user.username,
        "user_id": user.id
    }, expires_delta=timedelta(days=7))
    
    # 3. Update active refresh token in database
    crud.update_user_refresh_token(db, user.id, new_refresh)
    
    return {
        "access_token": new_access,
        "refresh_token": new_refresh,
        "token_type": "bearer"
    }


@app.post("/logout", tags=["Auth"])
def logout(current_user: dict = Depends(get_current_user_from_token), db: Session = Depends(get_db)):
    """
    Invalidates the user's session by clearing the refresh token from the database.
    """
    crud.clear_user_refresh_token(db, current_user["id"])
    return {"message": "Logged out successfully. Session invalidated."}


# ------------------------------------------------------------------------------
# Protected Test Routes
# ------------------------------------------------------------------------------

@app.get("/profile", response_model=schemas.UserResponse, tags=["Protected"])
def read_profile(current_user: dict = Depends(get_current_user_from_token), db: Session = Depends(get_db)):
    """
    Access: Any authenticated user.
    """
    return crud.get_user_by_id(db, current_user["id"])


@app.get("/admin-only", tags=["Protected"])
def read_admin_secrets(admin_user: dict = Depends(require_admin)):
    """
    Access: Admins only. Throws 403 Forbidden for standard users.
    """
    return {"message": f"Hello Admin {admin_user['username']}! You have accessed the administrative portal."}
