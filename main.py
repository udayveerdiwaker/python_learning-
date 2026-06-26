# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/users")
# def get_user(username: str, age: int):
#     return {
#         "username": username,
#         "age": age
#     }


# from fastapi import FastAPI
# from pydantic import BaseModel

# app = FastAPI()

# users = []

# class User(BaseModel):
#     username: str
#     password: str

# @app.post("/register")
# def register(user: User):
#     # Convert the user data into a Python dictionary and add it to our list
#     users.append(user.dict())
#     # Return a success message back to the client
#     return {"message": f"User created successfully name: {user.username}, password: {user.password}"}

    
# @app.get("/read")
# def read():
#     return users


from fastapi import FastAPI

app = FastAPI()

@app.get("/students")
def get_students():
    return [{"id": 1, "name": "Shiva"}]

@app.post("/students")
def create_student():
    return {"message": "Student created"}

@app.put("/students/{id}")
def update_student(id: int):
    return {"message": f"Student {id} updated"}

@app.delete("/students/{id}")
def delete_student(id: int):
    return {"message": f"Student {id} deleted"}

