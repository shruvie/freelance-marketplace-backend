from fastapi import APIRouter, Depends
from pydantic import BaseModel
from api.deps import get_current_active_user
from db.models import User
from services.ai_service import ai_service

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("/chat", response_model=ChatResponse)
def chat_with_ai(request: ChatRequest, current_user: User = Depends(get_current_active_user)):
    # Basic context placeholder - in a full implementation we'd query pgvector or the DB
    context_data = "Platform active projects: 5. Registered freelancers: 10."
    
    reply = ai_service.generate_response(
        prompt=request.message,
        user_role=current_user.role,
        context_data=context_data
    )
    
    return {"response": reply}
