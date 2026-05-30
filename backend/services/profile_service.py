from sqlalchemy.orm import Session
from db.models import FitnessProfile
from schema.profile_schema import ProfileCreate, ProfileUpdate
from services.calculation import feet_inches_to_cm, calculate_bmi, calculate_tdee, get_calorie_targets

from fastapi import HTTPException

def create_profile(db: Session, user_id: int, data: ProfileCreate):
    height_cm = feet_inches_to_cm(data.height_feet, data.height_inches)
    bmi = calculate_bmi(data.weight, height_cm)
    tdee = calculate_tdee(data.weight, height_cm, data.age, data.gender, data.activity_level)

    profile = FitnessProfile(
        user_id=user_id,
        age=data.age,
        weight=data.weight,
        height=height_cm,
        gender=data.gender,
        goal=data.goal,
        activity_level=data.activity_level,
        bmi=bmi,
        tdee=tdee
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def get_profile(db: Session, user_id: int):
    profile = db.query(FitnessProfile).filter(FitnessProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile
def update_profile(db: Session, user_id: int, data: ProfileUpdate):
    profile = get_profile(db, user_id)
    if not profile:
        return None

    if data.height_feet is not None:
        inches = data.height_inches or 0
        profile.height = feet_inches_to_cm(data.height_feet, inches)

    if data.age is not None:
        profile.age = data.age
    if data.weight is not None:
        profile.weight = data.weight
    if data.gender is not None:
        profile.gender = data.gender
    if data.goal is not None:
        profile.goal = data.goal
    if data.activity_level is not None:
        profile.activity_level = data.activity_level

    profile.bmi = calculate_bmi(profile.weight, profile.height)
    profile.tdee = calculate_tdee(profile.weight, profile.height, profile.age, profile.gender, profile.activity_level)

    db.commit()
    db.refresh(profile)
    return profile

def delete_profile(db: Session, user_id: int):
    profile = get_profile(db, user_id)
    if not profile:
        return None
    db.delete(profile)
    db.commit()
    return True