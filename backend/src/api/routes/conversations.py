"""
Conversation Management Routes
Endpoints for managing conversations and messages
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, col

from ...core import logger
from ...postgresql_db.models import (
    User,
    Conversation,
    Message,
    ConversationSchema,
    MessageSchema
)
from ...postgresql_db.database import get_session
from ...auth import get_current_user


router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"]
)


@router.get("", response_model=List[ConversationSchema])
async def get_conversations(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get all conversations for the current user
    
    Args:
        session: Database session
        current_user: Current authenticated user
        
    Returns:
        List[ConversationSchema]: List of conversations
    """
    logger.info(f"Fetching conversations for user: {current_user.email}")
    
    statement = select(Conversation).where(
        Conversation.user_id == current_user.id
    ).order_by(col(Conversation.created_at).desc())
    
    results = session.exec(statement).all()
    
    logger.info(f"Found {len(results)} conversations for user: {current_user.email}")
    
    return [
        ConversationSchema(
            id=c.id if c.id is not None else 0,
            title=c.title,
            created_at=c.created_at
        ) for c in results
    ]


@router.get("/{conversation_id}/messages", response_model=List[MessageSchema])
async def get_messages(
    conversation_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get all messages for a specific conversation
    
    Args:
        conversation_id: ID of the conversation
        session: Database session
        current_user: Current authenticated user
        
    Returns:
        List[MessageSchema]: List of messages
        
    Raises:
        HTTPException: If conversation not found or unauthorized
    """
    logger.info(f"Fetching messages for conversation {conversation_id}")
    
    # Verify conversation exists and belongs to user
    conversation = session.get(Conversation, conversation_id)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    if conversation.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this conversation"
        )
    
    # Get messages
    statement = select(Message).where(
        Message.conversation_id == conversation_id
    ).order_by(col(Message.created_at).asc())
    
    results = session.exec(statement).all()
    
    logger.info(f"Found {len(results)} messages for conversation {conversation_id}")
    
    return results


@router.delete("/{conversation_id}")
async def delete_conversation(
    conversation_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a conversation and all its messages
    
    Args:
        conversation_id: ID of the conversation to delete
        session: Database session
        current_user: Current authenticated user
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: If conversation not found or unauthorized
    """
    logger.info(f"Delete request for conversation {conversation_id} by user: {current_user.email}")
    
    # Get conversation
    db_conversation = session.get(Conversation, conversation_id)
    if not db_conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    # Verify ownership
    if db_conversation.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this conversation"
        )
    
    # Delete messages first
    statement = select(Message).where(Message.conversation_id == conversation_id)
    messages = session.exec(statement).all()
    for msg in messages:
        session.delete(msg)
    
    # Delete conversation
    session.delete(db_conversation)
    session.commit()
    
    logger.info(f"Successfully deleted conversation {conversation_id} with {len(messages)} messages")
    
    return {"message": "Conversation deleted successfully"}
