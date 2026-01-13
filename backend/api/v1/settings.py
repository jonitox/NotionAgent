from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from backend.core.deps import get_db, get_current_user
from backend.db.models import User, UserSettings

router = APIRouter(prefix="/settings", tags=["settings"])


class UserSettingsRequest(BaseModel):
    openai_api_key: str | None = None
    notion_api_key: str | None = None
    notion_page_id: str | None = None


class UserSettingsResponse(BaseModel):
    id: int
    user_id: int
    openai_api_key: str | None = None
    notion_api_key: str | None = None
    notion_page_id: str | None = None

    class Config:
        from_attributes = True


@router.post("/", response_model=UserSettingsResponse, status_code=status.HTTP_200_OK)
def upsert_settings(
    request: UserSettingsRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Upsert user settings (create if not exists, update if exists)
    """
    settings = db.query(UserSettings).filter(UserSettings.user_id == current_user.id).first()
    
    if not settings:
        settings = UserSettings(user_id=current_user.id)
    
    settings.openai_api_key = request.openai_api_key
    settings.notion_api_key = request.notion_api_key
    settings.notion_page_id = request.notion_page_id
    
    db.add(settings)
    db.commit()
    db.refresh(settings)
    return settings


@router.get("/", response_model=UserSettingsResponse, status_code=status.HTTP_200_OK)
def get_settings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get user settings
    """
    settings = db.query(UserSettings).filter(UserSettings.user_id == current_user.id).first()
    
    if not settings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Settings not found",
        )
    
    return settings
