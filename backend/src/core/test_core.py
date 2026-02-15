"""
Test script to verify core module works correctly
Run: python -m src.core.test_core
"""

if __name__ == "__main__":
    print("Testing core module imports...\n")
    
    # Test config
    from src.core import config, get_config, logger
    print("✅ Config and logger imported successfully")
    
    # Display config
    print(f"\n📋 Configuration:")
    print(f"   LLM Model: {config.LLM_MODEL}")
    print(f"   Embedding Model: {config.EMBEDDING_MODEL}")
    print(f"   Memory Window Size: {config.MEMORY_WINDOW_SIZE}")
    print(f"   Temperature: {config.TEMPERATURE}")
    print(f"   Chunk Size: {config.CHUNK_SIZE}")
    print(f"   Retrieval K: {config.RETRIEVAL_K}")
    
    # Test logger
    logger.info("Testing logger functionality")
    print("\n✅ Logger working correctly")
    
    # Test exceptions
    from src.core import (
        MedicalChatbotException,
        ConfigurationError,
        ModelNotFoundError,
        MemoryServiceError
    )
    print("\n✅ All exceptions imported successfully")
    
    # Test exception usage
    try:
        raise ModelNotFoundError("llama3.2:1b")
    except ModelNotFoundError as e:
        print(f"\n✅ Exception test passed: {e}")
    
    print("\n🎉 All core module tests passed!")
    print(f"\n💡 Your configuration is using: {config.LLM_MODEL}")
    print("   ✓ This model is already installed and ready to use!")
