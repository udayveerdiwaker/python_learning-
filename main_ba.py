# Import FastAPI (the web framework), HTTPException (for error handling) and BaseModel (for data validation)
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Initialize the FastAPI application
app = FastAPI()

# A simple in-memory database (a list) to store user data temporarily
users = []

# Define the structure of the data we expect from the client (data validation)
class User(BaseModel):
    name: str   # The user's name must be a string
    email: str  # The user's email must be a string

# Endpoint to CREATE a new user (POST request)
@app.post("/users_create")
def create_user(user: User):
    # Convert the user data into a Python dictionary and add it to our list
    users.append(user.dict())
    # Return a success message back to the client
    return {"message": f"User created successfully name: {user.name}, email: {user.email}"}

# Endpoint to READ/GET all users (GET request)
@app.get("/users_read")
def get_users():
    # Return the list of all users we have saved so far
    return users

# Endpoint to UPDATE a user's details by their email (PUT request)
@app.put("/users_update/{email}")
def update_user(email: str, updated_user: User):
    for user in users:
        if user["email"] == email:
            user["name"] = updated_user.name
            user["email"] = updated_user.email
            return {"message": f"User with email {email} updated successfully"}
    # If user is not found, return a 404 error
    raise HTTPException(status_code=404, detail="User not found")

# Endpoint to DELETE a user by their email (DELETE request)
@app.delete("/users_delete/{email}")
def delete_user(email: str):
    for idx, user in enumerate(users):
        if user["email"] == email:
            users.pop(idx)
            return {"message": f"User with email {email} deleted successfully"}
    # If user is not found, return a 404 error
    raise HTTPException(status_code=404, detail="User not found")

