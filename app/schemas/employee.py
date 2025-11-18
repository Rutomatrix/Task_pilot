from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# ---------- Base Schema ----------
class EmployeeBase(BaseModel):
    Emp_ID: str = Field(..., alias="Emp_ID")
    Team_ID: Optional[str] = Field(None, alias="Team_ID")
    Name: Optional[str] = Field(None, alias="Name")
    Role: Optional[str] = Field(None, alias="Role")
    Skillset: Optional[List[str]] = Field(default_factory=list, alias="Skillset")
    Current_Tasks: Optional[List[str]] = Field(default_factory=list, alias="Current_Tasks")
    Status: Optional[str] = Field(None, alias="Status")
    Comments: Optional[str] = Field(None, alias="Comments")
    Email: Optional[str] = Field(None, alias="Email")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        populate_by_name = True


# ---------- Create Schema ----------
class EmployeeCreate(EmployeeBase):
    """
    All fields from EmployeeBase, Emp_ID is required,
    others are optional or default.
    """
    pass


# ---------- Update Schema ----------
class EmployeeUpdate(BaseModel):
    Emp_ID: Optional[str] = Field(None, alias="Emp_ID")
    Team_ID: Optional[str] = Field(None, alias="Team_ID")
    Name: Optional[str] = Field(None, alias="Name")
    Role: Optional[str] = Field(None, alias="Role")
    Skillset: Optional[List[str]] = Field(None, alias="Skillset")
    Current_Tasks: Optional[List[str]] = Field(None, alias="Current_Tasks")
    Status: Optional[str] = Field(None, alias="Status")
    Comments: Optional[str] = Field(None, alias="Comments")
    Email: Optional[str] = Field(None, alias="Email")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        populate_by_name = True


# ---------- Response Schema ----------
class EmployeeResponse(EmployeeBase):
    id: int
    created_at: datetime
    updated_at: datetime
    emp_id: str
    name: str
    email: str | None
    skillset: List[str] 

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        populate_by_name = True
