from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, responses
from ...auth import get_current_active_user
from sqlalchemy.orm import Session
from . import crud, schemas
from ...database import SessionLocal
from ...models import User
from typing import List
import shutil


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(
    prefix="/inventory",
    tags=["inventory"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[schemas.InventoryOut])
def read_inventory(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_active_user),
):
    if user.role != "admin":
        raise HTTPException(status_code=400, detail="Not authorized")
    inventory = crud.get_inventory(db, skip=skip, limit=limit)
    return inventory


@router.post("/")
def create_inventory(
    # inventory: schemas.InventoryIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_active_user),
    file: UploadFile = File(...),
    inventory: schemas.InventoryIn=Depends()
):
    if user.role != "admin":
        raise HTTPException(status_code=400, detail="Not authorized")
    
    inventory = crud.create_inventory(db=db, inventory=inventory, user_id=user.id,photo=file)

    return {"message": "Inventory created successfully"}


@router.patch("/{inventory_id}", response_model=schemas.InventoryOut)
def update_inventory(
    inventory_id: int,
    inventory: schemas.InventoryUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_active_user),
):
    if user.role != "admin":
        raise HTTPException(status_code=400, detail="Not authorized")
    inventory = crud.update_inventory(
        db=db, inventory_id=inventory_id, inventory=inventory
    )
    return inventory


@router.delete("/{inventory_id}", response_model=schemas.InventoryOut)
def delete_inventory(
    inventory_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_active_user),
):
    if user.role != "admin":
        raise HTTPException(status_code=400, detail="Not authorized")
    inventory = crud.delete_inventory(db=db, inventory_id=inventory_id)
    return inventory


@router.get("/{inventory_id}")
def read_inventory_by_id(
    inventory_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_active_user),
):
    if user.role != "admin":
        raise HTTPException(status_code=400, detail="Not authorized")
    inventory = crud.read_inventory_by_id(db=db, inventory_id=inventory_id)
    return inventory
