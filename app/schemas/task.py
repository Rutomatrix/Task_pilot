from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class TaskBase(BaseModel):
    task_id: str = Field(..., alias="Task_ID")
    task_name: Optional[str] = Field(None, alias="Task_Name")
    project_id: Optional[List[str]] = Field(None, alias="Project_ID")
    type: Optional[str] = Field(None, alias="Type")
    assigned_to: Optional[List[str]] = Field(None, alias="Assigned_To")
    priority: Optional[str] = Field(None, alias="Priority")
    deadline: Optional[datetime] = Field(None, alias="Deadline")
    status: Optional[str] = Field(None, alias="Status")
    dependencies: Optional[List[str]] = Field(None, alias="Dependencies")
    description: Optional[str] = Field(None, alias="Description")
    skills_required: Optional[List[str]] = Field(None, alias="Skills_Required")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        populate_by_name = True


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    Task_ID: Optional[str]
    Task_Name: Optional[str]
    Project_ID: Optional[List[str]]
    Type: Optional[str]
    Assigned_To: Optional[List[str]]
    Priority: Optional[str]
    Deadline: Optional[datetime]
    Status: Optional[str]
    Dependencies: Optional[List[str]]
    Description: Optional[str]
    Skills_Required: Optional[List[str]]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        populate_by_name = True


class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        populate_by_name = True
