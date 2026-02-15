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

try:
    conversational_qa = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectordb.as_retriever(
            search_type=config.SEARCH_TYPE,
            search_kwargs={'k': config.RETRIEVAL_K}
        ),
        memory=memory,
        return_source_documents=True,
        verbose=True,  # Enable to debug query reformulation
        combine_docs_chain_kwargs={"prompt": conversational_prompt}
    )
    
    logger.info("Conversational RAG chain initialized successfully")
    print("🎉 Conversational RAG Chain Created Successfully!")
    print(f"   LLM Model: {config.LLM_MODEL}")
    print(f"   Temperature: {config.TEMPERATURE}")
    print(f"   Retrieval K: {config.RETRIEVAL_K}")
    print(f"   Memory: Enabled ✅")
    print("\n📝 KEY IMPROVEMENTS:")
    print("   ✅ Remembers conversation history")
    print("   ✅ Reformulates follow-up questions with context")  
    print("   ✅ Maintains topic continuity")
    print("   ✅ Retrieves correct documents for 'it', 'this', 'that'")
    print("\n💡 This is the ONLY chain you need - no separate 'qa' chain!")
    
except Exception as e:
    logger.error(f"Failed to create conversational chain: {e}")
    print(f"❌ Error: {e}")
    raise