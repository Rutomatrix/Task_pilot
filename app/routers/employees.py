from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse

router = APIRouter()


# --------------------------------------------------
# ✅ Get all employees
# --------------------------------------------------
@router.get("/employees/")
def get_employees(db: Session = Depends(get_db)):
    employees = db.query(Employee).all()
    
    return [
        {
            "id": e.id,
            "Emp_ID": e.Emp_ID,
            "Team_ID": e.Team_ID,
            "Name": e.Name,
            "Role": e.Role,
            "Skillset": e.Skillset,
            "Current_Tasks": e.Current_Tasks,
            "Status": e.Status,
            "Comments": e.Comments,
            "Email": e.Email,
            "created_at": e.created_at,
            "updated_at": e.updated_at,
        }
        for e in employees
    ]


# --------------------------------------------------
# ✅ Get employee by ID
# --------------------------------------------------
@router.get("/employees/{employee_id}")
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    return {
        "id": employee.id,
        "Emp_ID": employee.Emp_ID,
        "Team_ID": employee.Team_ID,
        "Name": employee.Name,
        "Role": employee.Role,
        "Skillset": employee.Skillset,
        "Current_Tasks": employee.Current_Tasks,
        "Status": employee.Status,
        "Comments": employee.Comments,
        "Email": employee.Email,
        "created_at": employee.created_at,
        "updated_at": employee.updated_at,
    }


# --------------------------------------------------
# ✅ Create a new employee
# --------------------------------------------------
@router.post("/employees/", response_model=EmployeeResponse)
def create_employee(employee_data: EmployeeCreate, db: Session = Depends(get_db)):
    new_employee = Employee(
        Emp_ID=employee_data.Emp_ID,
        Team_ID=employee_data.Team_ID,
        Name=employee_data.Name,
        Role=employee_data.Role,
        Skillset=employee_data.Skillset,
        Current_Tasks=employee_data.Current_Tasks,
        Status=employee_data.Status,
        Comments=employee_data.Comments,
        Email=employee_data.Email,
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return new_employee


# --------------------------------------------------
# ✅ Update an existing employee
# --------------------------------------------------
@router.put("/employees/{employee_id}", response_model=EmployeeResponse)
def update_employee(employee_id: int, updated_data: EmployeeUpdate, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    data = updated_data.dict(exclude_unset=True, by_alias=True)

    for key, value in data.items():
        if hasattr(employee, key):
            setattr(employee, key, value)
        else:
            print(f"⚠️ Skipping unknown field: {key}")

    db.commit()
    db.refresh(employee)

    return employee


# --------------------------------------------------
# ✅ Delete an employee
# --------------------------------------------------
@router.delete("/employees/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(employee)
    db.commit()

    return {"message": "Employee deleted successfully"}
