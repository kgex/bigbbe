from sqlalchemy.orm import Session
import datetime
from . import schemas
from ... import models
from ...auth import get_password_hash


def attendance_in(db: Session, attendance: schemas.QR_Attendance, user_id: int):
    db_attendance = models.QR_Attendance(user_id=user_id, in_time=attendance.in_time)
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return {"msg":"Student has been successfully clocked in"}

def attendance_out(db: Session, attendance: schemas.QR_Attendance, user_id: int):
    db_attendance = db.query(models.QR_Attendance).filter(models.QR_Attendance.user_id==user_id).first()
    db_attendance.out_time = attendance.out_time
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return {"msg":"Student has been successfully clocked out"}

def get_all_attendance(db: Session):
    return db.query(models.QR_Attendance).all() 

def get_attendance_by_id(db:Session, user_id:int):
    return db.query(models.QR_Attendance).filter(models.QR_Attendance.user_id==user_id).all()

def delete_all_attendance_entries(db: Session):
    db.query(models.QR_Attendance).delete()
    db.commit()
    return {"msg":"All attendance entries have been deleted"}