from pydantic import BaseModel, Field
from typing import Optional

# Base schema shared by create/update/response
class TeamBase(BaseModel):
    Team_ID: str = Field(..., alias="Team_ID")
    Category: str = Field(..., alias="Category")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True  # allows both alias & field names
        populate_by_name = True


# Schema for creating a team
class TeamCreate(TeamBase):
    pass


# Schema for updating a team (all fields optional)
class TeamUpdate(BaseModel):
    Team_ID: Optional[str]
    Category: Optional[str]


# Schema for response (includes id)
class TeamResponse(TeamBase):
    id: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
