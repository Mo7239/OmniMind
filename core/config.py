from pydantic_settings import BaseSettings,SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    # LLM
    ollama_base_url: str = Field(default="http://localhost:11434")
    ollama_model: str = Field(default="mistral")

    # Memory
    short_term_max_messages: int = Field(default=20)
    long_term_collection_name: str = Field(default="omnimind_memory")

    # ChromaDB
    chroma_persist_dir: str = Field(default="./data/chroma")

    #Embedding Model
    embedding_model: str = Field(default="all-MiniLM-L6-v2")

    #Reranker model
    reranker_model: str = Field(default="cross-encoder/ms-marco-MiniLM-L-6-v2")


    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )    


settings = Settings()


if __name__ == "__main__":
    print(f"Checking Settings:")
    print(f"LLM Model: {settings.ollama_model}")
    print(f"Embedding: {settings.embedding_model}")
    print(f"DB Path: {settings.chroma_persist_dir}")