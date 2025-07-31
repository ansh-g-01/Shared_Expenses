from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime, Enum, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
import enum


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    payer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    proof_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    payer = relationship("User", back_populates="payments_sent", foreign_keys=[payer_id])
    receiver = relationship("User", back_populates="payments_received", foreign_keys=[receiver_id])
