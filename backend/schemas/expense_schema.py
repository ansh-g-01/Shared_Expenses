from pydantic import BaseModel, EmailStr
from typing import List,Optional
from datetime import datetime
from enum import Enum
from .enums_schema import SplitType

class ExpenseShareCreate(BaseModel):
    user_id: int
    share_amount: float
    included: Optional[bool] = True

class ExpenseCreate(BaseModel):
    title: str
    amount: float
    payer_id: int
    group_id: Optional[int] = None
    split_type: SplitType
    shares: List[ExpenseShareCreate]

class ExpenseShareOut(BaseModel):
    user_id: int
    share_amount: float
    included: bool

    class Config:
        orm_mode = True

class ExpenseOut(BaseModel):
    id: int
    title: str
    amount: float
    payer_id: int
    group_id: Optional[int]
    split_type: SplitType
    shares: List[ExpenseShareOut]

    class Config:
        orm_mode = True