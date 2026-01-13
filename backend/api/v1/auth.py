from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from pydantic import BaseModel, EmailStr, Field
from backend.core.deps import get_db, get_current_user
from backend.db.models import User
from backend.core.security import (
    get_password_hash,
    authenticate_user,
    create_access_token
)
from backend.core.settings import settings

router = APIRouter(prefix="/auth", tags=["auth"])

class RegisterRequest(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=72)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class AuthResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    created_at: datetime
    
    class Config:
        from_attributes = True

@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """
    Register a new user
    """
    # check for existing email
    db_user = db.query(User).filter(User.email == request.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered"
        )
    
    # check for existing username
    db_user = db.query(User).filter(User.username == request.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is already taken"
        )
    
    # create new user
    hashed_password = get_password_hash(request.password)
    new_user = User(
        email=request.email,
        username=request.username,
        hashed_password=hashed_password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.post("/login", status_code=status.HTTP_200_OK)
def login(request: LoginRequest, response: Response, db: Session = Depends(get_db)):
    """
    User login
    """
    user = authenticate_user(db, request.email, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    

    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    response.set_cookie(
        key=settings.ACCESS_TOKEN_COOKIE_NAME,
        value=access_token,
        httponly=True,
        path="/",
    )
    response.status_code = status.HTTP_200_OK
    return response

@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(response: Response):
    """
    User logout
    """
    response.delete_cookie(key=settings.ACCESS_TOKEN_COOKIE_NAME, path="/")
    response.status_code = status.HTTP_200_OK
    return response


@router.get("/me", response_model=AuthResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """
    Get the currently logged-in user's information
    """
    return current_user
