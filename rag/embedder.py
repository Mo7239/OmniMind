from typing import List
from sentence_transformers import SentenceTransformer
from core.logger import get_logger
from core.config import settings

logger = get_logger(__name__)

class Embedder:
    def __init__(self, model_name : str =settings.embedding_model):
        self.model = SentenceTransformer(model_name)
        logger.info(f"Embedder initialized | model={model_name}")

    def embed(self, texts : List [str]) -> List[List[float]]:
        embeddings = self.model.encode(texts,show_progress_bar=False)
        logger.debug(f"Embedded {len(texts)} texts")
        return embeddings.tolist()
    
    def embed_one(self, text:str) -> List[float]:
        return self.embed([text])[0]
