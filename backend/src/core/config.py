from dataclasses import dataclass
from typing import Optional
import logging

@dataclass
class ChatbotConfig:
    """Centralized configuration for medical chatbot"""
    
    # Model Configuration
    EMBEDDING_MODEL: str = "nomic-embed-text"
    LLM_MODEL: str = "llama3.2:1b"
    TEMPERATURE: float = 0.3
    
    # Memory Configuration
    MEMORY_WINDOW_SIZE: int = 4  # Keep last 4 Q&A pairs (8 messages) to prevent overflow
    
    # Chunking Configuration
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 400
    
    # Retrieval Configuration
    RETRIEVAL_K: int = 5  # Retrieve top 3 documents
    SEARCH_TYPE: str = "similarity"  # or "mmr" for diversity
    
    # Database Configuration
    PERSIST_DIRECTORY: str = "db"
    DATA_DIRECTORY: str = "../data/"
    
    # Performance Configuration
    MAX_QUERY_LENGTH: int = 500
    REQUEST_TIMEOUT: int = 30
    
    # Safety Configuration
    ENABLE_MEDICAL_DISCLAIMER: bool = True
    ENABLE_QUERY_VALIDATION: bool = True
    ENABLE_EMERGENCY_DETECTION: bool = True
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"

# Initialize configuration
config = ChatbotConfig()

def get_config() -> ChatbotConfig:
    """Get the global configuration instance"""
    return config

if __name__ == "__main__":
    print("Configuration loaded successfully!")
    print(f"LLM Model: {config.LLM_MODEL}")
    print(f"Embedding Model: {config.EMBEDDING_MODEL}")
    print(f"Chunk Size: {config.CHUNK_SIZE}")
    print(f"Retrieval K: {config.RETRIEVAL_K}")
    print(f"Memory Window Size: {config.MEMORY_WINDOW_SIZE}")