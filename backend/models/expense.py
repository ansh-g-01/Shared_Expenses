from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime, Enum, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
from .enums import SplitType
import enum


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    payer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
    split_type = Column(Enum(SplitType), default=SplitType.equal)

    # Relationships
    payer = relationship("User", back_populates="expenses_paid")
    shares = relationship("ExpenseShare", back_populates="expense")
    group = relationship("Group", back_populates="expenses")

class ExpenseShare(Base):
    __tablename__ = "expense_shares"

    expense_id = Column(Integer, ForeignKey("expenses.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    share_amount = Column(Float, nullable=False)
    included = Column(Boolean, default=True)

    # Relationships
    expense = relationship("Expense", back_populates="shares")
    user = relationship("User", back_populates="shares")
