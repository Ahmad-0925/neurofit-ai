from pydantic import BaseModel, Field
from typing import Optional

class ProfileCreate(BaseModel):
    age: int = Field(..., ge=10, le=100)
    weight: float = Field(..., ge=30, le=300)
    height_feet: int = Field(..., ge=3, le=8)
    height_inches: int = Field(0, ge=0, le=11)
    gender: str = Field(..., pattern="^(male|female)$")
    goal: str = Field(..., pattern="^(lose_weight|gain_muscle|maintain)$")
    activity_level: str = Field(..., pattern="^(sedentary|light|moderate|active)$")

class ProfileUpdate(BaseModel):
    age: Optional[int] = Field(None, ge=10, le=100)
    weight: Optional[float] = Field(None, ge=30, le=300)
    height_feet: Optional[int] = Field(None, ge=3, le=8)
    height_inches: Optional[int] = Field(None, ge=0, le=11)
    gender: Optional[str] = None
    goal: Optional[str] = None
    activity_level: Optional[str] = None

class ProfileResponse(BaseModel):
    id: int
    user_id: int
    age: int
    weight: float
    height: float
    gender: str
    goal: str
    activity_level: str
    bmi: Optional[float] = None
    tdee: Optional[float] = None

    class Config:
        from_attributes = True