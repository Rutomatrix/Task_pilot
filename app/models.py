from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey
from app.db.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql

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


# ---------- Teams ----------
class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    Team_ID = Column(String, unique=True, nullable=False)
    Category = Column(String, nullable=False)


# ---------- Users ----------
# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     Emp_ID = Column(String, unique=True, nullable=False)
#     Team_ID = Column(String)
#     Name = Column(String)
#     Role = Column(String)
#     Skillset = Column(String)
#     Current_Tasks = Column(Integer, default=0)
#     Status = Column(String)
#     Comments = Column(Text)


# ---------- Projects ----------
class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    Project_ID = Column(String, unique=True, nullable=False)
    Name = Column(String, nullable=False)
    Client_ID = Column(postgresql.ARRAY(String))
    Description = Column(Text)
    Priority = Column(String)
    Deadline = Column(DateTime)
    Status = Column(String)
    Linked_Inventory = Column(postgresql.ARRAY(String))


# ---------- Tasks ----------
# class Task(Base):
#     __tablename__ = "tasks"

#     id = Column(Integer, primary_key=True, index=True)
#     Task_ID = Column(String, unique=True, nullable=False)
#     Task_Name = Column(String)
#     Project_ID = Column(String)
#     Type = Column(String)
#     Assigned_To = Column(String)
#     Priority = Column(String)
#     Deadline = Column(DateTime)
#     Status = Column(String)
#     Dependencies = Column(String)
#     Description = Column(Text)
