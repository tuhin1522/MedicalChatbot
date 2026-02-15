from ..core import config, logger
from langchain_chroma import Chroma
from .embedding_service import embeddings

# Initialize ChromaDB
persist_directory = config.PERSIST_DIRECTORY

try:
    # Load existing vector store (don't create from documents at import time)
    vectordb = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )
    logger.info(f"Vector store loaded from '{persist_directory}'")
except Exception as e:
    logger.warning(f"Vector store not available: {e}")
    vectordb = None