from fastapi import APIRouter

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/")
def chat(message: str):
    return {"response": f"You said: {message}"}