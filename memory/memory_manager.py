import uuid
from typing import List
from core.logger import get_logger
from memory.short_term import ShortTermMemory
from memory.long_term import LongTermMemory


logger = get_logger(__name__) 

class MemoryManager:
    def __init__(self):
        self.short_term = ShortTermMemory()
        self.long_term = LongTermMemory()
        logger.info("MemoryManager initialized")

    def add_message(self, role : str, content : str)->None:
        self.short_term.add(role=role , content=content)
        doc_id = str(uuid.uuid4())
        self.long_term.save(
            doc_id=doc_id,
            content=content,
            metadata={"role":role}
        )

    def get_context(self, query : str)->str:
        short_term_context = self.short_term.get_as_string()
        long_term_results = self.long_term.search(query=query, top_k=3)

        long_term_context = "\n".join(
            f"- ({mem['metadata']['role']}) {mem['content']}" for mem in long_term_results
        )
        
        context = (
            f"=== Recent Conversation ===\n{short_term_context}\n\n"
            f"=== Relevant Past Memories ===\n{long_term_context}"
        )
        logger.debug("Context built successfully")
        return context        
    

    def clear_all(self) -> None:
        self.short_term.clear()
        self.long_term.clear()
        logger.info("All memory cleared")    


    def get_short_term_history(self) -> List[dict]:
        return self.short_term.get_all()        