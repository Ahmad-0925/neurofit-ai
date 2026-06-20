from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_user
from db.models import User, FitnessProfile, MLPrediction
from services.ml_service import predict_fitness_score
import json

router = APIRouter(prefix="/predict", tags=["ML Prediction"])

@router.post("/")
def get_prediction(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = db.query(FitnessProfile).filter_by(user_id=current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found! Create profile first.")

    score = predict_fitness_score(
        age=profile.age,
        weight=profile.weight,
        height=profile.height,
        bmi=profile.bmi,
        tdee=profile.tdee,
        activity_level=profile.activity_level
    )

    input_data = {
        "age": profile.age,
        "weight": profile.weight,
        "height": profile.height,
        "bmi": profile.bmi,
        "tdee": profile.tdee,
        "activity_level": profile.activity_level
    }

    prediction_record = MLPrediction(
        user_id=current_user.id,
        model_name="fitness_score_v1",
        input_data=json.dumps(input_data),
        output_data=json.dumps({"fitness_score": score})
    )
    db.add(prediction_record)
    db.commit()

    return {
        "fitness_score": score,
        "message": get_score_message(score)
    }

def get_score_message(score: float) -> str:
    if score >= 80:
        return "Excellent fitness level! Keep it up! 💪"
    elif score >= 60:
        return "Good fitness level! Room for improvement."
    elif score >= 40:
        return "Average fitness level. Let's work on it!"
    else:
        return "Needs improvement. Start your fitness journey today!"