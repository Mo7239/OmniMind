from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from api.routes import chat, documents, health

app = FastAPI(
    title="OmniMind API",
    description="AI Assistant with RAG and Multi-Agent System",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["Health"])
app.include_router(chat.router, tags=["Chat"])
app.include_router(documents.router, tags=["Documents"])

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
