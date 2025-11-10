from fastapi import APIRouter, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends
import pandas as pd
from io import BytesIO
from app.db.database import get_db
from app.models import Client

router = APIRouter()

@router.post("/import-clients/")
async def import_clients(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Import clients from an uploaded CSV or Excel file.
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
        required_columns = {"Client_ID", "Client_Name"}
        if not required_columns.issubset(df.columns):
            raise HTTPException(status_code=400, detail=f"Missing required columns: {required_columns - set(df.columns)}")

        # Iterate through rows and insert into DB
        inserted = 0
        for _, row in df.iterrows():
            client = Client(
                Client_ID=row["Client_ID"],
                Client_Name=row["Client_Name"],
                Description=row.get("Description"),
                Type=row.get("Type"),
                Status=row.get("Status"),
                Active_Projects=row.get("Active_Projects", 0)
            )

            # Avoid duplicate Client_IDs
            existing = db.query(Client).filter(Client.Client_ID == client.Client_ID).first()
            if existing:
                continue  # Skip duplicates

            db.add(client)
            inserted += 1

        db.commit()
        return {"message": f"Successfully imported {inserted} clients."}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
