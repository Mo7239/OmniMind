from typing import Generator
from agents.base_agent import BaseAgent
from memory.memory_manager import MemoryManager
from rag.retriever import Retriever
from core.logger import get_logger

logger = get_logger(__name__)


class ResearcherAgent(BaseAgent):

    def __init__(self, memory_manager: MemoryManager, retriever: Retriever):
        super().__init__(name="Researcher", memory_manager=memory_manager)
        self.retriever = retriever

    def _rewrite_query(self, query: str) -> str:
        history = self.memory.short_term.get_as_string()

        if not history:
            return query

        rewriter_prompt = (
            "You are a query reformulation assistant. "
            "Your job is to rewrite follow-up questions to be standalone.\n\n"
            "CRITICAL RULES:\n"
            "1. If the question has NO pronouns (it, its, this, that, they, their, them), return it EXACTLY as written\n"
            "2. If it HAS pronouns, replace them with the actual subject from the chat history\n"
            "3. NEVER remove words like 'What is', 'Does', 'How', etc.\n"
            "4. NEVER shorten or modify the question structure\n"
            "5. Return ONLY the rewritten question, nothing else\n\n"
            "Examples:\n"
            "Input: 'What is artificial intelligence'\n"
            "Output: 'What is artificial intelligence'\n\n"
            "Input: 'What is its importance?' (after AI discussion)\n"
            "Output: 'What is artificial intelligence importance?'\n\n"
            f"=== Chat History ===\n{history}\n\n"
            f"Question: {query}\n"
            "Rewritten Question:"
        )

        rewritten = self.llm.generate(rewriter_prompt).strip()
        logger.debug(f"Query rewritten | original={query} | rewritten={rewritten}")
        return rewritten

    def _build_rag_prompt(self, query: str) -> tuple[str, str]:
        standalone_query = self._rewrite_query(query)

        docs = self.retriever.search(standalone_query, top_k=3)

        if not docs:
            context = "No relevant documents found."
        else:
            context = "\n\n".join(
                f"[Source: {d['metadata'].get('source', 'unknown')}]\n{d['content']}"
                for d in docs
            )

        system = (
            "You are a research assistant. "
            "Use the provided document context to answer the user's question accurately. "
            "If the answer is not in the context, say so clearly."
        )

        prompt = (
            f"{system}\n\n"
            f"=== Document Context ===\n{context}\n\n"
            f"=== Conversation History ===\n{self.memory.short_term.get_as_string()}\n\n"
            f"USER: {query}\nASSISTANT:"
        )

        return prompt, standalone_query

    def run(self, query: str) -> str:
        logger.info(f"Researcher running | query={query[:30]}")
        prompt, standalone_query = self._build_rag_prompt(query)
        response = self.llm.generate(prompt=prompt)
        self._save_interaction(query, response)
        logger.info(f"Researcher done | agent={self.name}")
        return response

    def stream(self, query: str) -> Generator[str, None, None]:
        logger.info(f"Researcher streaming | query={query[:30]}")
        prompt, standalone_query = self._build_rag_prompt(query)
        full_response = ""

        for chunk in self.llm.stream(prompt):
            full_response += chunk
            yield chunk

        self._save_interaction(query, full_response)
        logger.info(f"Researcher stream done | agent={self.name}")