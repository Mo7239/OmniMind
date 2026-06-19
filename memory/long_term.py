import chromadb
from chromadb.utils import embedding_functions
from typing import List
from core.config import settings
from core.logger import get_logger

logger = get_logger(__name__)

class LongTermMemory:
    def __init__(self):
        self.client  = chromadb.PersistentClient(path=settings.chroma_persist_dir)
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=settings.embedding_model)
        self.collection = self.client.get_or_create_collection(
            name=settings.long_term_collection_name,
            embedding_function=self.embedding_fn
        )
        logger.info("LongTermMemory initialized")

    def save(self, doc_id : str , content : str , metadata:dict = {})->None:
        self.collection.upsert(
            ids=[doc_id],
            documents=[content],
            metadatas=[metadata]
        )
        logger.debug(f"Saved to long-term memory | id={doc_id}")   

    def search(self, query : str , top_k : int = 3) -> List[dict]:
        results  = self.collection.query(
            query_texts = [query],
            n_results=top_k
        )

        memories = []
        for idx , doc in enumerate(results["documents"][0]):
            memories.append({
                "id": results["ids"][0][idx],
                "content": doc,
                "metadata": results["metadatas"][0][idx]

            })
        logger.debug(f"Retrieved {len(memories)} memories | query={query[:30]}")    
        return memories
    
    def delete(self, doc_id:str)->None:
        self.collection.delete(ids=[doc_id])
        logger.info(f"Deleted memory | id={doc_id}")

    def clear(self) -> None:
        self.client.delete_collection(settings.long_term_collection_name)
        self.collection = self.client.get_or_create_collection(
            name=settings.long_term_collection_name,
            embedding_function=self.embedding_fn
        )
        logger.info("Long-term memory cleared")
 
    def __len__(self) -> int:
        return self.collection.count()

