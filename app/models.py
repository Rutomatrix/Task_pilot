from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey
from app.db.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql import func

# ---------- Clients ----------
class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    Client_ID = Column(String, unique=True, nullable=False)
    Client_Name = Column(String, nullable=False)
    Description = Column(Text)
    Type = Column(String)
    Status = Column(String)
    Active_Projects = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


# ---------- Teams ----------
class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    Team_ID = Column(String, unique=True, nullable=False)
    Category = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


# ---------- Employees ----------
class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    Emp_ID = Column(String, unique=True, nullable=False)
    Team_ID = Column(String)
    Name = Column(String)
    Role = Column(String)
    Skillset = Column(ARRAY(String), default=list)
    Current_Tasks = Column(ARRAY(String), default=list)
    Status = Column(String)
    Comments = Column(Text)
    Email = Column(String, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


# ---------- Projects ----------
class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    Project_ID = Column(String, unique=True, nullable=False)
    Name = Column(String, nullable=False)
    Client_ID = Column(ARRAY(String), default=list)
    Description = Column(Text)
    Priority = Column(String)
    Deadline = Column(DateTime)
    Status = Column(String)
    Linked_Inventory = Column(ARRAY(String), default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


# ---------- Tasks ----------
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    Task_ID = Column(String, unique=True, nullable=False)
    Task_Name = Column(String)
    Project_ID = Column(ARRAY(String), default=list)
    Type = Column(String)
    Assigned_To = Column(ARRAY(String), default=list)
    Priority = Column(String)
    Deadline = Column(DateTime)
    Status = Column(String)
    Dependencies = Column(ARRAY(String), default=list)
    Description = Column(Text)
    Skills_Required = Column(ARRAY(String), default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
