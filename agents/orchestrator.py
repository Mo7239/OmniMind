from agents.researcher_agent import ResearcherAgent
from agents.summarizer_agent import SummarizerAgent
from agents.fact_checker_agent import FactCheckerAgent
from memory.memory_manager import MemoryManager
from rag.retriever import Retriever
from core.logger import get_logger
from typing import Generator

logger = get_logger(__name__)


class Orchestrator:

    def __init__(self):
        self.memory = MemoryManager()
        self.retriever = Retriever()

        self.researcher = ResearcherAgent(
            memory_manager=self.memory,
            retriever=self.retriever
        )
        self.summarizer = SummarizerAgent(
            memory_manager=self.memory
        )
        self.fact_checker = FactCheckerAgent(
            memory_manager=self.memory,
            retriever=self.retriever
        )

        logger.info("Orchestrator initialized")

    def get_agent_name(self, query: str) -> str:
        query_lower = query.lower()
        if any(word in query_lower for word in ["summarize", "summary", "تلخيص", "لخص"]):
            return "Summarizer"
        elif any(word in query_lower for word in ["verify", "fact", "true", "false", "تحقق", "صح", "غلط"]):
            return "FactChecker"
        else:
            return "Researcher"

    def route(self, query: str) -> tuple[str, str]:
        agent_name = self.get_agent_name(query)

        if agent_name == "Summarizer":
            return self.summarizer.run(query), "Summarizer"
        elif agent_name == "FactChecker":
            return self.fact_checker.run(query), "FactChecker"
        else:
            return self.researcher.run(query), "Researcher"

    def stream(self, query: str) -> Generator[str, None, None]:
        agent_name = self.get_agent_name(query)

        if agent_name == "Summarizer":
            yield from self.summarizer.stream(query)
        elif agent_name == "FactChecker":
            yield from self.fact_checker.stream(query)
        else:
            yield from self.researcher.stream(query)

    def add_documents(self, path: str) -> None:
        from rag.document_loader import DocumentLoader
        loader = DocumentLoader()

        import os
        if os.path.isdir(path):
            docs = loader.load_directory(path)
        else:
            docs = loader.load(path)

        self.retriever.add_documents(docs)
        logger.info(f"Documents added | path={path}")