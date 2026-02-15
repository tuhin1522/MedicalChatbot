"""
Request Models for Medical Chatbot API
Pydantic models for validating incoming requests
"""

from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    query: str = Field(..., min_length=1, max_length=2000, description="User's medical query")
    session_id: Optional[str] = Field(None, description="Session ID for conversation tracking")
    
    @validator('query')
    def validate_query(cls, v):
        """Validate and clean the query"""
        v = v.strip()
        if not v:
            raise ValueError("Query cannot be empty or whitespace only")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "What are the symptoms of diabetes?",
                "session_id": "user_123456"
            }
        }


class ResetRequest(BaseModel):
    """Request model for resetting conversation"""
    session_id: Optional[str] = Field(None, description="Session ID to reset (optional)")
    confirm: bool = Field(True, description="Confirmation flag")
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "user_123456",
                "confirm": True
            }
        }


class ExportRequest(BaseModel):
    """Request model for exporting conversation history"""
    session_id: Optional[str] = Field(None, description="Session ID to export")
    format: str = Field("json", description="Export format (json/txt)")
    
    @validator('format')
    def validate_format(cls, v):
        """Validate export format"""
        if v.lower() not in ['json', 'txt']:
            raise ValueError("Format must be 'json' or 'txt'")
        return v.lower()
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "user_123456",
                "format": "json"
            }
        }
