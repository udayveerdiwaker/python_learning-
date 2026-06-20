# ==============================================================================
# main.py - Introductory FastAPI Application Server
# ==============================================================================
# Run this server using command: uvicorn main:app --reload
# Then open your browser at: http://127.0.0.1:8000/docs to explore the interactive API docs!

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional

# 1. Initialize the FastAPI application
# This 'app' object represents our main API backend server.
app = FastAPI(
    title="FastAPI Learning API",
    description="This API teaches you path/query parameters, request bodies, and validation.",
    version="1.0.0"
)

# ------------------------------------------------------------------------------
# 2. Pydantic Schemas (Data Validation Models)
# ------------------------------------------------------------------------------
# Pydantic is a library used to validate data. By extending BaseModel, we declare
# the expected structure of incoming JSON requests. FastAPI uses this to validate
# data type inputs (e.g. returning a 422 Unprocessable Entity error if types mismatch).

class CourseItem(BaseModel):
    title: str = Field(..., description="The name of the learning course", min_length=2)
    category: str = Field("Programming", description="Course category")
    price: float = Field(..., description="Cost of the course", gt=0)  # price must be greater than 0
    duration_hours: Optional[int] = Field(None, description="Course length in hours", ge=1)

# In-memory database list representing data records:
courses_db = [
    {"id": 1, "title": "Python Basics", "category": "Programming", "price": 19.99, "duration_hours": 12},
    {"id": 2, "title": "Advanced SQL", "category": "Databases", "price": 29.99, "duration_hours": 8}
]


# ------------------------------------------------------------------------------
# 3. API Route Operations
# ------------------------------------------------------------------------------

# Root endpoint: Returns a static message.
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Basics Module! Visit /docs for the Swagger UI."}


# GET Endpoint with a Path Parameter:
# Path parameters are wrapped in curly braces {course_id} in the route decorator,
# and declared as arguments in the python function.
@app.get("/courses/{course_id}")
def read_course(course_id: int):
    """
    Retrieves a specific course by its path ID parameter.
    """
    for course in courses_db:
        if course["id"] == course_id:
            return course
            
    # Raise a 404 HTTP Exception if the course is not found in database list
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Course ID {course_id} was not found"
    )


# GET Endpoint with Query Parameters:
# Arguments that are not defined in the route path are automatically treated
# as query parameters (e.g. /courses?category=Programming&limit=5)
@app.get("/courses/")
def list_courses(category: Optional[str] = None, limit: int = 10):
    """
    Lists courses with optional category filter and response size limit.
    """
    results = courses_db
    
    # Filter by category if query param is provided
    if category:
        results = [c for c in results if c["category"].lower() == category.lower()]
        
    # Slice the list up to the specified limit
    return results[:limit]


# POST Endpoint with Request Body & Pydantic Validation:
# By declaring a parameter 'course' with a type hint of CourseItem (Pydantic model),
# FastAPI expects a JSON payload matching the CourseItem schema.
@app.post("/courses/", status_code=status.HTTP_201_CREATED)
def create_course(course: CourseItem):
    """
    Creates a new course entry. Incoming data is validated automatically by Pydantic.
    """
    # Create the new database record dict, allocating an ID
    new_id = max(c["id"] for c in courses_db) + 1 if courses_db else 1
    
    # Convert Pydantic model to dictionary:
    course_dict = course.model_dump()
    course_dict["id"] = new_id
    
    courses_db.append(course_dict)
    
    # Return the newly created course object
    return course_dict


# ------------------------------------------------------------------------------
# 4. Starting the Server Programmatically
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    # You can also run the file directly: python main.py
    # This runs the app object using uvicorn on localhost, port 8000
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
