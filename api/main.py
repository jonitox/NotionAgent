from fastapi import FastAPI
from api.v1 import health, chat

app = FastAPI()
prefix_v1 = "/api/v1"

app.include_router(health.router, prefix=prefix_v1)
app.include_router(chat.router, prefix=prefix_v1)