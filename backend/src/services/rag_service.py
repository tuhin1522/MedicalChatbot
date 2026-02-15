from ..core import config, logger
from langchain_ollama import ChatOllama
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from .embedding_service import embeddings
from .vectorstore_service import vectordb
from .memory_service import memory
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