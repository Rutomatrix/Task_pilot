from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# ---------- Base ----------
class ProjectBase(BaseModel):
    project_id: str = Field(..., alias="Project_ID")
    name: str = Field(..., alias="Name")
    client_id: Optional[List[str]] = Field(None, alias="Client_ID")
    description: Optional[str] = Field(None, alias="Description")
    priority: Optional[str] = Field(None, alias="Priority")
    deadline: Optional[datetime] = Field(None, alias="Deadline")
    status: Optional[str] = Field(None, alias="Status")
    linked_inventory: Optional[List[str]] = Field(None, alias="Linked_Inventory")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        populate_by_name = True


# ---------- Create ----------
class ProjectCreate(ProjectBase):
    pass


# ---------- Update ----------
class ProjectUpdate(BaseModel):
    Project_ID: Optional[str]
    Name: Optional[str]
    Client_ID: Optional[List[str]]
    Description: Optional[str]
    Priority: Optional[str]
    Deadline: Optional[datetime]
    Status: Optional[str]
    Linked_Inventory: Optional[List[str]]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        populate_by_name = True


# ---------- Response ----------
class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        populate_by_name = True