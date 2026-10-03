from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import requests
import secrets
import string
from db.database import get_db
from db.models import User, Profile
from schemas.auth import UserCreate, Token, UserResponse, GoogleAuthRequest
from core.security import verify_password, get_password_hash, create_access_token, create_refresh_token

router = APIRouter()

@router.post("/google", response_model=Token)
def google_auth(req: GoogleAuthRequest, db: Session = Depends(get_db)):
    headers = {'Authorization': f'Bearer {req.token}'}
    resp = requests.get('https://www.googleapis.com/oauth2/v3/userinfo', headers=headers)
    if not resp.ok:
        raise HTTPException(status_code=400, detail="Invalid Google token")
    
    user_info = resp.json()
    email = user_info.get("email")
    name = user_info.get("name", "Google User")
    
    if not email:
        raise HTTPException(status_code=400, detail="Email not provided by Google")
        
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        random_pwd = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))
        hashed_password = get_password_hash(random_pwd)
        
        user = User(
            email=email,
            name=name,
            hashed_password=hashed_password,
            role=req.role
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        db_profile = Profile(user_id=user.id)
        db.add(db_profile)
        db.commit()
        
    access_token = create_access_token(data={"sub": user.email, "role": user.role})
    refresh_token = create_refresh_token(data={"sub": user.email})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/register", response_model=UserResponse)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user_in.password)
    db_user = User(
        email=user_in.email,
        name=user_in.full_name,
        hashed_password=hashed_password,
        role=user_in.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Create profile
    db_profile = Profile(user_id=db_user.id)
    db.add(db_profile)
    db.commit()
    
    return db_user

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token = create_access_token(data={"sub": user.email, "role": user.role})
    refresh_token = create_refresh_token(data={"sub": user.email})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh")
def refresh():
    pass

@router.post("/logout")
def logout():
    pass

@router.post("/verify-email")
def verify_email():
    pass

@router.post("/resend-verification")
def resend_verification():
    pass

@router.post("/forgot-password")
def forgot_password():
    pass

@router.post("/reset-password")
def reset_password():
    pass
