from abc import ABC, abstractmethod
from typing import Generator
from models.ollama_llm import OllamaLLM
from memory.memory_manager import MemoryManager
from core.logger import get_logger

logger = get_logger(__name__)


class BaseAgent(ABC):

    def __init__(self, name: str, memory_manager: MemoryManager):
        self.name = name
        self.llm = OllamaLLM()
        self.memory = memory_manager
        logger.info(f"Agent initialized | name={self.name}")

    @abstractmethod
    def run(self, query: str) -> str:
        pass

    def stream(self, query: str) -> Generator[str, None, None]:
        prompt = self._build_prompt_for_stream(query)
        full_response = ""

        for chunk in self.llm.stream(prompt):
            full_response += chunk
            yield chunk

        self._save_interaction(query, full_response)

    def _build_prompt(self, system: str, query: str) -> str:
        context = self.memory.get_context(query)
        return f"{system}\n\n{context}\n\nUSER: {query}\nASSISTANT:"

    def _build_prompt_for_stream(self, query: str) -> str:
        return self._build_prompt(self._get_system_prompt(), query)

    def _get_system_prompt(self) -> str:
        return "You are a helpful AI assistant."

    def _save_interaction(self, query: str, response: str) -> None:
        self.memory.add_message("user", query)
        self.memory.add_message("assistant", response)
        logger.debug(f"Interaction saved | agent={self.name}")