from pydantic import BaseModel, EmailStr
from typing import List,Optional
from datetime import datetime
from enum import Enum


class GroupBase(BaseModel):
    name: str

class GroupCreate(GroupBase):
    pass

class GroupUpdate(BaseModel):
    name: str | None = None

class GroupOut(GroupBase):
    id: int
    created_at: datetime
    members: list[int] = []  # List of user_ids

    class Config:
        orm_mode = True

# -------- GROUP MEMBER --------
class GroupMemberBase(BaseModel):
    group_id: int
    user_id: int

class GroupMemberCreate(GroupMemberBase):
    pass

class GroupMemberOut(GroupMemberBase):
    joined_at: datetime
    class Config:
        orm_mode = True


