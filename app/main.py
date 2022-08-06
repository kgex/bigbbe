from datetime import datetime, timedelta
from typing import Optional, List

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models, schemas, auth, email
from .database import SessionLocal, engine
from .schemas import User, Token
from .routers import nivu
from .routers.inventory import inventory

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(nivu.router)
# app.include_router()
app.include_router(inventory.router, tags=["inventory"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

origins = [
    "http://kgx.nivu.me",
    "https://kgx.nivu.me",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    valid_domains = ["kgkite.ac.in", "kgcas.com"]
    if user.email.split("@")[1] not in valid_domains:
        raise HTTPException(
            status_code=400, detail="Email must be from kgkite.ac.in or kgkcas.com"
        )
    db_user = crud.create_user(db=db, user=user)
    db_user.otp = auth.generate_otp(6)
    crud.save_user_details(db=db, user=db_user)
    msg = "Your OTP is: <h2>" + str(db_user.otp) + "</h2>"
    email_client = email.Email()
    email_client.send(
        recipient=db_user.email, subject="Verify your email", html_content=msg
    )

    return db_user


@app.post("/verify", response_model=schemas.User)
def verify_user(user: schemas.UserVerify, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if not db_user:
        raise HTTPException(status_code=400, detail="Email not registered")
    if db_user.otp != user.otp:
        raise HTTPException(status_code=400, detail="OTP not valid")
    db_user.otp = None
    db_user.is_active = True
    crud.save_user_details(db=db, user=db_user)
    return db_user


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        # data={"sub": user.email}, expires_delta=access_token_expires
        data={
            "email": user.email,
            "user_id": user.id,
            "full_name": user.full_name,
            "role": user.role,
        },
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.delete("/users/{user_id}")
def delete_user(user: schemas.UserDelete, db: Session = Depends(get_db)):
    return crud.delete_user(user_id=user.id, db=db)


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(auth.get_current_active_user)):
    return current_user


@app.post("/users/{user_id}/report", response_model=schemas.Report)
def create_report_for_user(
    user_id: int, report: schemas.Report, db: Session = Depends(get_db)
):
    return crud.create_user_report(db=db, report=report, user_id=user_id)


@app.get("/users/{user_id}/reports", response_model=List[schemas.Report])
def get_user_reports(user_id: int, db: Session = Depends(get_db)):
    users = crud.get_user_report(db=db, user_id=user_id)
    return users

@app.patch("/users/{user_id}/reports/{report_id}", response_model=schemas.Report)
def update_user_report(
    user_id: int, report_id: int, report: schemas.Report, db: Session = Depends(get_db)
):
    return crud.update_user_report(db=db, report=report, user_id=user_id, report_id=report_id)

@app.post("/resetpass", response_model=schemas.User)
def reset_password(
    user_id: int, new_password: str, old_password: str, db: Session = Depends(get_db)
):
    return crud.change_password(
        db=db, user_id=user_id, new_password=new_password, old_password=old_password
    )


@app.get("/users/{user_id}/reports/{report_id}", response_model=schemas.Report)
def get_user_report(report_id: int, db: Session = Depends(get_db)):
    return crud.get_user_report_by_id(db=db, report_id=report_id)


@app.post("/client", response_model=schemas.ClientResponse)
def create_client(client: schemas.ClientBase, db: Session = Depends(get_db)):
    return crud.create_client(db=db, client=client)


@app.get("/clients", response_model=List[schemas.ClientResponse])
def get_clients(db: Session = Depends(get_db)):
    return crud.get_clients(db=db)


@app.get("/clients/{client_id}", response_model=schemas.ClientResponse)
def get_client(client_id: int, db: Session = Depends(get_db)):
    return crud.get_client_by_id(db=db, client_id=client_id)


@app.delete("/clients/{client_id}", response_model=schemas.ClientResponse)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    return crud.delete_client(db=db, client_id=client_id)


@app.post("/clients/{client_id}/projects", response_model=schemas.ProjectResponse)
def create_project(
    client_id: int, project: schemas.ProjectBase, db: Session = Depends(get_db)
):
    return crud.create_project(db=db, project=project, client_id=client_id)


@app.get("/clients/{client_id}/projects", response_model=List[schemas.ProjectResponse])
def get_projects(client_id: int, db: Session = Depends(get_db)):
    return crud.get_projects(db=db, client_id=client_id)


@app.get(
    "/clients/{client_id}/projects/{project_id}", response_model=schemas.ProjectResponse
)
def get_project(project_id: int, db: Session = Depends(get_db)):
    return crud.get_project_by_id(db=db, project_id=project_id)


@app.delete(
    "/clients/{client_id}/projects/{project_id}", response_model=schemas.ProjectResponse
)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    return crud.delete_project(db=db, project_id=project_id)


@app.post("/users/{user_id}/grievance", response_model=schemas.ProjectResponse)
def create_grievance(
    user_id: int, grievance: schemas.GrievanceBase, db: Session = Depends(get_db)
):
    return crud.create_grievance(db=db, grievance=grievance, user_id=user_id)


@app.get("/users/{user_id}/getreports", response_model=List[schemas.Report])
def get_user_reports(user_id: int, db: Session = Depends(get_db)):
    user_reports = crud.get_user_reports(db=db, user_id=user_id)
    if not user_reports:
        raise HTTPException(
            status_code=status.HTTP_403_UNAUTHORIZED,
            detail="You are not authorized to access this resource",
            headers={"WWW-Authenticate": "Bearer"},
        )
        return user_reports
    return user_reports


@app.get("/projects", response_model=List[schemas.ProjectResponse])
def get_all_projects(db: Session = Depends(get_db)):
    return crud.get_projects(db=db)


@app.post("/forgotpass")
def forgot_password(user_email: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user_email)
    db_user.otp = auth.generate_otp()
    crud.save_user_details(db, db_user)
    msg = "<h2>Your otp is <h1>" + str(db_user.otp) + "</h1></h2>"
    email_client = email.Email()
    try:
        email_client.send(
            recipient=db_user.email, subject="Password Reset OTP", html_content=msg
        )
    except Exception as e:
        return {"status": "failure", "message": str(e)}
    return {"status": "success", "message": "OTP sent to your email"}


@app.post("/enterotp")
def enter_otp(user_email: str, otp: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user_email)
    if db_user.otp == otp:
        db_user.otp = 0
        return {"status": "success", "message": "OTP verified"}
    else:
        return {"status": "failure", "message": "OTP not verified"}


@app.post("/resetpassword")
def reset_password(user_email: str, new_password: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user_email)
    db_user.password = new_password
    crud.save_user_details(db, db_user)
    return {"status": "success", "message": "Password reset successfully"}


# @app.get("/users/{user_id}/getgrievances", response_model=List[schemas.Grievance])
# def get_user_grievances(user_id: int, db: Session = Depends(get_db)):
#     user_grievances = crud.get_user_grievances(db=db, user_id=user_id)
#     if not user_grievances:
#         raise HTTPException(
#             status_code=status.HTTP_403_UNAUTHORIZED,
#             detail="You are not authorized to access this resource",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#         return user_grievances
#     return user_grievances


@app.post("/attendance_in", response_model=schemas.AttendanceInResponse)
def attendance_in(
    attendance_entry: schemas.AttendanceIn, db: Session = Depends(get_db)
):
    db_user = crud.get_user_id_by_rfid_key(db, rfid_key=attendance_entry.rfid_key)
    if not db_user:
        raise HTTPException(status_code=400, detail="User with RFID key not found")
    return crud.attendance_in(db=db, entry=attendance_entry, user_id=db_user.id)


@app.patch("/attendance_out", response_model=schemas.AttendanceInResponse)
def attendance_out(
    attendance_entry: schemas.AttendanceOut, db: Session = Depends(get_db)
):
    return crud.attendance_out(db=db, entry=attendance_entry)


@app.get("/attendance")
def get_attendance(db: Session = Depends(get_db)):
    return crud.get_attendance(db=db)


@app.patch("/updaterfid", response_model=schemas.User)
def update_rfid(details: schemas.UpdateRFID, db: Session = Depends(get_db)):
    return crud.update_user_rfid_key(
        db=db, user_email=details.email, rfid_key=details.rfid_key
    )


<<<<<<< HEAD
@app.get("/get_today_attendance")
def get_today_attendance( user_id: int, db: Session = Depends(get_db)):
    return crud.get_today_attendance(db=db, user_id=user_id)

@app.get("/get_previous_month_attendance", response_model=List[schemas.AttendanceResponse])
def get_previous_month_attendance( user_id: int, db: Session = Depends(get_db)):
=======
@app.get("/get_today_attendace")
def get_today_attendance(user_id: int, db: Session = Depends(get_db)):
    return crud.get_today_attendance(db=db, user_id=user_id)


@app.get("/get_previous_month_attendance")
def get_previous_month_attendance(user_id: int, db: Session = Depends(get_db)):
>>>>>>> 5db2acc43c68319151ad208f179722847d5d6c20
    return crud.get_previous_month_attendance(db=db, user_id=user_id)


@app.patch("/user/{user_id}/{discord_id}")
def update_discord_id(user_id: int, discord_username: str, db: Session = Depends(get_db)):
    return crud.add_user_discord_id(db=db, user_id=user_id, discord_username=discord_username)

@app.get("/user/{user_id}/{discord_id}")
def get_user_report_by_discord_id(discord_username: str, db: Session = Depends(get_db)):
    return crud.get_user_reports_by_discord_id(db=db, discord_username=discord_username)
