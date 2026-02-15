"""
Core module for Medical Chatbot
Provides configuration, logging, and custom exceptions
"""

from .config import ChatbotConfig, config, get_config
from .logging_config import logger
from .exceptions import (
    ChatbotException,
    MedicalChatbotException,
    ConfigurationError,
    DocumentLoadError,
    EmbeddingError,
    VectorStoreError,
    RAGServiceError,
    QueryValidationError,
    EmergencyDetectedError,
    HarmfulQueryError,
    ServiceInitializationError,
    MemoryServiceError,
    ChatServiceError,
    ModelNotFoundError,
    DatabaseClearError,
)

__all__ = [
    # Configuration
    "ChatbotConfig",
    "config",
    "get_config",
    # Logging
    "logger",
    # Exceptions
    "ChatbotException",
    "MedicalChatbotException",
    "ConfigurationError",
    "DocumentLoadError",
    "EmbeddingError",
    "VectorStoreError",
    "RAGServiceError",
    "QueryValidationError",
    "EmergencyDetectedError",
    "HarmfulQueryError",
    "ServiceInitializationError",
    "MemoryServiceError",
    "ChatServiceError",
    "ModelNotFoundError",
    "DatabaseClearError",
]
