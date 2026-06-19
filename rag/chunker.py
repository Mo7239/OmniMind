from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rag.document_loader import Document
from core.logger import get_logger

logger = get_logger(__name__)

class Chunker:
    def __init__(self,chunk_size: int = 500, chunk_overlap: int = 50):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap = chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

    def chunk(self, documents:List[Document]) -> List[Document]:
        all_chunks = []
        for doc in documents:
            chunks = self.splitter.split_text(doc.content)
            for idx , chunk in enumerate(chunks):
                all_chunks.append(Document(
                    content=chunk,
                    metadata={**doc.metadata, "chunk_index": idx}
                ))

        logger.info(f"Created {len(all_chunks)} chunks from {len(documents)} documents")
        return all_chunks



        