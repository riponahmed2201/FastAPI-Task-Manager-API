from sqlalchemy.orm import Session
from . import models, schemas

def get_tasks(db: Session, user_id: int):
    return db.query(models.Task).filter(models.Task.owner_id == user_id).all()

def create_user_task(db: Session, task: schemas.TaskCreate, user_id: int):
    db_task = models.Task(**task.model_dump(), owner_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, user_id: int, task_update: schemas.TaskCreate):
    db_task = db.query(models.Task).filter(
        models.Task.id == task_id, 
        models.Task.owner_id == user_id
    ).first()
    if db_task:
        for key, value in task_update.model_dump(exclude_unset=True).items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
    return db_task

def update_task_completion(db: Session, task_id: int, user_id: int, completed: bool):
    db_task = db.query(models.Task).filter(
        models.Task.id == task_id, 
        models.Task.owner_id == user_id
    ).first()
    if db_task:
        db_task.completed = completed
        db.commit()
        db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int, user_id: int):
    db_task = db.query(models.Task).filter(
        models.Task.id == task_id, 
        models.Task.owner_id == user_id
    ).first()
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task