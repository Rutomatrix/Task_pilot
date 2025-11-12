from fastapi import APIRouter, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends
import pandas as pd
from io import BytesIO
from app.db.database import get_db
from app.models import Team  # Make sure Team model is defined

router = APIRouter()

@router.post("/import-teams/")
async def import_teams(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Import teams from an uploaded CSV or Excel file.
    """
    try:
        # Check file type
        if not (file.filename.endswith('.csv') or file.filename.endswith(('.xls', '.xlsx'))):
            raise HTTPException(status_code=400, detail="Only CSV or Excel files are supported.")
        
        # Read file content
        contents = await file.read()

        # Load data into a pandas DataFrame
        if file.filename.endswith('.csv'):
            df = pd.read_csv(BytesIO(contents))
        else:
            df = pd.read_excel(BytesIO(contents))

        # Validate required columns
        required_columns = {"Team_ID", "Category"}
        if not required_columns.issubset(df.columns):
            raise HTTPException(
                status_code=400,
                detail=f"Missing required columns: {required_columns - set(df.columns)}"
            )

        # Iterate through rows and insert into DB
        inserted = 0
        for _, row in df.iterrows():
            team = Team(
                Team_ID=row["Team_ID"],
                Category=row["Category"]
            )

            # Avoid duplicate Team_IDs
            existing = db.query(Team).filter(Team.Team_ID == team.Team_ID).first()
            if existing:
                continue  # Skip duplicates

            db.add(team)
            inserted += 1

        db.commit()
        return {"message": f"Successfully imported {inserted} teams."}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
