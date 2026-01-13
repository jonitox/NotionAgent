from functools import lru_cache
from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from jose import JWTError
from agent.graph.build import build_graph
from backend.db.database import SessionLocal
from backend.db.models import User
from backend.core.security import decode

@lru_cache()
def get_agent_graph():
    """Create and cache the agent graph instance for DI."""
    return build_graph()

def get_db():
    """Create and return a database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
) -> User:
    """Get the currently authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unable to verify credentials",
    )
    
    try:
        from backend.core.settings import settings

        access_token = request.cookies.get(settings.ACCESS_TOKEN_COOKIE_NAME)
        if not access_token:
            raise credentials_exception
        payload = decode(access_token)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user