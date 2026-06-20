# ==============================================================================
# challenge.py - Authentication Utility Functions Challenge
# ==============================================================================
# CHALLENGE: Implement the password hashing, verification, and JWT parsing functions.
# Run this script using `python challenge.py` to verify your code with assertions!

from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt

SECRET_KEY = "challenge_secret_key"
ALGORITHM = "HS256"

# CryptContext manager using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ------------------------------------------------------------------------------
# Task 1: Complete Password Utilities
# ------------------------------------------------------------------------------
def hash_user_password(password: str) -> str:
    """
    Hashes a password using the bcrypt algorithm.
    """
    # Write your code below this line
    return pwd_context.hash(password)
    # Write your code above this line

def verify_user_password(plain_password: str, hashed_password: str) -> bool:
    """
    Compares a plain password with a hashed password, returning True if matching.
    """
    # Write your code below this line
    return pwd_context.verify(plain_password, hashed_password)
    # Write your code above this line


# ------------------------------------------------------------------------------
# Task 2: Complete JWT Utilities
# ------------------------------------------------------------------------------
def generate_token(username: str, expires_minutes: int) -> str:
    """
    Generates a JWT token containing claim 'sub' set to username.
    Expiry claim 'exp' set to current UTC timestamp + expires_minutes.
    """
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    payload = {
        "sub": username,
        "exp": int(expire.timestamp())
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_and_verify_token(token: str) -> dict:
    """
    Decodes the JWT token.
    - If the token is valid, returns the decoded payload dictionary.
    - If the token has expired, raises a jwt.ExpiredSignatureError.
    - If the token is invalid, raises a jwt.InvalidTokenError.
    """
    # Write your code below this line
    # Hint: Use jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    # Write your code above this line


# ==============================================================================
# AUTOMATED TESTS (Do not modify!)
# ==============================================================================
if __name__ == "__main__":
    print("Running authentication utility tests...")
    
    # Test Password Hashing
    raw_pw = "SuperPassword123"
    hashed_pw = hash_user_password(raw_pw)
    assert raw_pw != hashed_pw, "Password should not be stored in plain text!"
    assert verify_user_password(raw_pw, hashed_pw) is True, "Password verification failed"
    assert verify_user_password("WrongPassword", hashed_pw) is False, "Should reject wrong passwords"
    print("Task 1 (Password Hashing) passed! ✅")
    
    # Test JWT Token Encoding/Decoding
    user = "alice_tester"
    token = generate_token(user, expires_minutes=5)
    
    # Verify parsing valid token
    try:
        payload = decode_and_verify_token(token)
        assert payload["sub"] == user, f"Expected subject '{user}', got '{payload.get('sub')}'"
        print("Task 2 (JWT Decoding) passed! ✅")
    except Exception as e:
        print(f"Failed decoding valid token: {e}")
        
    # Verify parsing expired token
    expired_token = generate_token(user, expires_minutes=-10)  # Created 10 minutes in past
    try:
        decode_and_verify_token(expired_token)
        print("❌ Test failed: Should raise ExpiredSignatureError for expired tokens")
    except jwt.ExpiredSignatureError:
        print("Task 2 (JWT Expiration Catching) passed! ✅")
    except Exception as e:
        print(f"❌ Test failed: Raised wrong exception for expired token: {type(e)}")
        
    # Verify parsing corrupt token
    corrupt_token = token + "corrupted_signature"
    try:
        decode_and_verify_token(corrupt_token)
        print("❌ Test failed: Should raise InvalidTokenError for corrupted tokens")
    except jwt.InvalidTokenError:
        print("Task 2 (JWT Tampering Verification) passed! ✅")
    except Exception as e:
        print(f"❌ Test failed: Raised wrong exception: {type(e)}")
        
    print("\nAll authentication challenge exercises passed! Security expert status achieved! 🛡️")
