from typing import Optional, Dict, Any
from ..core import config, logger
from langchain_ollama import ChatOllama
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from .embedding_service import embeddings
from .vectorstore_service import vectordb
from .memory_service import memory, memory_manager
from ..prompts.medical_prompts import conversational_prompt

# Initialize Ollama LLM
llm = ChatOllama(
    model=config.LLM_MODEL,
    temperature=config.TEMPERATURE,
)

# Initialize conversational QA chain
conversational_qa = None

try:
    if vectordb is not None:
        conversational_qa = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectordb.as_retriever(
                search_type=config.SEARCH_TYPE,
                search_kwargs={'k': config.RETRIEVAL_K}
            ),
            memory=memory,
            return_source_documents=True,
            verbose=False,  # Set to True for debugging
            combine_docs_chain_kwargs={"prompt": conversational_prompt}
        )
        logger.info("Conversational RAG chain initialized successfully")
    else:
        logger.warning("Vector database not available, conversational QA chain not initialized")
    
except Exception as e:
    logger.error(f"Failed to create conversational chain: {e}")
    conversational_qa = None


def process_query_with_session(question: str, session_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Process a query with session-specific conversation memory
    
    Args:
        question: User's question
        session_id: Session identifier for conversation tracking
        
    Returns:
        Dict containing answer and source documents
        
    Raises:
        ValueError: If conversational_qa is not initialized
    """
    if conversational_qa is None:
        raise ValueError("RAG service not initialized")
    
    # Get session-specific memory
    session_memory = memory_manager.get_memory(session_id)
    
    # Temporarily swap memory in the chain
    original_memory = conversational_qa.memory
    conversational_qa.memory = session_memory
    
    try:
        # Process the query
        result = conversational_qa({"question": question})
        logger.debug(f"Query processed for session: {session_id}")
        return result
    finally:
        # Restore original memory
        conversational_qa.memory = original_memory