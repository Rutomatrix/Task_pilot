from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import Team
from app.schemas.team import TeamCreate, TeamUpdate, TeamResponse

router = APIRouter()


# ✅ Get all teams
@router.get("/teams/")
def get_teams(db: Session = Depends(get_db)):
    teams = db.query(Team).all()
    return [
        {
            "id": t.id,
            "team_id": t.Team_ID,
            "category": t.Category,
        }
        for t in teams
    ]


# ✅ Get team by ID
@router.get("/teams/{team_id}")
def get_team(team_id: int, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    return {
        "id": team.id,
        "team_id": team.Team_ID,
        "category": team.Category,
    }


# ✅ Create new team
@router.post("/teams/", response_model=TeamResponse)
def create_team(team_data: TeamCreate, db: Session = Depends(get_db)):
    new_team = Team(
        Team_ID=team_data.team_id,
        Category=team_data.category,
    )
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    return new_team


# ✅ Update existing team
@router.put("/teams/{team_id}", response_model=TeamResponse)
def update_team(team_id: int, updated_data: TeamUpdate, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    data = updated_data.dict(exclude_unset=True, by_alias=True)
    for key, value in data.items():
        if hasattr(team, key):
            setattr(team, key, value)
        else:
            print(f"⚠️ Skipping unknown attribute {key}")

    db.commit()
    db.refresh(team)
    return team


# ✅ Delete team
@router.delete("/teams/{team_id}")
def delete_team(team_id: int, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    db.delete(team)
    db.commit()
    return {"message": "Team deleted successfully"}
