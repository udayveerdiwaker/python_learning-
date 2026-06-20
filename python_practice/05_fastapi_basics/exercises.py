# ==============================================================================
# exercises.py - Practice Exercises for FastAPI Basics
# ==============================================================================
# Complete the exercises below. Run this script using `python exercises.py`
# to run the local TestClient assertions to check if your endpoints are correct.

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

# Instantiate a learning FastAPI application for routing exercises
app = FastAPI()

# ------------------------------------------------------------------------------
# Exercise 1: Path Parameter Route
# ------------------------------------------------------------------------------
# Task: Create a GET endpoint at path "/greet/{name}".
# It should accept a string path parameter 'name' and return a dictionary:
# {"message": "Hello, <name>!"}

# Write your code below this line
@app.get("/greet/{name}")
def greet(name: str):
    return {"message": f"Hello, {name}!"}
# Write your code above this line


# ------------------------------------------------------------------------------
# Exercise 2: Query Parameters Route
# ------------------------------------------------------------------------------
# Task: Create a GET endpoint at path "/search".
# It should accept two query parameters:
# - 'q' (optional string, defaults to None)
# - 'limit' (integer, defaults to 10)
# Returns a dictionary: {"q": q, "limit": limit}

# Write your code below this line
@app.get("/search")
def search(q: Optional[str] = None, limit: int = 10):
    return {"q": q, "limit": limit}
# Write your code above this line


# ------------------------------------------------------------------------------
# Exercise 3: Pydantic Validation Schema
# ------------------------------------------------------------------------------
# Task: Complete the Pydantic schema model 'UserSignUp' to validate registration fields:
# - username: must be a string, minimum length of 3 characters, required.
# - email: must be a string (or EmailStr), required.
# - password: must be a string, minimum length of 6 characters, required.

class UserSignUp(BaseModel):
    # Write your code below this line
    username: str = Field(..., min_length=3)
    email: str
    password: str = Field(..., min_length=6)
    # Write your code above this line


# Endpoint to test the schema
@app.post("/register")
def register_user(user: UserSignUp):
    return {"status": "success", "user": user}


# ==============================================================================
# AUTOMATED TESTS (Do not modify!)
# ==============================================================================
if __name__ == "__main__":
    from fastapi.testclient import TestClient
    
    print("Initializing test client...")
    client = TestClient(app)
    
    print("Running exercises tests...")
    
    # Test Exercise 1
    resp1 = client.get("/greet/Alice")
    assert resp1.status_code == 200, f"Expected 200, got {resp1.status_code}"
    assert resp1.json() == {"message": "Hello, Alice!"}, f"Unexpected greeting: {resp1.json()}"
    print("Exercise 1 passed! ✅")

    # Test Exercise 2
    resp2 = client.get("/search?q=fastapi&limit=5")
    assert resp2.status_code == 200
    assert resp2.json() == {"q": "fastapi", "limit": 5}, f"Unexpected search return: {resp2.json()}"
    
    resp2_default = client.get("/search")
    assert resp2_default.json() == {"q": None, "limit": 10}, "Defaults query params not matched"
    print("Exercise 2 passed! ✅")

    # Test Exercise 3
    # 1. Valid data
    valid_payload = {"username": "tester", "email": "test@example.com", "password": "securepwd"}
    resp3_valid = client.post("/register", json=valid_payload)
    assert resp3_valid.status_code == 200, f"Expected 200 for valid signup, got {resp3_valid.status_code}"
    
    # 2. Invalid short username
    invalid_payload_1 = {"username": "te", "email": "test@example.com", "password": "securepwd"}
    resp3_invalid_1 = client.post("/register", json=invalid_payload_1)
    assert resp3_invalid_1.status_code == 422, "Should reject usernames shorter than 3 characters"
    
    # 3. Invalid short password
    invalid_payload_2 = {"username": "tester", "email": "test@example.com", "password": "123"}
    resp3_invalid_2 = client.post("/register", json=invalid_payload_2)
    assert resp3_invalid_2.status_code == 422, "Should reject passwords shorter than 6 characters"
    
    print("Exercise 3 passed! ✅")
    
    print("\nAll exercises passed successfully! Brilliant work! 🎉")
