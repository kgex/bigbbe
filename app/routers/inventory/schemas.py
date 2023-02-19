from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


class InventoryIn(BaseModel):
    name: str
    category: str
    qty: int
    specs: str
    department: str
    college: str
    description: str
    purchase_date: datetime
    created_at: datetime
    item_condition: str
    purchase_price: float

    # class Config:
    #     orm_mode = True
    #     fields = {

    #         "name": "name",
    #         "category": "category",
    #         "qty": "qty",
    #         "specs": "specs",
    #         "department": "department",
    #         "college": "college",
    #         "description": "description",
    #         "purchase_date": "purchase_date",
    #         "created_at": "created_at",
    #         "item_condition": "item_condition",
    #         "purchase_price": "purchase_price",
    #     }


class InventoryOut(InventoryIn):
    id: int

    class Config:
        orm_mode = True


class InventoryUpdate(BaseModel):
    category: Optional[str]
    qty: Optional[int]
    specs: Optional[str]
    department: Optional[str]
    college: Optional[str]
    desc: Optional[str]
    purchase_date: Optional[datetime]
    user_id: Optional[int]
    created_at: Optional[datetime]
    item_condition: Optional[str]
    purchase_price: Optional[float]
    photo_urls: Optional[str]
    thumbnail_url: Optional[str]
    category: Optional[str]

    class Config:
        orm_mode = True
