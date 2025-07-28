from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.schemas import UserCreate, User
from app.models.models import User as UserModel
from app.utils.utils import hash_password, verify_password,create_jwt_token
from app.utils.utils import decode_token

from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies import get_current_user,get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=User)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(UserModel.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pwd = hash_password(user_data.password)
    new_user = UserModel(
        email=user_data.email,
        username=user_data.username,
        password_hash=hashed_pwd,
        is_active=True,
        is_verified=False,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_jwt_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=User)
def read_me(current_user: UserModel = Depends(get_current_user)):
    return current_user


@router.post("/verify-email/{token}")
def verify_email(token: str, db: Session = Depends(get_db)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = db.query(UserModel).filter(UserModel.email == payload["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_verified = True
    db.commit()
    return {"msg": "Email verified successfully"}

