"""
Database Models for Medical Chatbot
SQLModel models for PostgreSQL database
"""

from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship


class User(SQLModel, table=True):
    """User model for authentication"""
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    full_name: str = Field(max_length=255)
    password_hash: str = Field()
    is_verified: bool = Field(default=False)
    verification_token: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    conversations: List["Conversation"] = Relationship(back_populates="user")


class Conversation(SQLModel, table=True):
    """Conversation model for storing chat sessions"""
    __tablename__ = "conversation"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key="users.id")
    
    # Relationships
    user: User = Relationship(back_populates="conversations")
    messages: List["Message"] = Relationship(back_populates="conversation")


class Message(SQLModel, table=True):
    """Message model for storing chat messages"""
    __tablename__ = "message"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id", index=True)
    role: str = Field(max_length=50)  # 'user' or 'assistant'
    content: str = Field()
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    
    # Metadata fields
    query_type: Optional[str] = Field(default=None, max_length=100)
    elapsed_time: Optional[float] = Field(default=None)
    docs_retrieved: Optional[int] = Field(default=None)
    
    # Relationships
    conversation: Conversation = Relationship(back_populates="messages")
    
    class Config:
        """SQLModel configuration"""
        json_schema_extra = {
            "example": {
                "conversation_id": 1,
                "role": "user",
                "content": "What is diabetes?",
                "query_type": "medical_query",
                "elapsed_time": 2.5,
                "docs_retrieved": 5
            }
        }


# Pydantic schemas for API requests/responses
class UserCreate(SQLModel):
    """Schema for user registration"""
    email: str = Field(max_length=255)
    full_name: str = Field(max_length=255)
    password: str = Field(min_length=8)


class UserSchema(SQLModel):
    """Schema for user response (without password)"""
    id: int
    email: str
    full_name: str
    is_verified: bool
    created_at: datetime


class Token(SQLModel):
    """Schema for JWT token response"""
    access_token: str
    token_type: str


class ForgotPasswordRequest(SQLModel):
    """Schema for forgot password request"""
    email: str


class ResetPasswordRequest(SQLModel):
    """Schema for reset password request"""
    token: str
    new_password: str = Field(min_length=8)
