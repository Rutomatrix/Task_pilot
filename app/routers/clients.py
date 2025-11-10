from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import Client
from app.schemas.client import ClientCreate, ClientUpdate, ClientResponse

router = APIRouter()


# ✅ Get all clients
@router.get("/clients/")
def get_clients(db: Session = Depends(get_db)):
    clients = db.query(Client).all()
    return [
        {
            "id": c.id,
            "client_id": c.Client_ID,
            "client_name": c.Client_Name,
            "description": c.Description,
            "type": c.Type,
            "status": c.Status,
            "active_projects": c.Active_Projects,
        }
        for c in clients
    ]



# ✅ Get client by ID
@router.get("/clients/{client_id}")
def get_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        return {"error": "Client not found"}
    
    return {
        "id": client.id,
        "client_id": client.Client_ID,
        "client_name": client.Client_Name,
        "description": client.Description,
        "type": client.Type,
        "status": client.Status,
        "active_projects": client.Active_Projects,
    }


# ✅ Create new client
@router.post("/clients/", response_model=ClientResponse)
def create_client(client_data: ClientCreate, db: Session = Depends(get_db)):
    new_client = Client(
        Client_ID=client_data.client_id,
        Client_Name=client_data.client_name,
        Description=client_data.description,
        Type=client_data.type,
        Status=client_data.status,
        Active_Projects=client_data.active_projects,
    )
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client


# ✅ Update existing client
@router.put("/clients/{client_id}", response_model=ClientResponse)
def update_client(client_id: int, updated_data: ClientUpdate, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    data = updated_data.dict(exclude_unset=True, by_alias=True)  # use alias names
    for key, value in data.items():
        if hasattr(client, key):
            setattr(client, key, value)
        else:
            print(f"⚠️ Skipping unknown attribute {key}")

    db.commit()
    db.refresh(client)
    return client


# ✅ Delete client
@router.delete("/clients/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    db.delete(client)
    db.commit()
    return {"message": "Client deleted successfully"}
