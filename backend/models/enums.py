from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime, Enum, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
import enum


class SplitType(str, enum.Enum):
    equal = "equal"
    unequal = "unequal"
    percentage = "percentage"
    custom = "custom"
