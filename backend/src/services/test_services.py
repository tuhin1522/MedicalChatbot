"""
Test script to verify services module works correctly
Run: python -m src.services.test_services
"""

if __name__ == "__main__":
    print("Testing services module imports...\n")
    
    try:
        # Test core imports
        from src.core import config, logger
        print("✅ Core modules imported")
        
        # Test prompts
        from src.prompts import conversational_prompt
        print("✅ Prompts imported")
        
        # Test document service
        from src.services.document_service import load_pdf, text_split, text_chunks
        print(f"✅ Document service imported")
        print(f"   Text chunks: {len(text_chunks)}")
        
        # Test embedding service
        from src.services.embedding_service import embeddings
        print(f"✅ Embedding service imported")
        print(f"   Model: {config.EMBEDDING_MODEL}")
        
        # Test vector store
        from src.services.vectorstore_service import vectordb
        print(f"✅ Vector store imported")
        print(f"   Persist directory: {config.PERSIST_DIRECTORY}")
        
        # Test memory service
        from src.services.memory_service import memory
        print(f"✅ Memory service imported")
        print(f"   Window size: k=4")
        
        # Test RAG service
        from src.services.rag_service import conversational_qa, llm
        print(f"✅ RAG service imported")
        print(f"   LLM Model: {config.LLM_MODEL}")
        
        # Test chat service
        from src.services.chat_service import conversational_chat
        print(f"✅ Chat service imported")
        
        print("\n" + "="*80)
        print("🎉 All services imported successfully!")
        print("="*80)
        
        print("\n📊 System Summary:")
        print(f"   Documents indexed: {len(text_chunks)} chunks")
        print(f"   Embedding model: {config.EMBEDDING_MODEL}")
        print(f"   LLM model: {config.LLM_MODEL}")
        print(f"   Memory window: {config.MEMORY_WINDOW_SIZE} Q&A pairs")
        print(f"   Retrieval k: {config.RETRIEVAL_K}")
        print(f"   Temperature: {config.TEMPERATURE}")
        
        print("\n✅ All services are ready to use!")
        print("   You can now run: python -m src.services.chat_service")
        
    except ImportError as e:
        print(f"\n❌ Import Error: {e}")
        print("   Please ensure all dependencies are installed")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
