from fastapi import APIRouter, Depends
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from backend.core.deps import get_agent_graph, get_current_user, get_db
from backend.db.models import User, UserSettings, Message
from sqlalchemy.orm import Session
import traceback

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str
    thread_id: str = "default"

class ChatResponse(BaseModel):
    answer: str

class ChatMessage(BaseModel):
    """Serialized chat message for history responses"""
    type: str
    content: str

class ChatHistoryResponse(BaseModel):
    messages: list[ChatMessage]

@router.post("/", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    graph = Depends(get_agent_graph),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        settings = db.query(UserSettings).filter(UserSettings.user_id == current_user.id).first()
        
        state = {
            "messages": [HumanMessage(content=request.message)],
            "openai_api_key": settings.openai_api_key if settings else None,
            "notion_api_key": settings.notion_api_key if settings else None,
            "notion_page_id": settings.notion_page_id if settings else None,
        }
        
        namespaced_thread_id = f"{current_user.id}:{request.thread_id}"
        config = {"configurable": {"thread_id": namespaced_thread_id}}
        result = graph.invoke(state, config)
        print("STATE AFTER:", [
            (type(m).__name__, (m.content[:80] if hasattr(m, 'content') and isinstance(m.content, str) else m.content))
            for m in graph.get_state(config).values.get("messages", [])
        ])
        
        # Extract the last AI message
        last_message = result["messages"][-1]
        response_text = last_message.content if hasattr(last_message, 'content') else str(last_message)
        
        # Save messages to database
        db.add(Message(
            user_id=current_user.id,
            thread_id=request.thread_id,
            role="user",
            content=request.message
        ))
        db.add(Message(
            user_id=current_user.id,
            thread_id=request.thread_id,
            role="assistant",
            content=response_text
        ))
        db.commit()
        
        return ChatResponse(answer=response_text)
        
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {str(e)}")
        traceback.print_exc()
        return ChatResponse(answer=f"ERROR OCCURRED: {str(e)}")

@router.get("/history", response_model=ChatHistoryResponse, tags=["chat"])
def get_history(
    thread_id: str = "default",
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Return chat history for the given thread from database.
    """
    try:
        # Query messages from database
        db_messages = db.query(Message).filter(
            Message.user_id == current_user.id,
            Message.thread_id == thread_id
        ).order_by(Message.created_at).limit(limit).all()
        
        messages = [
            ChatMessage(type=msg.role, content=msg.content)
            for msg in db_messages
        ]
        return ChatHistoryResponse(messages=messages)
    except Exception as e:
        print(f"ERROR(history): {type(e).__name__}: {str(e)}")
        traceback.print_exc()
        return ChatHistoryResponse(messages=[])
    
