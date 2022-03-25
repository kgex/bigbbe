from sqlalchemy.orm import Session

from . import models, schemas
from .auth import get_password_hash             


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, full_name=user.full_name, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def create_user_entry(db: Session, entry: schemas.Entry, user_id: int):
    db_entry = models.Entry(**entry.dict(), owner_id=user_id)
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

def create_user_report(db: Session, report: schemas.Report, user_id: int):
    db_report = models.Report(**report.dict(), owner_id=user_id)
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

def get_user_report(db: Session, user_id: int):
    return db.query(models.Report).filter(models.Report.owner_id == user_id).all()

def update_user_report(db: Session, report: schemas.Report, user_id: int):
    db_report = models.Report(**report.dict(), owner_id=user_id)
    db.commit()
    db.refresh(db_report)
    return db_report
