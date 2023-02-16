from sqlalchemy.orm import Session
import datetime
from . import schemas
from ... import models
from ...auth import get_password_hash
from fastapi import File, UploadFile
import shutil

def get_inventory(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Inventory).offset(skip).limit(limit).all()


def create_inventory(db: Session, inventory: schemas.InventoryIn, user_id: int,photo:UploadFile):
    db_inventory = models.Inventory(
        **inventory.dict(), updated_at=datetime.datetime.now(), user_id=user_id
    )
    photo_url = f"./media/{photo.filename}"
    db_inventory.photo_urls = photo_url
    db_inventory.thumbnail_url = photo_url
    with open(photo_url, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory


def update_inventory(
    db: Session, inventory: schemas.InventoryUpdate, inventory_id: int
):
    db_inventory = (
        db.query(models.Inventory).filter(models.Inventory.id == inventory_id).first()
    )
    db_inventory.category = (
        inventory.category if inventory.category is not None else db_inventory.category
    )
    db_inventory.qty = inventory.qty if inventory.qty is not None else db_inventory.qty
    db_inventory.specs = (
        inventory.specs if inventory.specs is not None else db_inventory.specs
    )
    db_inventory.department = (
        inventory.department
        if inventory.department is not None
        else db_inventory.department
    )
    db_inventory.college = (
        inventory.college if inventory.college is not None else db_inventory.college
    )
    db_inventory.desc = (
        inventory.desc if inventory.desc is not None else db_inventory.desc
    )
    db_inventory.purchase_date = (
        inventory.purchase_date
        if inventory.purchase_date is not None
        else db_inventory.purchase_date
    )
    db_inventory.item_condition = (
        inventory.item_condition
        if inventory.item_condition is not None
        else db_inventory.item_condition
    )
    db_inventory.updated_at = datetime.datetime.now()
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory


def delete_inventory(db: Session, inventory_id: int):
    db_inventory = (
        db.query(models.Inventory).filter(models.Inventory.id == inventory_id).first()
    )
    db.delete(db_inventory)
    db.commit()
    return db_inventory


def read_inventory_by_id(db: Session, inventory_id: int):
    db_inventory = db.query(models.Inventory).filter(models.Inventory.id == inventory_id).first()
    photo = open(db_inventory.photo_urls, "rb") 
    return {"inventory": db_inventory, "photo": photo}
