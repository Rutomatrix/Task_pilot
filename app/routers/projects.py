from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import Project
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse

router = APIRouter()

# ✅ Get all projects
@router.get("/projects/")
def get_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    return [
        {
            "id": p.id,
            "project_id": p.Project_ID,
            "name": p.Name,
            "client_id": p.Client_ID,
            "description": p.Description,
            "priority": p.Priority,
            "deadline": p.Deadline,
            "status": p.Status,
            "linked_inventory": p.Linked_Inventory,
        }
        for p in projects
    ]


# ✅ Get project by ID
@router.get("/projects/{project_id}")
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {
        "id": project.id,
        "project_id": project.Project_ID,
        "name": project.Name,
        "client_id": project.Client_ID,
        "description": project.Description,
        "priority": project.Priority,
        "deadline": project.Deadline,
        "status": project.Status,
        "linked_inventory": project.Linked_Inventory,
    }


# ✅ Create new project
@router.post("/projects/", response_model=ProjectResponse)
def create_project(project_data: ProjectCreate, db: Session = Depends(get_db)):
    print('ProjectCreate',ProjectCreate)
    new_project = Project(
        Project_ID=project_data.project_id,
        Name=project_data.name,
        Client_ID=project_data.client_id,
        Description=project_data.description,
        Priority=project_data.priority,
        Deadline=project_data.deadline,
        Status=project_data.status,
        Linked_Inventory=project_data.linked_inventory,
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project


# ✅ Update existing project
@router.put("/projects/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, updated_data: ProjectUpdate, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    data = updated_data.dict(exclude_unset=True, by_alias=True)
    for key, value in data.items():
        if hasattr(project, key):
            setattr(project, key, value)
        else:
            print(f"⚠️ Skipping unknown attribute {key}")

    db.commit()
    db.refresh(project)
    return project


# ✅ Delete project
@router.delete("/projects/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    db.delete(project)
    db.commit()
    return {"message": "Project deleted successfully"}
