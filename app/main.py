from fastapi import FastAPI
from app.models import Base
from app.db.database import engine
from fastapi.middleware.cors import CORSMiddleware
from app.routers.clients import router as clients_router
from app.imports.import_clients import router as import_clients_router
from app.routers.teams import router as teams_router
from app.imports.import_teams import router as import_teams_router
from app.routers.projects import router as projects_router
from app.imports.import_projects import router as import_projects_router
from app.routers.tasks import router as tasks_router
from app.imports.import_tasks import router as import_tasks_router
from app.routers.employees import router as employees_routes
from app.imports.import_employees import router as import_employees_routes

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

# Clients routes
app.include_router(import_clients_router, prefix="/api", tags=["Clients"])
app.include_router(clients_router, prefix="/api", tags=["Clients"])

# Teams routes
app.include_router(import_teams_router, prefix="/api", tags=["Teams"])
app.include_router(teams_router, prefix="/api", tags=["Teams"])

# Projects routes
app.include_router(import_projects_router, prefix="/api", tags=["Projects"])
app.include_router(projects_router, prefix="/api", tags=["Projects"])

# Tasks routes
app.include_router(import_tasks_router, prefix="/api", tags=["Tasks"])
app.include_router(tasks_router, prefix="/api", tags=["Tasks"])

# Tasks routes
app.include_router(import_employees_routes, prefix="/api", tags=["Employees"])
app.include_router(employees_routes, prefix="/api", tags=["Employees"])

@app.get("/")
def read_root():
    return {"message": "FastAPI with PostgreSQL is connected successfully!"}