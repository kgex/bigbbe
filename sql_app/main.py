from datetime import datetime, timedelta
from typing import Optional, List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models, schemas, auth
from .database import SessionLocal, engine
from .schemas import User, Token


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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
    allow_origins=origins,
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
    return crud.create_user(db=db, user=user)


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
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
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
        data={"email": user.email, "user_id": user.id, "full_name": user.full_name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(auth.get_current_active_user)):
    return current_user


@app.post("/users/{user_id}/entry/", response_model=schemas.Entry)
def create_entry_for_user(
    user_id: int, entry: schemas.EntryCreate, db: Session = Depends(get_db)
):
    return crud.create_user_entry(db=db, entry=entry, user_id=user_id)


@app.post("/users/{user_id}/entry2/", response_model=schemas.Entry)
def create_entry2_for_user(user_id: int, entry: schemas.EntryCreate, db: Session = Depends(get_db)):
    return crud.create_user_entry(db=db, entry=entry, user_id=user_id)


@app.post("/users/{user_id}/report", response_model=schemas.Report)
def create_report_for_user(user_id: int, report: schemas.Report, db: Session = Depends(get_db)):
    return crud.create_user_report(db=db, report=report, user_id=user_id)

@app.get("/users/{user_id}/reports", response_model=List[schemas.Report])
def get_user_reports(user_id:int, db: Session = Depends(get_db)):
    users = crud.get_user_report(db=db, user_id=user_id)
    return users

@app.post("/resetpass", response_model=schemas.User)
def reset_password(user_id: int, new_password: str, old_password: str, db: Session = Depends(get_db)):
    return crud.change_password(db=db, user_id=user_id, new_password=new_password, old_password=old_password)

@app.get("/users/{user_id}/reports/{report_id}", response_model=schemas.Report)
def get_user_report(report_id: int, db: Session = Depends(get_db)):
    return crud.get_user_report_by_id(db=db, report_id=report_id)

@app.post("/client", response_model=schemas.ClientResponse)
def create_client(user_id: int, client: schemas.ClientBase, db: Session = Depends(get_db)):
    return crud.create_client(db=db, client=client, user_id=user_id)

@app.get("/clients", response_model=List[schemas.ClientResponse])
def get_clients(db: Session = Depends(get_db)):
    return crud.get_clients(db=db)

@app.get("/clients/{client_id}", response_model=schemas.ClientResponse)
def get_client(client_id: int, db: Session = Depends(get_db)):
    return crud.get_client_by_id(db=db, client_id=client_id)

@app.delete("/clients/{client_id}", response_model=schemas.ClientResponse)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    return crud.delete_client(db=db, client_id=client_id)

@app.post("/clients/{client_id}/project", response_model=schemas.ProjectResponse)
def create_project(client_id: int, project: schemas.ProjectBase, db: Session = Depends(get_db)):
    return crud.create_project(db=db, project=project, client_id=client_id)

@app.get("/clients/{client_id}/projects", response_model=List[schemas.ProjectResponse])
def get_projects(client_id: int, db: Session = Depends(get_db)):
    return crud.get_projects(db=db, client_id=client_id)

@app.get("/clients/{client_id}/projects/{project_id}", response_model=schemas.ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    return crud.get_project_by_id(db=db, project_id=project_id)

@app.delete("/clients/{client_id}/projects/{project_id}", response_model=schemas.ProjectResponse)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    return crud.delete_project(db=db, project_id=project_id)

