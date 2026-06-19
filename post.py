# from fastapi import FastAPI

# app = FastAPI()

# @app.post("/users")
# def create_user():
#     return {
#         "message": "User Created"
#     }

# from fastapi import APIRouter
# from pydantic import BaseModel



# router = APIRouter()

# class User(BaseModel):
#     name: str
#     email: str

# @router.post("/users")
# def create_user(user: User):
#     return {
#         "name": user.name,
#         "email": user.email
#     }