from enum import unique
from pydoc import describe
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from .enums import TaskEnum, GrievanceEnum
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=False)
    rfid_key = Column(String, unique=True)
    otp = Column(Integer, unique=True)
    role = Column(String, default="student")
    items = relationship("Item", back_populates="owner")
    entries = relationship("Entry", back_populates="owner")
    reports = relationship("Report", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    owner = relationship("User", back_populates="items")


class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, index=True)
    time = Column(DateTime, index=True)
    location = Column(String, index=True)
    entry_type = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    owner = relationship("User", back_populates="entries")


class Report(Base):

    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    task_type = Column(Enum(TaskEnum), index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    start_time = Column(DateTime, index=True)
    stop_time = Column(DateTime, index=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    owner = relationship("User", back_populates="reports")


# task type(learnin, project, others)
# title
# description
# starttime
# stop time
# owner_id


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user_id = relationship("User", cascade="all, delete-orphan", single_parent=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    poc_name = Column(String, index=True)
    poc_phone = Column(String, index=True)
    poc_email = Column(String, index=True)


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("clients.id", ondelete="CASCADE"))
    name = Column(String, index=True)
    description = Column(String, index=True)
    start_time = Column(DateTime, index=True)
    stop_time = Column(DateTime, index=True)
    project_status = Column(String, index=True)
    domain = Column(String, index=True)


class Grievance(Base):
    __tablename__ = "grievances"

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    name = Column(String, index=True)
    description = Column(String, index=True)
    image_url = Column(String, index=True)
    grievance_type = Column(Enum(GrievanceEnum), index=True)


class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE") )
    token = Column(String, index=True)
    expires = Column(DateTime, index=True)


class AttendanceEntries(Base):

    __tablename__ = "attendance_entries"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    in_time = Column(DateTime, index=True)
    out_time = Column(DateTime, index=True, nullable=True)
    updated_time = Column(DateTime, index=True)


class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    category = Column(String, index=True)
    qty = Column(Integer, index=True)
    specs = Column(String, index=True)
    department = Column(String, index=True)
    college = Column(String, index=True)
    description = Column(String, index=True)
    purchase_date = Column(DateTime, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE") )

    created_at = Column(DateTime, index=True)
    updated_at = Column(DateTime, index=True)
    item_condition = Column(String, index=True)
    purchase_price = Column(Integer, index=True)
    photo_urls = Column(String, index=True)
    thumbnail_url = Column(String, index=True)
