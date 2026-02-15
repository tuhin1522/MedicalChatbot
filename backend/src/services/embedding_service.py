from langchain_ollama import OllamaEmbeddings
from ..core import config, logger

# Initialize Ollama embeddings with nomic-embed-text model
def download_ollama_embeddings():
    embeddings = OllamaEmbeddings(model=config.EMBEDDING_MODEL)
    return embeddings

embeddings = download_ollama_embeddings()
logger.info(f"Embeddings initialized with model: {config.EMBEDDING_MODEL}")
print(f"Ollama embeddings initialized successfully!")
print(f"   Model: {config.EMBEDDING_MODEL}")