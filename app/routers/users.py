from fastapi import APIRouter, Depends, HTTPException
from ..auth import get_current_active_user
from sqlalchemy.orm import Session

from . import crud, models, schemas, auth, email
from .database import SessionLocal, engine
from .schemas import User, Token


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(
    prefix="/users",
    tags=["uses"],
    dependencies=[Depends(get_current_active_user)],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=schemas.User, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = crud.create_user(db=db, user=user)
    db_user.otp = auth.generate_otp(4)
    crud.save_user_details(db=db, user=db_user)
    msg = "Your OTP is: <h2>" + str(db_user.otp) + "</h2>"
    email_client = email.Email()
    email_client.send(
        recipient=db_user.email, subject="Verify your email", html_content=msg
    )

    return db_user


@router.get("/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/me", response_model=schemas.User)
async def read_users_me(current_user: User = Depends(auth.get_current_active_user)):
    return current_user


@router.post("/{user_id}/items/", response_model=List[schemas.Item])
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@router.post("/{user_id}/reports/", response_model=schemas.Report)
def create_report_for_user(
    user_id: int, report: schemas.Report, db: Session = Depends(get_db)
):
    return crud.create_user_report(db=db, report=report, user_id=user_id)


@router.get("/{user_id}/reports/", response_model=List[schemas.Report])
def read_reports_for_user(
    current_user: User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=400, detail="Not authorized")
    return crud.get_user_reports(db=db)
