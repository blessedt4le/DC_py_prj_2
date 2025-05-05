from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from app.schemas import UserCreate, UserSchema, Token
from app.auth import get_password_hash, create_access_token, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UserSchema)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Проверка уникальности email
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")
    
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Неверный email или пароль")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users", response_model=List[UserSchema])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users