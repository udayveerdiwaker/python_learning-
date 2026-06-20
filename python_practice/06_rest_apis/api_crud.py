# ==============================================================================
# api_crud.py - Full REST API with HTTP Verbs, Status Codes & Query Options
# ==============================================================================
# Run this server using command: uvicorn api_crud:app --reload
# View interactive documentation at: http://127.0.0.1:8000/docs

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI(
    title="RESTful Task API",
    description="A demonstration of REST API design principles and HTTP verbs.",
    version="1.0.0"
)

# ------------------------------------------------------------------------------
# 1. Schemas for Input Validation & Output Response
# ------------------------------------------------------------------------------
# Creating separate schemas for creation and updates is standard REST practice.

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Task Title")
    description: Optional[str] = Field(None, description="Detailed explanation of the task")
    completed: bool = Field(default=False, description="Completion status of the task")

class TaskUpdate(BaseModel):
    # Optional fields for partial updates (PATCH) or full updates (PUT)
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool


# 2. In-Memory Task Store
tasks_db = [
    {"id": 1, "title": "Setup MySQL Database", "description": "Run setup_db.sql script", "completed": True},
    {"id": 2, "title": "Learn FastAPI Basics", "description": "Practice path and query parameter exercises", "completed": False}
]


# ------------------------------------------------------------------------------
# 3. REST API Routes
# ------------------------------------------------------------------------------

# GET /tasks -> Retrieve all tasks
@app.get("/tasks", response_model=List[TaskResponse], status_code=status.HTTP_200_OK, tags=["Tasks"])
def get_all_tasks(completed: Optional[bool] = None):
    """
    GET (READ): Lists all tasks. Supports filtering by completed status.
    Example: /tasks?completed=true
    """
    if completed is not None:
        return [t for t in tasks_db if t["completed"] == completed]
    return tasks_db


# GET /tasks/{task_id} -> Retrieve a single task by ID
@app.get("/tasks/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK, tags=["Tasks"])
def get_task(task_id: int):
    """
    GET (READ): Retrieves details of a specific task.
    Returns 404 if the task ID does not exist.
    """
    for task in tasks_db:
        if task["id"] == task_id:
            return task
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task with ID {task_id} not found."
    )


# POST /tasks -> Create a new task
@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, tags=["Tasks"])
def create_task(task_input: TaskCreate):
    """
    POST (CREATE): Creates a new task.
    Returns 201 Created and the created task object.
    """
    # Allocate a new unique ID
    new_id = max(t["id"] for t in tasks_db) + 1 if tasks_db else 1
    
    # Construct task dictionary
    new_task = task_input.model_dump()
    new_task["id"] = new_id
    
    tasks_db.append(new_task)
    return new_task


# PUT /tasks/{task_id} -> Full Update of a task
@app.put("/tasks/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK, tags=["Tasks"])
def update_task_full(task_id: int, task_input: TaskCreate):
    """
    PUT (UPDATE): Performs a full update, replacing the entire resource.
    If the resource does not exist, it raises a 404 error.
    """
    for task in tasks_db:
        if task["id"] == task_id:
            # Overwrite all fields with the incoming body data
            task["title"] = task_input.title
            task["description"] = task_input.description
            task["completed"] = task_input.completed
            return task
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task with ID {task_id} not found."
    )


# PATCH /tasks/{task_id} -> Partial Update of a task
@app.patch("/tasks/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK, tags=["Tasks"])
def update_task_partial(task_id: int, task_input: TaskUpdate):
    """
    PATCH (UPDATE): Performs a partial update, modifying only the fields provided.
    """
    for task in tasks_db:
        if task["id"] == task_id:
            # Convert incoming model data to dictionary, excluding unset parameters
            update_data = task_input.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                task[key] = value
            return task
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task with ID {task_id} not found."
    )


# DELETE /tasks/{task_id} -> Delete a task
@app.delete("/tasks/{task_id}", status_code=status.HTTP_200_OK, tags=["Tasks"])
def delete_task(task_id: int):
    """
    DELETE: Deletes a task by its ID.
    """
    for index, task in enumerate(tasks_db):
        if task["id"] == task_id:
            removed = tasks_db.pop(index)
            return {"message": f"Task '{removed['title']}' deleted successfully."}
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task with ID {task_id} not found."
    )
