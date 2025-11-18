from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
import pandas as pd
from io import BytesIO

from app.db.database import get_db
from app.models import Employee

router = APIRouter()


@router.post("/import-employees/")
async def import_employees(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Import employees from CSV or Excel file.
    Required columns: Emp_ID, Team_ID, Name
    """

    try:
        # --------------------------------------------------
        # Validate file type
        # --------------------------------------------------
        if not (file.filename.endswith(".csv") or file.filename.endswith((".xls", ".xlsx"))):
            raise HTTPException(status_code=400, detail="Only CSV or Excel files are supported.")

        # --------------------------------------------------
        # Read file
        # --------------------------------------------------
        content = await file.read()

        df = pd.read_csv(BytesIO(content)) if file.filename.endswith(".csv") else pd.read_excel(BytesIO(content))

        # Strip column names
        df.columns = [col.strip() for col in df.columns]

        # --------------------------------------------------
        # Validate required columns
        # --------------------------------------------------
        required_columns = {"Emp_ID", "Team_ID", "Name"}
        missing = required_columns - set(df.columns)

        if missing:
            raise HTTPException(status_code=400, detail=f"Missing required columns: {missing}")
        
        print('after the required columns')

        # Convert Emp_ID and Team_ID to string always
        if "Emp_ID" in df.columns:
            df["Emp_ID"] = df["Emp_ID"].astype(str).str.strip()

        if "Team_ID" in df.columns:
            df["Team_ID"] = df["Team_ID"].astype(str).str.strip()

        # --------------------------------------------------
        # Convert comma-separated list fields into arrays
        # --------------------------------------------------
        array_fields = ["Skillset", "Current_Tasks"]

        for field in array_fields:
            if field in df.columns:
                df[field] = df[field].apply(
                    lambda x: [i.strip() for i in str(x).split(",")] if pd.notna(x) and str(x).strip() != "" else []
                )

        inserted = 0

        # --------------------------------------------------
        # Process rows one-by-one
        # --------------------------------------------------
        print('one')
        for idx, row in df.iterrows():
            try:
                emp_id = str(row["Emp_ID"]).strip()
                if not emp_id:
                    continue

                # Skip duplicates
                if db.query(Employee).filter(Employee.Emp_ID == emp_id).first():
                    print(f"⚠️ Duplicate Emp_ID skipped: {emp_id}")
                    continue

                if "Email" in df.columns:
                    email = row.get("Email")
                    if email and db.query(Employee).filter(Employee.Email == email).first():
                        print(f"⚠️ Duplicate Email skipped: {email}")
                        continue
                else:
                    email = None  # optional

                # --------------------------------------------------
                # Create employee
                # --------------------------------------------------
                employee = Employee(
                    Emp_ID=row.get("Emp_ID"),
                    Team_ID=row.get("Team_ID"),
                    Name=row.get("Name"),
                    Role=row.get("Role"),
                    Skillset=row.get("Skillset") if isinstance(row.get("Skillset"), list) else [],
                    Current_Tasks=row.get("Current_Tasks") if isinstance(row.get("Current_Tasks"), list) else [],
                    Status=row.get("Status"),
                    Comments=row.get("Comments"),
                    Email=row.get("Email"),
                )

                print('employee',employee)
                db.add(employee)
                inserted += 1
                print(f"✅ Added employee: {emp_id}")

            except Exception as row_error:
                print(f"⚠️ Row {idx} skipped due to error: {row_error}")
                continue
        print('before commit')
        db.commit()
        print("✅ Employees imported successfully!")
        return {"message": f"Successfully imported {inserted} employees."}

    except Exception as e:
        db.rollback()
        print("❌ Import failed:", str(e))
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")
