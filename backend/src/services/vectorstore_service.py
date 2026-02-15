from ..core import config, logger
from langchain_chroma import Chroma

# Import dependencies
from .embedding_service import embeddings
from .document_service import text_chunks

# Initialize ChromaDB
persist_directory = config.PERSIST_DIRECTORY

try:
    vectordb = Chroma.from_documents(
        documents=text_chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    logger.info(f"Vector store created with {len(text_chunks)} documents")
    print(f"Vector store created and persisted to '{persist_directory}'!")
    print(f"   Total documents indexed: {len(text_chunks)}")
except Exception as e:
    logger.error(f"Failed to create vector store: {e}")
    raise