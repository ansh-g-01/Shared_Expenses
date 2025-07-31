from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime, Enum, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
import enum

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    password_hash = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    expenses_paid = relationship("Expense", back_populates="payer")
    shares = relationship("ExpenseShare", back_populates="user")
    groups = relationship("Group", secondary="group_members", back_populates="members")
    payments_sent = relationship("Payment", back_populates="payer", foreign_keys="Payment.payer_id")
    payments_received = relationship("Payment", back_populates="receiver", foreign_keys="Payment.receiver_id")
