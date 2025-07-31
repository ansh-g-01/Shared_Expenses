from pydantic import BaseModel, EmailStr
from typing import List,Optional
from datetime import datetime
from enum import Enum


# -------- GROUP --------





class PaymentCreate(BaseModel):
    payer_id: int
    receiver_id: int
    amount: float
    proof_url: Optional[str] = None

class PaymentOut(BaseModel):
    id: int
    payer_id: int
    receiver_id: int
    amount: float
    proof_url: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True
