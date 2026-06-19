from agents.base_agent import BaseAgent
from memory.memory_manager import MemoryManager
from core.logger import get_logger

logger = get_logger(__name__)

class SummarizerAgent(BaseAgent):
    def __init__(self, memory_manager: MemoryManager):
        super().__init__(name="Summarizer",memory_manager=memory_manager)

    def run(self, query):
        logger.info(f"Summarizer running | query={query[:30]}")
        history = self.memory.short_term.get_as_string()   


        system = (
            "You are a summarization assistant. "
            "Your job is to summarize the conversation or any provided text clearly and concisely. "
            "Focus on key points only."
        )

        prompt = (
            f"{system}\n\n"
            f"=== Conversation History ===\n{history}\n\n"
            f"USER: {query}\nASSISTANT:"
        )

        response = self.llm.generate(prompt)
        self._save_interaction(query, response)

        logger.info(f"Summarizer done | agent={self.name}")
        return response
