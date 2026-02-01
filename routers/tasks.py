from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.dependencies import get_db, get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=list[schemas.Task])
def read_tasks(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.get_tasks(db, user_id=current_user.id)

@router.post("/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_user_task(db=db, task=task, user_id=current_user.id)

@router.put("/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_task = crud.update_task(db, task_id=task_id, user_id=current_user.id, task_update=task)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.patch("/{task_id}/complete", response_model=schemas.Task)
def mark_task_complete(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_task = crud.update_task_completion(db, task_id=task_id, user_id=current_user.id, completed=True)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.patch("/{task_id}/incomplete", response_model=schemas.Task)
def mark_task_incomplete(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_task = crud.update_task_completion(db, task_id=task_id, user_id=current_user.id, completed=False)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.delete("/{task_id}")
def remove_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    success = crud.delete_task(db, task_id=task_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}