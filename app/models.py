from enum import unique
from pydoc import describe
from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    Enum,
    Date,
)
from sqlalchemy.orm import relationship
from .enums import TaskEnum, GrievanceEnum, PriorityEnum, StatusEnum
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=False)
    rfid_key = Column(String, unique=True)
    otp = Column(Integer)
    role = Column(String, default="student")
    gender = Column(String)
    stay = Column(String)
    register_num = Column(String, unique=True)
    discord_username = Column(String, unique=True)
    phone_no = Column(String, unique=True)
    college = Column(String)
    dept = Column(String)
    join_year = Column(Integer)
    grad_year = Column(Integer)
    otp_last_gen = Column(DateTime)
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
    assigned_by = Column(String, unique=True, index=True)
    priority = Column(String, index=True)
    status = Column(String, index=True)
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
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
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

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    name = Column(String)
    category = Column(String)
    qty = Column(Integer)
    specs = Column(String)
    department = Column(String)
    college = Column(String)
    description = Column(String)
    purchase_date = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    item_condition = Column(String)
    purchase_price = Column(Integer)
    photo_urls = Column(String, nullable=True)
    thumbnail_url = Column(String,  nullable=True)


class QR_Attendance(Base):
    __tablename__ = "qr_attendance"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    in_time = Column(DateTime)
    out_time = Column(DateTime, nullable=True)
