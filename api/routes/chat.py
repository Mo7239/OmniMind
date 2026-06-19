from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from agents.orchestrator import Orchestrator
from api.dependencies import get_orchestrator
from core.logger import get_logger
import json

logger = get_logger(__name__)

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    agent_used: str


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    orchestrator: Orchestrator = Depends(get_orchestrator)
):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    logger.info(f"Chat request | message={request.message[:30]}")
    response, agent_used = orchestrator.route(request.message)
    return ChatResponse(response=response, agent_used=agent_used)


@router.post("/chat/stream")
async def chat_stream(
    request: ChatRequest,
    orchestrator: Orchestrator = Depends(get_orchestrator)
):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    logger.info(f"Stream request | message={request.message[:30]}")

    def generate():
        agent_used = orchestrator.get_agent_name(request.message)

        # أول chunk بيبعت اسم الـ agent
        yield f"data: {json.dumps({'type': 'agent', 'agent': agent_used})}\n\n"

        for chunk in orchestrator.stream(request.message):
            yield f"data: {json.dumps({'type': 'chunk', 'content': chunk})}\n\n"

        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


@router.get("/history")
def get_history(orchestrator: Orchestrator = Depends(get_orchestrator)):
    history = orchestrator.memory.get_short_term_history()
    return {"history": history}


@router.delete("/history")
def clear_history(orchestrator: Orchestrator = Depends(get_orchestrator)):
    orchestrator.memory.clear_all()
    return {"status": "success", "message": "History cleared"}