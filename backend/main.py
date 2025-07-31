# backend/main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from backend.crud.user_crud import UserCRUD
from fastapi.middleware.cors import CORSMiddleware
from backend.utils.auth import get_current_user
from backend.models.user import User as UserModel
from backend.models.database import Base, engine
from backend.models import database
from backend.schemas import user_schema
import backend.models  # This registers all models once



app = FastAPI()



# Auto-create tables at startup (only creates if not exists)
Base.metadata.create_all(bind=engine)

# CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/register/")
def register_user(user: user_schema.UserCreate, db_: Session = Depends(database.get_db)):
    user_crud = UserCRUD(db_)        # 👈 create an instance with the DB session
    return user_crud.create_user(user)  # 👈 call the method from that instance


@app.post("/login/")
def login_user(login_data: user_schema.UserLogin, db: Session = Depends(database.get_db)):
    user_cruds = UserCRUD(db)
    return user_cruds.authenticate_user(login_data)



@app.get("/protected/")
def protected_route(current_user: UserModel = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.name}!"}


@app.get("/users/all/")
def get_all_users(db_: Session = Depends(database.get_db)):
    user_crud_instance = UserCRUD(db_)
    print("Fetching all users")
    return