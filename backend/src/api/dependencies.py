"""
Dependency Injection for Medical Chatbot API
Provides shared instances of services and configurations
"""

from functools import lru_cache
from typing import Generator, Optional
from fastapi import Depends

from ..core import config, logger, get_config
from ..core.exceptions import ServiceInitializationError
from ..validators import SafetyValidator, safety
from ..analyzers import ResponseAnalyzer, PerformanceMetrics, analyzer


# Global instances for performance tracking
_performance_metrics: Optional[PerformanceMetrics] = None
_start_time: Optional[float] = None


def get_performance_metrics() -> PerformanceMetrics:
    """
    Get global performance metrics instance
    
    Returns:
        PerformanceMetrics: Performance metrics tracker
    """
    global _performance_metrics
    if _performance_metrics is None:
        _performance_metrics = PerformanceMetrics()
        logger.info("Performance metrics initialized")
    return _performance_metrics


def get_start_time() -> float:
    """
    Get service start time
    
    Returns:
        float: Start time timestamp
    """
    global _start_time
    if _start_time is None:
        import time
        _start_time = time.time()
    return _start_time


@lru_cache()
def get_chatbot_config():
    """
    Get chatbot configuration (cached)
    
    Returns:
        ChatbotConfig: Configuration instance
    """
    return get_config()


def get_safety_validator() -> SafetyValidator:
    """
    Get safety validator instance
    
    Returns:
        SafetyValidator: Validator for safety checks
    """
    return safety


def get_response_analyzer() -> ResponseAnalyzer:
    """
    Get response analyzer instance
    
    Returns:
        ResponseAnalyzer: Analyzer for response quality
    """
    return analyzer


def get_rag_service():
    """
    Get RAG service (conversational QA chain)
    Lazy loads the service to avoid import errors if dependencies not installed
    
    Returns:
        ConversationalRetrievalChain: RAG service
        
    Raises:
        ServiceInitializationError: If service cannot be initialized
    """
    try:
        from ..services.rag_service import conversational_qa
        
        if conversational_qa is None:
            raise ServiceInitializationError(
                "RAG service not initialized",
                "conversational_qa",
                "Ensure dependencies are installed and vector database is created"
            )
        
        return conversational_qa
    except ImportError as e:
        logger.error(f"Failed to import RAG service: {e}")
        raise ServiceInitializationError(
            "RAG service dependencies not available",
            "rag_service",
            "Install required packages: pip install langchain langchain-community langchain-ollama langchain-chroma"
        )
    except Exception as e:
        logger.error(f"Failed to initialize RAG service: {e}")
        raise ServiceInitializationError(
            "RAG service initialization failed",
            "rag_service",
            str(e)
        )


def get_memory_service():
    """
    Get conversation memory manager (session-aware)
    
    Returns:
        SessionMemoryManager: Memory manager with per-session support
        
    Raises:
        ServiceInitializationError: If service cannot be initialized
    """
    try:
        from ..services.memory_service import memory_manager
        
        if memory_manager is None:
            raise ServiceInitializationError(
                "Memory service not initialized",
                "memory",
                "Ensure dependencies are installed"
            )
        
        return memory_manager
    except ImportError as e:
        logger.error(f"Failed to import memory service: {e}")
        raise ServiceInitializationError(
            "Memory service dependencies not available",
            "memory_service",
            "Install required packages: pip install langchain"
        )
    except Exception as e:
        logger.error(f"Failed to initialize memory service: {e}")
        raise ServiceInitializationError(
            "Memory service initialization failed",
            "memory_service",
            str(e)
        )


def get_vectorstore_service():
    """
    Get vector store service
    
    Returns:
        Chroma: Vector database instance
        
    Raises:
        ServiceInitializationError: If service cannot be initialized
    """
    try:
        from ..services.vectorstore_service import vectordb
        
        if vectordb is None:
            raise ServiceInitializationError(
                "Vector store not initialized",
                "vectordb",
                "Run store_index.py to create the vector database first"
            )
        
        return vectordb
    except ImportError as e:
        logger.error(f"Failed to import vector store service: {e}")
        raise ServiceInitializationError(
            "Vector store dependencies not available",
            "vectorstore_service",
            "Install required packages: pip install langchain-chroma"
        )
    except Exception as e:
        logger.error(f"Failed to initialize vector store: {e}")
        raise ServiceInitializationError(
            "Vector store initialization failed",
            "vectorstore_service",
            str(e)
        )


def verify_ollama_models() -> dict:
    """
    Verify that required Ollama models are installed
    
    Returns:
        dict: Model status information
        
    Raises:
        ServiceInitializationError: If models are not available
    """
    import subprocess
    import json
    
    try:
        # Check Ollama models
        result = subprocess.run(
            ['ollama', 'list'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode != 0:
            raise ServiceInitializationError(
                "Ollama service not available",
                "ollama",
                "Ensure Ollama is installed and running"
            )
        
        models_output = result.stdout.lower()
        
        # Check for required models
        llm_model = config.LLM_MODEL.lower()
        embedding_model = config.EMBEDDING_MODEL.lower()
        
        llm_available = llm_model in models_output
        embedding_available = embedding_model in models_output
        
        if not llm_available:
            raise ServiceInitializationError(
                f"LLM model '{config.LLM_MODEL}' not found",
                "ollama_model",
                f"Install with: ollama pull {config.LLM_MODEL}"
            )
        
        if not embedding_available:
            raise ServiceInitializationError(
                f"Embedding model '{config.EMBEDDING_MODEL}' not found",
                "ollama_model",
                f"Install with: ollama pull {config.EMBEDDING_MODEL}"
            )
        
        return {
            "status": "operational",
            "llm_model": config.LLM_MODEL,
            "embedding_model": config.EMBEDDING_MODEL,
            "models_available": True
        }
        
    except subprocess.TimeoutExpired:
        raise ServiceInitializationError(
            "Ollama service timeout",
            "ollama",
            "Ollama is not responding. Check if the service is running."
        )
    except FileNotFoundError:
        raise ServiceInitializationError(
            "Ollama not installed",
            "ollama",
            "Install Ollama from https://ollama.ai"
        )
    except Exception as e:
        logger.error(f"Ollama verification failed: {e}")
        raise ServiceInitializationError(
            "Ollama verification failed",
            "ollama",
            str(e)
        )


# Dependency for routes that need configuration
async def get_config_dependency():
    """FastAPI dependency for configuration"""
    return get_chatbot_config()


# Dependency for routes that need safety validation
async def get_safety_dependency():
    """FastAPI dependency for safety validator"""
    return get_safety_validator()


# Dependency for routes that need response analysis
async def get_analyzer_dependency():
    """FastAPI dependency for response analyzer"""
    return get_response_analyzer()


# Dependency for routes that need metrics
async def get_metrics_dependency():
    """FastAPI dependency for performance metrics"""
    return get_performance_metrics()
