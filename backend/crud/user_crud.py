# crud_user.py
from sqlalchemy.orm import Session
from backend.models.user import User
from backend.schemas.user_schema import UserCreate, UserUpdate, UserLogin
from backend.utils.auth import create_access_token
from backend.utils.security import verify_password,hash_password
from fastapi import HTTPException


class UserCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_data: UserCreate) -> User:
        existing = self.db.query(User).filter(User.email == user_data.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_pw = hash_password(user_data.password)

        db_user = User(
            name=user_data.name,
            email=user_data.email,
            phone=user_data.phone,
            password_hash=hashed_pw
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    def authenticate_user(self, login_data: UserLogin):
        user = self.db.query(User).filter(User.email == login_data.email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if not verify_password(login_data.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Incorrect password")
        else:
            access_token = create_access_token(data={"sub": user.email})
            return {"access_token": access_token, "token_type": "bearer"}


    def get_user_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_all_users(self) -> list[User]:
        return self.db.query(User).all()

    def update_user(self, user_id: int, updates: UserUpdate) -> User | None:
        user = self.get_user_by_id(user_id)
        if not user:
            return None

        for key, value in updates.dict(exclude_unset=True).items():
            setattr(user, key, value)

        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user_id: int) -> bool:
        user = self.get_user_by_id(user_id)
        if not user:
            return False

        self.db.delete(user)
        self.db.commit()
        return True