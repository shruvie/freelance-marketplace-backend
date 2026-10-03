from fastapi import APIRouter, Depends
from schemas.auth import UserResponse
from api.deps import get_current_active_user
from db.models import User

router = APIRouter()

@router.get("/me", response_model=UserResponse)
def get_current_user(current_user: User = Depends(get_current_active_user)):
    return current_user
