from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.v1 import health, chat, auth, settings
from backend.db.database import engine, Base

# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title = "Notion Agent")

# CORS
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
app.include_router(auth.router, prefix=prefix_v1)
app.include_router(settings.router, prefix=prefix_v1)