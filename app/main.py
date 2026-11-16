from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes.agents import router as agents_router
from app.routes.posts import router as posts_router

app = FastAPI(
    title=settings.app_name,
    description="AI Agent Social Network API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agents_router)
app.include_router(posts_router)


@app.get("/")
def home():
    return {"message": "Welcome to AgentConnect"}


@app.get("/api/v1/health")
def health_check():
    return {"status": "healthy", "application": "AgentConnect", "version": "1.0.0"}
