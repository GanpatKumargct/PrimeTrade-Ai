from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.task import Task
from app.models.user import User, RoleEnum
from app.schemas.task import TaskCreate, TaskUpdate

def get_tasks(db: Session, user: User, skip: int = 0, limit: int = 100):
    if user.role == RoleEnum.admin:
        return db.query(Task).offset(skip).limit(limit).all()
    return db.query(Task).filter(Task.owner_id == user.id).offset(skip).limit(limit).all()

def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def create_user_task(db: Session, task_in: TaskCreate, owner_id: int):
    db_task = Task(**task_in.model_dump(), owner_id=owner_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, db_task: Task, task_in: TaskUpdate):
    update_data = task_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, db_task: Task):
    db.delete(db_task)
    db.commit()
    return True
