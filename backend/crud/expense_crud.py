from sqlalchemy.orm import Session
from backend.models.expense import Expense, ExpenseShare
from backend.schemas.expense_schema import ExpenseCreate
from fastapi import HTTPException
from typing import Optional, List


class ExpenseCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create_expense(self, expense_data: ExpenseCreate) -> Expense:
        expense = Expense(
            title=expense_data.title,
            amount=expense_data.amount,
            payer_id=expense_data.payer_id,
            group_id=expense_data.group_id,
            split_type=expense_data.split_type
        )
        self.db.add(expense)
        self.db.flush()  # Get expense.id before adding shares

        for share in expense_data.shares:
            share_entry = ExpenseShare(
                expense_id=expense.id,
                user_id=share.user_id,
                share_amount=share.share_amount,
                included=share.included
            )
            self.db.add(share_entry)

        self.db.commit()
        self.db.refresh(expense)
        return expense

    def get_expense_by_id(self, expense_id: int) -> Optional[Expense]:
        return self.db.query(Expense).filter(Expense.id == expense_id).first()

    def delete_expense(self, expense_id: int) -> bool:
        expense = self.get_expense_by_id(expense_id)
        if not expense:
            return False

        self.db.delete(expense)
        self.db.commit()
        return True
    
