from fastapi import APIRouter
from models.ollama_llm import OllamaLLM

router = APIRouter()

@router.get("/health")
def health_check():
    llm = OllamaLLM()
    return{
        "status": "ok",
        "ollama": llm.is_available()
    }