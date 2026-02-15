"""
Custom exceptions for the Medical Chatbot application
"""

class ChatbotException(Exception):
    """Base exception for all chatbot errors"""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class MedicalChatbotException(ChatbotException):
    """Base exception for all medical chatbot errors"""
    pass


class ConfigurationError(MedicalChatbotException):
    """Raised when configuration is invalid or missing"""
    def __init__(self, message: str, config_key: str = None):
        super().__init__(message)
        self.config_key = config_key


class DocumentLoadError(MedicalChatbotException):
    """Raised when document loading fails"""
    pass


class EmbeddingError(MedicalChatbotException):
    """Raised when embedding generation fails"""
    pass


class VectorStoreError(MedicalChatbotException):
    """Raised when vector store operations fail"""
    def __init__(self, message: str, operation: str = None):
        super().__init__(message)
        self.operation = operation


class RAGServiceError(MedicalChatbotException):
    """Raised when RAG service operations fail"""
    pass


class QueryValidationError(MedicalChatbotException):
    """Raised when query validation fails"""
    def __init__(self, message: str, suggestions: list = None):
        super().__init__(message)
        self.suggestions = suggestions or []


class EmergencyDetectedError(MedicalChatbotException):
    """Raised when emergency keywords are detected"""
    def __init__(self, emergency_type: str = "unknown", query: str = ""):
        message = f"Emergency detected: {emergency_type}"
        super().__init__(message)
        self.emergency_type = emergency_type
        self.query = query
        self.emergency_contacts = [
            "Emergency: 911",
            "Suicide Prevention Lifeline: 988",
            "Crisis Text Line: Text HOME to 741741"
        ]


class MemoryServiceError(MedicalChatbotException):
    """Raised when memory service operations fail"""
    pass


class ChatServiceError(MedicalChatbotException):
    """Raised when chat service operations fail"""
    pass


class ModelNotFoundError(MedicalChatbotException):
    """Raised when required Ollama model is not found"""
    def __init__(self, model_name: str):
        message = f"Model '{model_name}' not found"
        super().__init__(message)
        self.model_name = model_name
        self.install_command = f"ollama pull {model_name}"


class HarmfulQueryError(MedicalChatbotException):
    """Raised when harmful content is detected in query"""
    def __init__(self, query: str = "", reason: str = "Harmful content detected"):
        super().__init__(reason)
        self.query = query
        self.reason = reason


class ServiceInitializationError(MedicalChatbotException):
    """Raised when service initialization fails"""
    def __init__(self, message: str, service_name: str = "unknown", resolution: str = ""):
        super().__init__(message)
        self.service_name = service_name
        self.resolution = resolution


class DatabaseClearError(MedicalChatbotException):
    """Raised when database clearing fails"""
    pass
