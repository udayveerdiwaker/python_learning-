# main.py
import sys
from pathlib import Path

# Add parent directory for imports
sys.path.append(str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from db_helper import get_db
import crud
import schemas

app = FastAPI(
    title="Task Manager API Service",
    description="Project 3: Manage tasks, priorities, deadlines, and project execution.",
    version="1.0.0"
)

@app.get("/tasks", response_model=List[schemas.TaskResponse], tags=["Tasks"])
def read_tasks(
    completed: Optional[bool] = None, 
    priority: Optional[str] = None, 
    db: Session = Depends(get_db)
):
    """
    Lists tasks. Allows filtering by completed status and priority level.
    """
    return crud.get_tasks(db, completed=completed, priority=priority)


@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse, tags=["Tasks"])
def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.get_task_by_id(db, task_id)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found."
        )
    return db_task


@app.post("/tasks", response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED, tags=["Tasks"])
def create_new_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, task)


@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse, tags=["Tasks"])
def update_task_details(task_id: int, task_update: schemas.TaskUpdate, db: Session = Depends(get_db)):
    db_task = crud.get_task_by_id(db, task_id)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found."
        )
    return crud.update_task(db, task_id, task_update)


@app.delete("/tasks/{task_id}", status_code=status.HTTP_200_OK, tags=["Tasks"])
def delete_task_record(task_id: int, db: Session = Depends(get_db)):
    success = crud.delete_task(db, task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found."
        )
    return {"message": "Task deleted successfully."}
