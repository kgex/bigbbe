from datetime import datetime
from decimal import Overflow
from typing import List, Optional
from .enums import TaskEnum, GrievanceEnum
from pydantic import BaseModel


class EntryBase(BaseModel):
    time: datetime
    location: str
    entry_type: str


class EntryCreate(EntryBase):
    pass


class Entry(EntryBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class UserBase(BaseModel):
    email: str
    full_name: str


class UserCreate(UserBase):
    password: str
    phone_no: str
    register_num: str
    college: str
    join_year: int
    grad_year: int
    dept: str
    gender: str
    stay: str
    category: str

    class Config:
        orm_mode = True


class UserDelete(BaseModel):
    id: int


class UserVerify(BaseModel):
    email: str
    otp: int


class User(UserBase):
    id: int
    rfid_key: Optional[str]
    is_active: bool
    register_num: str
    join_year: int
    grad_year: int
    college: str
    gender: str
    dept: str
    stay: str
    category: str

    class Config:
        orm_mode = True


class Report(BaseModel):
    task_type: TaskEnum
    title: str
    description: str
    start_time: datetime
    stop_time: datetime
    owner_id: int
    assigned_by: Optional[str]
    priority: Optional[str]
    status: Optional[str]

    class Config:
        orm_mode = True


class ReportDiscord(BaseModel):
    task_type: TaskEnum
    title: str
    description: str
    start_time: datetime
    stop_time: datetime
    assigned_by: Optional[str]
    priority: Optional[str]
    status: Optional[str]

    class Config:
        orm_mode = True


class ResetPasswordBase(BaseModel):
    email: str
    password: str
    new_password: str


class ClientBase(BaseModel):
    name: str
    description: str
    poc_name: str
    poc_phone: str
    poc_email: str

    class Config:
        orm_mode = True


class ClientResponse(ClientBase):
    id: int
    owner_id: int


class ProjectBase(BaseModel):
    name: str
    description: str
    start_time: datetime
    stop_time: datetime
    project_status: str
    domain: str

    class Config:
        orm_mode = True


class ProjectResponse(ProjectBase):
    id: int
    owner_id: int


class GrievanceBase(BaseModel):
    id: int
    owner_id: int
    grievance_type: GrievanceEnum
    name: str
    description: str
    image_url: str

    class Config:
        orm_mode = True


class VerifyToken(BaseModel):
    id: int
    owner_id: int
    token: str
    expires: datetime

    class Config:
        orm_mode = True


class AttendanceIn(BaseModel):
    in_time: datetime
    rfid_key: str

    class Config:
        orm_mode = True


class AttendanceInResponse(BaseModel):
    id: int

    class Config:
        orm_mode = True


class AttendanceEntry(BaseModel):
    id: int
    user_id: int
    in_time: datetime
    out_time: datetime

    class Config:
        orm_mode = True


class AttendanceOut(BaseModel):
    id: int
    out_time: datetime

    class Config:
        orm_mode = True


class UpdateRFID(BaseModel):
    rfid_key: str
    email: str

    class Config:
        orm_mode = True


class AttendanceResponse(BaseModel):
    User: User
    AttendanceEntries: AttendanceEntry

    class Config:
        orm_mode = True


class ForgotPass(BaseModel):
    email: str
    otp: int
    password: str
