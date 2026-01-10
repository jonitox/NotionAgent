from fastapi import APIRouter, Depends
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from api.deps import get_agent_graph
import traceback

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str
    thread_id: str = "default"

class ChatResponse(BaseModel):
    answer: str

@router.post("/", response_model=ChatResponse)
def chat(
    req: ChatRequest,
    graph = Depends(get_agent_graph) 
):
    try:
        state = {
            "messages": [HumanMessage(content=req.message)]
        }
        
        config = {"configurable": {"thread_id": req.thread_id}}
        result = graph.invoke(state, config)
        print("STATE AFTER:", [
            (type(m).__name__, (m.content[:80] if hasattr(m, 'content') and isinstance(m.content, str) else m.content))
            for m in graph.get_state(config).values.get("messages", [])
        ])
        
        # 마지막 AI 메시지 추출
        last_message = result["messages"][-1]
        response_text = last_message.content if hasattr(last_message, 'content') else str(last_message)
        
        return ChatResponse(answer=response_text)
        
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {str(e)}")
        traceback.print_exc()
        return ChatResponse(answer=f"ERROR OCCURRED: {str(e)}")