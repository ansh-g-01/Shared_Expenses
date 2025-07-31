from pydantic import BaseModel, EmailStr
from typing import List,Optional
from datetime import datetime
from enum import Enum
from sqlalchemy.orm import Session
from backend.models.payment import Payment
from backend.schemas.payment_schema import PaymentCreate

class PaymentCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create_payment(self, payment_data: PaymentCreate) -> Payment:
        payment = Payment(
            payer_id=payment_data.payer_id,
            receiver_id=payment_data.receiver_id,
            amount=payment_data.amount,
            proof_url=payment_data.proof_url
        )
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        return payment

    def get_payment_by_id(self, payment_id: int) -> Optional[Payment]:
        return self.db.query(Payment).filter(Payment.id == payment_id).first()

    def get_all_payments(self) -> List[Payment]:
        return self.db.query(Payment).all()

    def get_payments_by_user(self, user_id: int) -> List[Payment]:
        return self.db.query(Payment).filter(
            (Payment.payer_id == user_id) | (Payment.receiver_id == user_id)
        ).all()

    def delete_payment(self, payment_id: int) -> bool:
        payment = self.get_payment_by_id(payment_id)
        if not payment:
            return False
        self.db.delete(payment)
        self.db.commit()
        return True

