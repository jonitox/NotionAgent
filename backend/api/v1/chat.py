from fastapi import APIRouter, Depends
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from backend.core.deps import get_agent_graph, get_current_user
from backend.db.models import User
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
):
    try:
        state = {
            "messages": [HumanMessage(content=request.message)]
        }
        
        # Namespace thread_id per user to avoid cross-user collisions
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
        
        return ChatResponse(answer=response_text)
        
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {str(e)}")
        traceback.print_exc()
        return ChatResponse(answer=f"ERROR OCCURRED: {str(e)}")

@router.get("/history", response_model=ChatHistoryResponse, tags=["chat"])
def get_history(
    thread_id: str = "default",
    limit: int = 50,
    graph = Depends(get_agent_graph),
    current_user: User = Depends(get_current_user),
):
    """
    Return prior messages for the given thread (namespaced per user).
    """
    try:
        namespaced_thread_id = f"{current_user.id}:{thread_id}"
        config = {"configurable": {"thread_id": namespaced_thread_id}}
        state = graph.get_state(config)
        raw_messages = state.values.get("messages", [])
        # take the last `limit` messages
        raw_messages = raw_messages[-limit:]

        def _serialize(m) -> ChatMessage:
            t = m.__class__.__name__
            c = m.content if hasattr(m, "content") and isinstance(m.content, str) else str(m)
            return ChatMessage(type=t, content=c)

        messages = [_serialize(m) for m in raw_messages]
        return ChatHistoryResponse(messages=messages)
    except Exception as e:
        print(f"ERROR(history): {type(e).__name__}: {str(e)}")
        traceback.print_exc()
        return ChatHistoryResponse(messages=[])
    
