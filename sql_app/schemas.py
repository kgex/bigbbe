from datetime import datetime
from decimal import Overflow
from typing import List, Optional

from pydantic import BaseModel

class EntryBase(BaseModel):
    time: datetime
    location: str
    entry_type: str

class EntryCreate(EntryBase):
    pass

class Entry(EntryBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserBase(BaseModel):
    email: str
    full_name: str
    is_active: Optional[bool] = None

class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True