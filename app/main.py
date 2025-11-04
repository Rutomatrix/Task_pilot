from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app import models
from app.db.database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "FastAPI with PostgreSQL is connected successfully!"}
