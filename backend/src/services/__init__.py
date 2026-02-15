"""
Services module for Medical Chatbot
Provides document loading, embedding, vector store, memory, RAG, and chat services

Note: Services may fail to import if dependencies are not installed.
Install: pip install langchain langchain-community langchain-ollama langchain-chroma pypdf
"""

__all__ = [
    # Document processing
    "load_pdf",
    "filter_to_minimal_docs",
    "text_split",
    "extracted_data",
    "minimal_documents",
    "text_chunks",
    # Embeddings
    "download_ollama_embeddings",
    "embeddings",
    # Vector store
    "vectordb",
    # Memory
    "memory",
    # RAG
    "llm",
    "conversational_qa",
    # Chat
    "conversational_chat",
]

# Lazy imports to avoid circular dependencies and provide better error messages
def __getattr__(name):
    """Lazy loading of services"""
    if name in __all__:
        if name in ["load_pdf", "filter_to_minimal_docs", "text_split", "extracted_data", "minimal_documents", "text_chunks"]:
            from .document_service import load_pdf, filter_to_minimal_docs, text_split, extracted_data, minimal_documents, text_chunks
            return locals()[name]
        elif name in ["download_ollama_embeddings", "embeddings"]:
            from .embedding_service import download_ollama_embeddings, embeddings
            return locals()[name]
        elif name == "vectordb":
            from .vectorstore_service import vectordb
            return vectordb
        elif name == "memory":
            from .memory_service import memory
            return memory
        elif name in ["llm", "conversational_qa"]:
            from .rag_service import llm, conversational_qa
            return locals()[name]
        elif name == "conversational_chat":
            from .chat_service import conversational_chat
            return conversational_chat
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
