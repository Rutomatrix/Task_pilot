from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ---------- Base ----------
class ClientBase(BaseModel):
    client_id: str = Field(..., alias="Client_ID")
    client_name: str = Field(..., alias="Client_Name")
    description: Optional[str] = Field(None, alias="Description")
    type: Optional[str] = Field(None, alias="Type")
    status: Optional[str] = Field(None, alias="Status")
    active_projects: Optional[int] = Field(0, alias="Active_Projects")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        populate_by_name = True


# ---------- Create ----------
class ClientCreate(ClientBase):
    pass


# ---------- Update ----------
class ClientUpdate(BaseModel):
    Client_ID: Optional[str]
    Client_Name: Optional[str]
    Description: Optional[str]
    Type: Optional[str]
    Status: Optional[str]
    Active_Projects: Optional[int]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        populate_by_name = True


# ---------- Response ----------
class ClientResponse(ClientBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        populate_by_name = True
