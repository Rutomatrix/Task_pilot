from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter()


# ✅ Get all tasks
@router.get("/tasks/")
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return [
        {
            "id": t.id,
            "task_id": t.Task_ID,
            "task_name": t.Task_Name,
            "project_id": t.Project_ID,
            "type": t.Type,
            "assigned_to": t.Assigned_To,
            "priority": t.Priority,
            "deadline": t.Deadline,
            "status": t.Status,
            "dependencies": t.Dependencies,
            "description": t.Description,
            "skills_required": t.Skills_Required,
        }
        for t in tasks
    ]


# ✅ Get task by ID
@router.get("/tasks/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {
        "id": task.id,
        "task_id": task.Task_ID,
        "task_name": task.Task_Name,
        "project_id": task.Project_ID,
        "type": task.Type,
        "assigned_to": task.Assigned_To,
        "priority": task.Priority,
        "deadline": task.Deadline,
        "status": task.Status,
        "dependencies": task.Dependencies,
        "description": task.Description,
        "skills_required": task.Skills_Required,
    }


# ✅ Create new task
@router.post("/tasks/", response_model=TaskResponse)
def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(
        Task_ID=task_data.task_id,
        Task_Name=task_data.task_name,
        Project_ID=task_data.project_id,
        Type=task_data.type,
        Assigned_To=task_data.assigned_to,
        Priority=task_data.priority,
        Deadline=task_data.deadline,
        Status=task_data.status,
        Dependencies=task_data.dependencies,
        Description=task_data.description,
        Skills_Required=task_data.skills_required,
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


# ✅ Update existing task
@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, updated_data: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    data = updated_data.dict(exclude_unset=True, by_alias=True)
    for key, value in data.items():
        if hasattr(task, key):
            setattr(task, key, value)
        else:
            print(f"⚠️ Skipping unknown attribute {key}")

    db.commit()
    db.refresh(task)
    return task


# ✅ Delete task
@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}
