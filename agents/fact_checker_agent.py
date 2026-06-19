from agents.base_agent import BaseAgent
from memory.memory_manager import MemoryManager
from rag.retriever import Retriever
from core.logger import get_logger

logger = get_logger(__name__)


class FactCheckerAgent(BaseAgent):

    def __init__(self, memory_manager: MemoryManager, retriever: Retriever):
        super().__init__(name="FactChecker", memory_manager=memory_manager)
        self.retriever = retriever

    def run(self, query: str) -> str:
        logger.info(f"FactChecker running | query={query[:30]}")

        docs = self.retriever.search(query=query, top_k=3)

        if not docs:
            context = "No documents available to verify against."
        else:
            context = "\n\n".join(
                f"[Source: {d['metadata'].get('source', 'unknown')}]\n{d['content']}"
                for d in docs
            )

        system = (
            "You are a fact-checking assistant. "
            "Given the document context, verify whether the user's claim is true, false, or unverifiable. "
            "Always cite which source supports your conclusion."
        )

        prompt = (
            f"{system}\n\n"
            f"=== Document Context ===\n{context}\n\n"
            f"=== Conversation History ===\n{self.memory.short_term.get_as_string()}\n\n"
            f"USER: {query}\nASSISTANT:"
        )

        response = self.llm.generate(prompt)
        self._save_interaction(query, response)

        logger.info(f"FactChecker done | agent={self.name}")
        return response