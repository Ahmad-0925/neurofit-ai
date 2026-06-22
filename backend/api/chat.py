from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from core.database import get_db
from core.security import get_current_user
from db.models import User, FitnessProfile, AIChat
from services.chat_service import get_ai_response

router = APIRouter(prefix="/chat", tags=["AI Chat"])

class ChatMessage(BaseModel):
    message: str

@router.post("/")
def chat_with_ai(
    data: ChatMessage,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = db.query(FitnessProfile).filter_by(user_id=current_user.id).first()
    
    user_context = {}
    if profile:
        user_context = {
            "age": profile.age,
            "bmi": profile.bmi,
            "tdee": profile.tdee,
            "goal": profile.goal,
            "activity_level": profile.activity_level
        }

    ai_response = get_ai_response(data.message, user_context)

    chat_record = AIChat(
        user_id=current_user.id,
        message=data.message,
        response=ai_response
    )
    db.add(chat_record)
    db.commit()

    return {"response": ai_response}

@router.get("/history")
def get_chat_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chats = db.query(AIChat).filter_by(user_id=current_user.id).order_by(AIChat.timestamp).all()
    return chats