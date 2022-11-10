from fastapi import APIRouter, Depends, HTTPException
from ...auth import get_current_active_user
from sqlalchemy.orm import Session
from . import crud, schemas
from ...database import SessionLocal
from ...models import User
from typing import List


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(
    prefix="/qr_attendance",
    tags=["qr_attendance"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.post("/",)
def post_attendance(attendance: schemas.QR_Attendance, db: Session = Depends(get_db),user: User = Depends(get_current_active_user)):
    if attendance.type == "in":
        return crud.attendance_in(attendance=attendance, user_id=user.id, db=db)
    return crud.attendance_out(db=db, attendance=attendance, user_id=user.id)


@router.get("/")
def get_all_attendance(db:Session = Depends(get_db)):
    return crud.get_all_attendance(db=db)

@router.get("/user")
def get_attendance_by_user_id(db:Session = Depends(get_db), user: User = Depends(get_current_active_user)):
    return crud.get_attendance_by_id(db=db, user_id = user.id)
