from fastapi import FastAPI
from app.models import Base
from app.db.database import engine
from app.imports.import_clients import router as import_clients_router
from fastapi.middleware.cors import CORSMiddleware
from app.routers.clients import router as clients_router  # ✅ Add this line

app = FastAPI(title="TaskPilot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create DB tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(import_clients_router, prefix="/api", tags=["Clients"])
app.include_router(clients_router, prefix="/api", tags=["Clients"])  # ✅ Add this

@app.get("/")
def read_root():
    return {"message": "FastAPI with PostgreSQL is connected successfully!"}