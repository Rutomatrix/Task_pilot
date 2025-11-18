from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
import pandas as pd
from io import BytesIO
from datetime import datetime
from app.db.database import get_db
from app.models import Task

router = APIRouter()

@router.post("/import-tasks/")
async def import_tasks(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Import tasks from an uploaded CSV or Excel file.
    """
    try:
        # ✅ Validate file type
        if not (file.filename.endswith('.csv') or file.filename.endswith(('.xls', '.xlsx'))):
            raise HTTPException(status_code=400, detail="Only CSV or Excel files are supported.")
        
        # ✅ Read file
        contents = await file.read()
        df = pd.read_csv(BytesIO(contents)) if file.filename.endswith('.csv') else pd.read_excel(BytesIO(contents))

        # ✅ Validate required columns
        required_columns = {"Task_ID", "Task_Name"}
        missing = required_columns - set(df.columns)
        if missing:
            raise HTTPException(status_code=400, detail=f"Missing required columns: {missing}")

        # ✅ Convert arrays (comma-separated strings -> list)
        array_fields = ["Project_ID", "Assigned_To", "Dependencies", "Skills_Required"]
        for field in array_fields:
            if field in df.columns:
                df[field] = df[field].apply(
                    lambda x: [i.strip() for i in str(x).split(',')] if pd.notna(x) and str(x).strip() != "" else None
                )

        # ✅ Parse datetime safely
        if "Deadline" in df.columns:
            df["Deadline"] = pd.to_datetime(df["Deadline"], errors="coerce")

         # Convert NaN in Description to empty string
        if "Description" in df.columns:
            df["Description"] = df["Description"].fillna("")

        inserted = 0
        for index, row in df.iterrows():
            try:
                task_id = row.get("Task_ID")
                if not task_id:
                    continue

                # ✅ Skip duplicate Task_IDs
                existing = db.query(Task).filter(Task.Task_ID == task_id).first()
                if existing:
                    continue

                # ✅ Build task object
                task = Task(
                    Task_ID=task_id,
                    Task_Name=row.get("Task_Name"),
                    Project_ID=row.get("Project_ID"),
                    Type=row.get("Type"),
                    Assigned_To=row.get("Assigned_To"),
                    Priority=row.get("Priority"),
                    Deadline=row.get("Deadline").to_pydatetime() if pd.notna(row.get("Deadline")) else None,
                    Status=row.get("Status"),
                    Dependencies=row.get("Dependencies"),
                    Description=row.get("Description"),
                    Skills_Required=row.get("Skills_Required"),
                )

                db.add(task)
                inserted += 1
                print(f"✅ Added task: {task_id}")

            except Exception as row_error:
                print(f"⚠️ Skipping row {index} due to error: {row_error}")
                continue

        db.commit()
        print("✅ All tasks committed successfully!")
        return {"message": f"Successfully imported {inserted} tasks."}

    except Exception as e:
        db.rollback()
        print("❌ Import failed:", str(e))
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")
