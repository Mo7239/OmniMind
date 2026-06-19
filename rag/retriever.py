import uuid
from typing import List
import chromadb
from chromadb.utils import embedding_functions
from rank_bm25 import BM25Okapi
from sentence_transformers import CrossEncoder
from rag.document_loader import Document
from rag.chunker import Chunker
from core.config import settings
from core.logger import get_logger

logger = get_logger(__name__)


class Retriever:

    def __init__(self):
        self.chunker = Chunker()
        self.client = chromadb.PersistentClient(path=settings.chroma_persist_dir)
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=settings.embedding_model
        )
        self.collection = self.client.get_or_create_collection(
            name="omnimind_rag",
            embedding_function=self.embedding_fn
        )
        self.reranker = CrossEncoder(settings.reranker_model)

        self.bm25 = None
        self.bm25_chunks: List[dict] = []
        self._load_existing_documents()

        logger.info("Retriever initialized with Hybrid Search + Reranking")

    def _load_existing_documents(self) -> None:
        try:
            existing_data = self.collection.get()

            if existing_data and existing_data["documents"]:
                all_contents = existing_data["documents"]
                all_metadatas = existing_data["metadatas"]

                self.bm25_chunks = []
                for i in range(len(all_contents)):
                    self.bm25_chunks.append({
                        "content": all_contents[i],
                        "metadata": all_metadatas[i]
                    })

                tokenized_corpus = [doc.lower().split() for doc in all_contents]
                self.bm25 = BM25Okapi(tokenized_corpus)
                logger.info(f"Loaded {len(all_contents)} existing chunks into BM25 index")
            else:
                logger.info("No existing documents found in ChromaDB to index.")

        except Exception as e:
            logger.error(f"Failed to load existing documents: {e}")

    def add_documents(self, documents: List[Document]) -> None:
        chunks = self.chunker.chunk(documents)

        ids = [str(uuid.uuid4()) for _ in chunks]
        contents = [chunk.content for chunk in chunks]
        metadatas = [chunk.metadata for chunk in chunks]

        self.collection.upsert(
            ids=ids,
            documents=contents,
            metadatas=metadatas
        )

        new_chunks = [{"content": c, "metadata": m} for c, m in zip(contents, metadatas)]
        self.bm25_chunks.extend(new_chunks)

        tokenized_corpus = [doc["content"].lower().split() for doc in self.bm25_chunks]
        self.bm25 = BM25Okapi(tokenized_corpus)

        logger.info(f"Added {len(chunks)} chunks and updated Hybrid index")

    def _semantic_search(self, query: str, top_k: int) -> List[dict]:
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )
        docs = []
        for i, doc in enumerate(results["documents"][0]):
            docs.append({
                "content": doc,
                "metadata": results["metadatas"][0][i],
                "score": results["distances"][0][i],
                "source": "semantic"
            })
        return docs

    def _keyword_search(self, query: str, top_k: int) -> List[dict]:
        if not self.bm25 or not self.bm25_chunks:
            return []

        tokenized_query = query.lower().split()
        scores = self.bm25.get_scores(tokenized_query)

        top_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )[:top_k]

        docs = []
        for idx in top_indices:
            docs.append({
                "content": self.bm25_chunks[idx]["content"],
                "metadata": self.bm25_chunks[idx]["metadata"],
                "score": float(scores[idx]),
                "source": "keyword"
            })
        return docs

    def _fuse_results(self, semantic: List[dict], keyword: List[dict]) -> List[dict]:
        seen = {}

        for doc in semantic:
            key = doc["content"]
            if key not in seen:
                seen[key] = doc

        for doc in keyword:
            key = doc["content"]
            if key not in seen:
                seen[key] = doc

        return list(seen.values())

    def _rerank(self, query: str, docs: List[dict], top_k: int) -> List[dict]:
        if not docs:
            return []

        pairs = [[query, doc["content"]] for doc in docs]
        scores = self.reranker.predict(pairs)

        for i, doc in enumerate(docs):
            doc["rerank_score"] = float(scores[i])

        reranked = sorted(docs, key=lambda x: x["rerank_score"], reverse=True)
        return reranked[:top_k]

    def search(self, query: str, top_k: int = 5) -> List[dict]:
        semantic_results = self._semantic_search(query, top_k=top_k * 2)
        keyword_results = self._keyword_search(query, top_k=top_k * 2)

        fused = self._fuse_results(semantic_results, keyword_results)
        reranked = self._rerank(query, fused, top_k=top_k)

        logger.debug(
            f"Hybrid search done | "
            f"semantic={len(semantic_results)} "
            f"keyword={len(keyword_results)} "
            f"final={len(reranked)}"
        )
        return reranked

    def clear(self) -> None:
        self.client.delete_collection("omnimind_rag")
        self.collection = self.client.get_or_create_collection(
            name="omnimind_rag",
            embedding_function=self.embedding_fn
        )
        self.bm25 = None
        self.bm25_chunks = []
        logger.info("RAG collection cleared")

    def __len__(self) -> int:
        return self.collection.count()