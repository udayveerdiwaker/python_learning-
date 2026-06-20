# crud.py
from sqlalchemy.orm import Session
from models import DBTask
from schemas import TaskCreate, TaskUpdate
from typing import Optional

def get_tasks(db: Session, completed: Optional[bool] = None, priority: Optional[str] = None, limit: int = 50):
    """
    Retrieves tasks with optional filters for completion status and priority level.
    """
    query = db.query(DBTask)
    if completed is not None:
        query = query.filter(DBTask.completed == completed)
    if priority:
        query = query.filter(DBTask.priority == priority)
    return query.limit(limit).all()

def get_task_by_id(db: Session, task_id: int):
    return db.query(DBTask).filter(DBTask.id == task_id).first()

def create_task(db: Session, task: TaskCreate):
    db_task = DBTask(
        title=task.title,
        description=task.description,
        priority=task.priority,
        due_date=task.due_date
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task_update: TaskUpdate):
    db_task = get_task_by_id(db, task_id)
    if not db_task:
        return None
        
    update_data = task_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)
        
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    db_task = get_task_by_id(db, task_id)
    if db_task:
        db.delete(db_task)
        db.commit()
        return True
    return False
