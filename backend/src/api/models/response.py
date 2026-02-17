"""
Response Models for Medical Chatbot API
Pydantic models for formatting API responses
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum


class ResponseStatus(str, Enum):
    """Response status enum"""
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"


class SourceDocument(BaseModel):
    """Model for source document information"""
    content: str = Field(..., description="Document content snippet")
    page: Optional[int] = Field(None, description="Page number (if available)")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    status: ResponseStatus = Field(..., description="Response status")
    response: str = Field(..., description="Chatbot's response")
    conversation_id: int = Field(..., description="Conversation ID")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Response metadata")
    sources: List[SourceDocument] = Field(default_factory=list, description="Source documents")
    confidence: Optional[str] = Field(None, description="Confidence level (high/medium/low)")
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Confidence score (0-1)")
    response_time: Optional[float] = Field(None, description="Response time in seconds")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")
    disclaimer: Optional[str] = Field(None, description="Safety disclaimer (if applicable)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "response": "Diabetes symptoms include increased thirst, frequent urination, and fatigue.",
                "conversation_id": 1,
                "metadata": {
                    "query_type": "medical_query",
                    "elapsed_time": 1.23,
                    "docs_retrieved": 5
                },
                "sources": [
                    {
                        "content": "Common symptoms of diabetes...",
                        "page": 42,
                        "metadata": {"source": "medical_guide.pdf"}
                    }
                ],
                "confidence": "high",
                "confidence_score": 0.85,
                "response_time": 1.23,
                "timestamp": "2026-02-15T10:30:00"
            }
        }


class ConversationMessage(BaseModel):
    """Model for a single conversation message"""
    role: str = Field(..., description="Message role (human/ai)")
    content: str = Field(..., description="Message content")
    timestamp: Optional[datetime] = Field(None, description="Message timestamp")


class HistoryResponse(BaseModel):
    """Response model for conversation history"""
    status: ResponseStatus = Field(..., description="Response status")
    messages: List[ConversationMessage] = Field(default_factory=list, description="Conversation messages")
    session_id: Optional[str] = Field(None, description="Session ID")
    total_messages: int = Field(0, description="Total number of messages")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "messages": [
                    {
                        "role": "human",
                        "content": "What are diabetes symptoms?",
                        "timestamp": "2026-02-15T10:29:00"
                    },
                    {
                        "role": "ai",
                        "content": "Diabetes symptoms include...",
                        "timestamp": "2026-02-15T10:29:02"
                    }
                ],
                "session_id": "user_123456",
                "total_messages": 2
            }
        }


class HealthResponse(BaseModel):
    """Response model for health check"""
    status: ResponseStatus = Field(..., description="Overall health status")
    ollama_status: str = Field(..., description="Ollama service status")
    llm_model: str = Field(..., description="LLM model name")
    embedding_model: str = Field(..., description="Embedding model name")
    database_status: str = Field(..., description="Vector database status")
    memory_window: int = Field(..., description="Conversation memory window size")
    timestamp: datetime = Field(default_factory=datetime.now, description="Health check timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "ollama_status": "operational",
                "llm_model": "llama3.2:1b",
                "embedding_model": "nomic-embed-text",
                "database_status": "connected",
                "memory_window": 4,
                "timestamp": "2026-02-15T10:30:00"
            }
        }


class MetricsResponse(BaseModel):
    """Response model for performance metrics"""
    status: ResponseStatus = Field(..., description="Response status")
    total_queries: int = Field(0, description="Total queries processed")
    successful_queries: int = Field(0, description="Successful queries")
    failed_queries: int = Field(0, description="Failed queries")
    average_response_time: float = Field(0.0, description="Average response time in seconds")
    average_confidence: float = Field(0.0, description="Average confidence score")
    uptime: Optional[float] = Field(None, description="Service uptime in seconds")
    timestamp: datetime = Field(default_factory=datetime.now, description="Metrics timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "total_queries": 150,
                "successful_queries": 142,
                "failed_queries": 8,
                "average_response_time": 1.45,
                "average_confidence": 0.78,
                "uptime": 3600.0,
                "timestamp": "2026-02-15T10:30:00"
            }
        }


class ErrorResponse(BaseModel):
    """Response model for errors"""
    status: ResponseStatus = Field(ResponseStatus.ERROR, description="Error status")
    error: str = Field(..., description="Error message")
    error_type: Optional[str] = Field(None, description="Error type/category")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.now, description="Error timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "error",
                "error": "Query validation failed",
                "error_type": "ValidationError",
                "details": {"field": "query", "issue": "too short"},
                "timestamp": "2026-02-15T10:30:00"
            }
        }


class SuccessResponse(BaseModel):
    """Generic success response"""
    status: ResponseStatus = Field(ResponseStatus.SUCCESS, description="Success status")
    message: str = Field(..., description="Success message")
    data: Optional[Dict[str, Any]] = Field(default=None, description="Additional data")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "message": "Operation completed successfully",
                "timestamp": "2026-02-15T10:30:00"
            }
        }
