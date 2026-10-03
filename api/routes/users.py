from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
import cloudinary
import cloudinary.uploader
from core.config import settings

from schemas.auth import UserResponse
from api.deps import get_current_active_user
from db.database import get_db
from db.models import User, Profile

router = APIRouter()

# Configure Cloudinary
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)

@router.get("/me", response_model=UserResponse)
def get_current_user(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.put("/profile")
async def update_profile(
    bio: str = Form(None),
    location: str = Form(None),
    hourly_rate: float = Form(None),
    experience_years: int = Form(None),
    profile_picture: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Upload image to Cloudinary if provided
    image_url = None
    if profile_picture:
        try:
            result = cloudinary.uploader.upload(profile_picture.file)
            image_url = result.get("secure_url")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Image upload failed: {str(e)}")

    # Update or create profile
    profile = current_user.profile
    if not profile:
        profile = Profile(user_id=current_user.id)
        db.add(profile)
    
    if bio: profile.bio = bio
    if location: profile.location = location
    if hourly_rate: profile.hourly_rate = hourly_rate
    if experience_years: profile.experience_years = experience_years
    if image_url: profile.profile_image = image_url

    db.commit()
    db.refresh(profile)
    return {"message": "Profile updated successfully", "profile_image": image_url}
