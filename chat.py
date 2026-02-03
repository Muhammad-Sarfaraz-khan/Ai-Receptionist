"""
Chat router for handling AI conversations
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatMessage, ChatResponse
from app.services.ai_service import ai_service

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """
    Send a message to the AI receptionist and get a response
    
    - **message**: User's message
    - **conversation_id**: Optional conversation ID for context
    - **user_name**: Optional user name
    - **user_email**: Optional user email
    """
    try:
        result = ai_service.chat(
            message=message.message,
            conversation_id=message.conversation_id,
            user_name=message.user_name,
            user_email=message.user_email
        )
        
        return ChatResponse(
            response=result["response"],
            conversation_id=result["conversation_id"],
            suggested_actions=result.get("suggested_actions"),
            requires_followup=result.get("requires_followup", False)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")


@router.delete("/chat/{conversation_id}")
async def clear_conversation(conversation_id: str):
    """Clear a conversation from memory"""
    try:
        ai_service.clear_conversation(conversation_id)
        return {"message": "Conversation cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing conversation: {str(e)}")
