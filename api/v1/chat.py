from fastapi import APIRouter, Depends
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from api.deps import get_agent_graph

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str

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
        
        result = graph.invoke(state)
        
        # 마지막 AI 메시지 추출
        last_message = result["messages"][-1]
        response_text = last_message.content if hasattr(last_message, 'content') else str(last_message)
        
        return ChatResponse(answer=response_text)
        
    except Exception as e:
        return ChatResponse(answer=f"ERROR OCCURRED: {str(e)}")