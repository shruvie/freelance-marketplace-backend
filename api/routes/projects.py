from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import Project, User
from api.deps import get_current_active_user
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class ProjectCreate(BaseModel):
    title: str
    description: str
    category: str
    budget: float

class ProjectResponse(ProjectCreate):
    id: int
    client_id: int
    status: str

    class Config:
        from_attributes = True

@router.get("/", response_model=List[ProjectResponse])
def get_projects(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    projects = db.query(Project).offset(skip).limit(limit).all()
    return projects

@router.post("/", response_model=ProjectResponse)
def create_project(project_in: ProjectCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    if current_user.role != 'client':
        raise HTTPException(status_code=403, detail="Only clients can create projects")
    
    db_project = Project(
        client_id=current_user.id,
        title=project_in.title,
        description=project_in.description,
        category=project_in.category,
        budget=project_in.budget
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project
