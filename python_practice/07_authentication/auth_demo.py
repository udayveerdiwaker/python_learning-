# ==============================================================================
# auth_demo.py - FastAPI JWT Authentication and Password Hashing
# ==============================================================================
# Run this server using command: uvicorn auth_demo:app --reload
# View interactive documentation and test register/login at: http://127.0.0.1:8000/docs

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import jwt
from typing import Dict

# ------------------------------------------------------------------------------
# 1. Configuration & Security Settings
# ------------------------------------------------------------------------------

# WARNING: In production systems, NEVER hardcode secret keys. Use environment variables.
SECRET_KEY = "my_learning_super_secret_key_which_is_very_long"
ALGORITHM = "HS256"  # HMAC with SHA-256 signature algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Tokens will expire in 30 minutes for security

# Passlib CryptContext manages password hashing using the bcrypt algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2PasswordBearer extracts the token from the "Authorization: Bearer <token>" header.
# tokenUrl defines the endpoint that the documentation uses to request the token (login).
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI(
    title="JWT Auth Learning Server",
    description="A complete guide to password hashing, JWT generation, and endpoint protection.",
    version="1.0.0"
)


# ------------------------------------------------------------------------------
# 2. Database Models and In-Memory Data Store
# ------------------------------------------------------------------------------

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    username: str
    email: EmailStr

# In-memory user database storing user dictionaries (passwords are hashed!)
users_db: Dict[str, dict] = {}


# ------------------------------------------------------------------------------
# 3. Cryptographic & JWT Helper Functions
# ------------------------------------------------------------------------------

def get_password_hash(password: str) -> str:
    """
    Hashes a plain-text password using the bcrypt hashing algorithm.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain-text password against a stored hash.
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Generates a signed JSON Web Token (JWT).
    Adds expiration claim (exp) to the token payload.
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        
    # 'exp' is a standard JWT claim representing the expiration timestamp
    to_encode.update({"exp": int(expire.timestamp())})
    
    # Encode and sign the JWT payload using the Secret Key and Algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    FastAPI Dependency: Extracts and decodes the JWT token from the Authorization header.
    Validates token expiration and returns the active user record.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the token using our secret key and algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")  # 'sub' (subject) represents the user identifier
        
        if username is None:
            raise credentials_exception
            
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise credentials_exception
        
    # Retrieve user from the database
    user = users_db.get(username)
    if user is None:
        raise credentials_exception
        
    return user


# ------------------------------------------------------------------------------
# 4. Authentication Endpoints
# ------------------------------------------------------------------------------

# Route: Register a new user
@app.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["Auth"])
def register(user: UserRegister):
    """
    Registers a new user, hashes their password, and saves them to database.
    """
    if user.username in users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
        
    # Store hashed password, not the plain text!
    hashed_password = get_password_hash(user.password)
    
    users_db[user.username] = {
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed_password
    }
    
    return users_db[user.username]


# Route: Login (OAuth2 Password Request Flow)
# OAuth2PasswordRequestForm expects form-data: 'username' and 'password'
@app.post("/login", tags=["Auth"])
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticates username & password. Returns a JWT Bearer access token on success.
    """
    user = users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # Create the access token payload, setting 'sub' to username
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=access_token_expires
    )
    
    # Return the token in standard OAuth2 format
    return {"access_token": access_token, "token_type": "bearer"}


# Protected Route: Get User Profile details
# By depending on 'get_current_user', this endpoint will reject any requests
# that do not have a valid, unexpired Bearer token in their headers.
@app.get("/users/me", response_model=UserResponse, tags=["Users"])
def read_users_me(current_user: dict = Depends(get_current_user)):
    """
    A protected route returning the authenticated user's profile details.
    Requires a valid JWT Bearer Token.
    """
    return current_user
