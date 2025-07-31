from pydantic import BaseModel, EmailStr
from typing import List,Optional
from datetime import datetime
from enum import Enum
class UserCreate(BaseModel):
    name: str
    email: str
    phone: int
    password: str 


class UserUpdate(BaseModel):
    name: Optional[str]
    phone: Optional[str]

class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    phone: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True
class UserLogin(BaseModel):
    email: EmailStr
    password: str

