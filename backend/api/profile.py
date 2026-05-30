from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from schema.profile_schema import ProfileCreate, ProfileUpdate, ProfileResponse
from services.profile_service import create_profile, get_profile, update_profile, delete_profile
from core.security import get_current_user
from db.models import User,FitnessProfile

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.post("/", response_model=ProfileResponse)
def create_user_profile(data: ProfileCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing = db.query(FitnessProfile).filter_by(user_id=current_user.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Profile already exists")
    return create_profile(db, current_user.id, data)

@router.get("/", response_model=ProfileResponse)
def get_user_profile(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_profile(db, current_user.id)

@router.put("/", response_model=ProfileResponse)
def update_user_profile(data: ProfileUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return update_profile(db, current_user.id, data)

@router.delete("/")
def delete_user_profile(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    delete_profile(db, current_user.id)
    return {"message": "Profile deleted successfully"}