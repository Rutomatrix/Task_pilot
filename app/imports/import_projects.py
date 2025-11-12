from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
import pandas as pd
from io import BytesIO
from app.db.database import get_db
from app.models import Project

router = APIRouter()

def safe_value(value):
    """Return None instead of NaN."""
    return None if pd.isna(value) else value

@router.post("/import-projects/")
async def import_projects(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Import projects from a CSV or Excel file.
    Supports comma-separated values for Client_ID and Linked_Inventory.
    """
    try:
        # ✅ Validate file type
        if not (file.filename.endswith(".csv") or file.filename.endswith((".xls", ".xlsx"))):
            raise HTTPException(status_code=400, detail="Only CSV or Excel files are supported.")
        
        # ✅ Read uploaded file content
        contents = await file.read()

        # ✅ Load into pandas DataFrame
        if file.filename.endswith(".csv"):
            df = pd.read_csv(BytesIO(contents))
        else:
            df = pd.read_excel(BytesIO(contents))

        # ✅ Required columns (exact match)
        required_columns = {"Project_ID", "Name"}
        if not required_columns.issubset(df.columns):
            missing = required_columns - set(df.columns)
            raise HTTPException(status_code=400, detail=f"Missing required columns: {missing}")

        inserted = 0

        # ✅ Iterate rows
        for _, row in df.iterrows():
            # Parse Client_ID
            client_ids = []
            if pd.notna(row.get("Client_ID")):
                client_ids = [x.strip() for x in str(row["Client_ID"]).split(",") if x.strip()]

            # Parse Linked_Inventory
            linked_inventory = []
            if pd.notna(row.get("Linked_Inventory")):
                linked_inventory = [x.strip() for x in str(row["Linked_Inventory"]).split(",") if x.strip()]

            # ✅ Create project instance
            project = Project(
                Project_ID=safe_value(row["Project_ID"]),
                Name=safe_value(row["Name"]),
                Client_ID=client_ids,
                Description=safe_value(row.get("Description")),
                Priority=safe_value(row.get("Priority")),
                Deadline=safe_value(row.get("Deadline")),
                Status=safe_value(row.get("Status")),
                Linked_Inventory=linked_inventory,
            )

            # ✅ Skip duplicates
            existing = db.query(Project).filter(Project.Project_ID == project.Project_ID).first()
            if existing:
                continue

            db.add(project)
            inserted += 1

        db.commit()

        return {"message": f"✅ Successfully imported {inserted} projects."}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error importing projects: {str(e)}")