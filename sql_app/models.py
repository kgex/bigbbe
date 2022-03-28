from pydoc import describe
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from .enums import TaskEnum
from .database import Base



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    
    items = relationship("Item", back_populates="owner")
    entries = relationship("Entry", back_populates="owner")
    reports = relationship("Report", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")

class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, index=True)
    time = Column(DateTime, index=True)
    location = Column(String, index=True)
    entry_type = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="entries")


class Report(Base):

    __tablename__ = 'reports'
    
    id = Column(Integer, primary_key=True, index=True)
    task_type = Column(Enum(TaskEnum), index=True)
    title = Column(String, index=True)
    description = Column(String, index = True)
    start_time = Column(DateTime, index = True)
    stop_time = Column(DateTime, index=True)
    owner_id =  Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="reports")

# task type(learnin, project, others)
# title
# description
# starttime
# stop time
# owner_id

class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String, index=True)
    description = Column(String, index=True)
    poc_name = Column(String, index=True)
    poc_phone = Column(String, index=True)
    poc_email = Column(String, index=True)

class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('clients.id'))
    name = Column(String, index=True)
    description = Column(String, index=True)
    start_time = Column(DateTime, index=True)
    stop_time = Column(DateTime, index=True)
    project_status = Column(String, index=True)