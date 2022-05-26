from sqlalchemy.orm import Session
import datetime
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
    db_user = models.User(
        email=user.email, full_name=user.full_name, hashed_password=hashed_password
    )
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


def get_user_report_by_id(db: Session, report_id: int):
    return db.query(models.Report).filter(models.Report.id == report_id).first()


def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user


def change_password(db: Session, user_id: int, new_password: str, old_password: str):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user.hashed_password == get_password_hash(old_password):
        db_user.hashed_password = get_password_hash(new_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    return db_user


def save_user_details(db: Session, user: models.User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def verify_email(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db_user.is_active = True
    db.commit()
    return db_user


def create_client(db: Session, client: schemas.ClientBase, user_id: int):
    db_client = models.Client(**client.dict(), owner_id=user_id)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


def get_client_by_id(db: Session, client_id: int):
    return db.query(models.Client).filter(models.Client.id == client_id).first()


def get_clients(db: Session):
    return db.query(models.Client).all()


def delete_client(db: Session, client_id: int):
    db_client = db.query(models.Client).filter(models.Client.id == client_id).first()
    db.delete(db_client)
    db.commit()
    return db_client


def create_project(db: Session, project: schemas.ProjectBase, client_id: int):
    db_project = models.Project(**project.dict(), owner_id=client_id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def get_projects(db: Session, client_id: int):
    return db.query(models.Project).filter(models.Project.owner_id == client_id).all()


def get_project_by_id(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id).first()


def delete_project(db: Session, project_id: int):
    db_project = (
        db.query(models.Project).filter(models.Project.id == project_id).first()
    )
    db.delete(db_project)
    db.commit()
    return db_project


def create_grievance(db: Session, user_id: int, grievance: schemas.GrievanceBase):
    db_grievance = models.Grievance(owner_id=user_id)
    db.add(db_grievance)
    db.commit()
    db.refresh(db_grievance)
    return db_grievance


def get_user_reports(db: Session):
    return db.query(models.Report).all()


def get_user_reports_by_date(db: Session, user_id: int, date: str):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user.role == "admin":
        return False
    return (
        db.query(models.Report)
        .filter(models.Report.owner_id == user_id, models.Report.start_date == date)
        .all()
    )


def create_verify_token(db: Session, token: schemas.VerifyToken):
    db_token = models.VerifyToken(**token.dict())
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token


def verify_email_by_id(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db_user.is_active = True
    db_user.otp = None
    db.commit()
    return db_user


def get_user_id_by_rfid_key(db: Session, rfid_key: str):
    return db.query(models.User).filter(models.User.rfid_key == rfid_key).first().id


def attendance_in(db: Session, entry: schemas.AttendanceEntryCreate):
    db_entry = models.AttendanceEntries(
        rfid_key=entry.rfid_key,
        in_time=entry.in_time,
        updated_time=datetime.datetime.now(),
    )
    db_entry.user_id = 2
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry


def get_attendance(db: Session):
    return db.query(models.AttendanceEntries).all()


def attendance_out(db: Session, entry: schemas.AttendanceOut):
    db_entry = (
        db.query(models.AttendanceEntries)
        .filter(models.AttendanceEntries.id == entry.id)
        .first()
    )
    db_entry.out_time = entry.out_time
    db_entry.updated_time = datetime.datetime.now()
    db.commit()
    db.refresh(db_entry)
    return db_entry


def update_user_rfid_key(db: Session, user_email: str, rfid_key: str):
    db_user = db.query(models.User).filter(models.User.email == user_email).first()
    db_user.rfid_key = rfid_key
    db.commit()
    return db_user
