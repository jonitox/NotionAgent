from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1 import health, chat

app = FastAPI(title = "Notion Agent")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

prefix_v1 = "/api/v1"

app.include_router(health.router, prefix=prefix_v1)
app.include_router(chat.router, prefix=prefix_v1)