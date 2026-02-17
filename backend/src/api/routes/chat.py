"""
Chat Routes for Medical Chatbot API
Main endpoints for conversational interaction
"""

import time
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime
from sqlmodel import Session

from ...core import logger
from ...core.exceptions import EmergencyDetectedError, HarmfulQueryError
from ...postgresql_db.models import User, Conversation, Message
from ...postgresql_db.database import get_session
from ...auth import get_current_user
from ..dependencies import (
    get_rag_service,
    get_memory_service,
    get_safety_validator,
    get_response_analyzer,
    get_performance_metrics
)
from ..models.request import ChatRequest, ResetRequest, ExportRequest
from ..models.response import (
    ChatResponse,
    HistoryResponse,
    SuccessResponse,
    ConversationMessage,
    SourceDocument,
    ResponseStatus
)


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("", response_model=ChatResponse)
@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    safety_validator = Depends(get_safety_validator),
    response_analyzer = Depends(get_response_analyzer),
    metrics = Depends(get_performance_metrics)
):
    """
    Process a chat message and return AI response
    
    This endpoint:
    1. Creates or retrieves conversation
    2. Saves user message to database
    3. Validates the query for safety
    4. Processes the query through RAG pipeline
    5. Saves assistant response to database
    6. Returns structured response with conversation ID
    
    Args:
        request: ChatRequest with user message
        session: Database session
        current_user: Current authenticated user
        
    Returns:
        ChatResponse: AI response with conversation ID and metadata
    """
    start_time = time.time()
    message_text = request.message
    conversation_id = request.conversation_id
    response_type = request.response_type
    
    logger.info(f"Processing chat request: '{message_text[:50]}...' (user: {current_user.email}, conv: {conversation_id})")
    
    try:
        # Step 1: Get or create conversation
        if conversation_id:
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
        else:
            # Create new conversation with first message as title
            title = message_text[:50] + "..." if len(message_text) > 50 else message_text
            conversation = Conversation(
                title=title,
                user_id=current_user.id
            )
            session.add(conversation)
            session.commit()
            session.refresh(conversation)
            conversation_id = conversation.id
            logger.info(f"Created new conversation {conversation_id} for user {current_user.email}")
        
        # Step 2: Save user message
        user_message = Message(
            conversation_id=conversation_id,
            role="user",
            content=message_text
        )
        session.add(user_message)
        session.commit()
        
        # Step 3: Safety validation
        validation_result = safety_validator.validate_query(message_text)
        
        if not validation_result["is_valid"]:
            error_msg = validation_result.get("reason", "Query validation failed")
            logger.warning(f"Query validation failed: {error_msg}")
            raise ValueError(error_msg)
        
        # Check for emergency
        if validation_result.get("is_emergency"):
            logger.critical(f"EMERGENCY DETECTED in query: {message_text}")
            raise EmergencyDetectedError(
                emergency_type=validation_result.get("emergency_type", "unknown"),
                query=message_text
            )
        
        # Check for harmful content
        if validation_result.get("is_harmful"):
            logger.warning(f"Harmful query blocked: {message_text}")
            raise HarmfulQueryError(query=message_text)
        
        # Step 4: Handle greetings
        if validation_result.get("is_greeting"):
            logger.info(f"Greeting detected: {message_text}")
            answer = (
                "Hello! I'm your AI medical assistant. I'm here to help answer your health and medical questions. "
                "You can ask me about:\n\n"
                "• Symptoms and conditions\n"
                "• Treatment options\n"
                "• General health information\n"
                "• Preventive care\n"
                "• Medication information\n\n"
                "What would you like to know about today?"
            )
            source_docs = []
            analysis = {
                "confidence": 1.0,
                "confidence_label": "high"
            }
        else:
            # Step 5: Process query through RAG
            logger.debug(f"Processing query through RAG pipeline (conv: {conversation_id})")
            from ...services.rag_service import process_query_with_session
            result = process_query_with_session(message_text, str(conversation_id))
            
            answer = result.get("answer", "")
            source_docs = result.get("source_documents", [])
            
            # Step 6: Analyze response
            analysis = response_analyzer.analyze_response(result)
        
        # Step 7: Format sources
        formatted_sources = []
        for doc in source_docs:
            formatted_sources.append(
                SourceDocument(
                    content=doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                    page=doc.metadata.get("page"),
                    metadata=doc.metadata
                )
            )
        
        # Step 8: Calculate metrics
        response_time = time.time() - start_time
        
        # Step 9: Save assistant message with metadata
        assistant_message = Message(
            conversation_id=conversation_id,
            role="assistant",
            content=answer,
            query_type="greeting" if validation_result.get("is_greeting") else "medical_query",
            elapsed_time=response_time,
            docs_retrieved=len(source_docs)
        )
        session.add(assistant_message)
        session.commit()
        
        # Step 10: Record metrics
        metrics.record_query(
            success=True,
            response_time=response_time,
            confidence=analysis["confidence"]
        )
        
        # Step 11: Add disclaimer if needed
        disclaimer = None
        if validation_result.get("needs_disclaimer"):
            disclaimer = safety_validator.add_disclaimer(answer)
        
        # Build response
        query_type = "greeting" if validation_result.get("is_greeting") else "medical_query"
        response = ChatResponse(
            status=ResponseStatus.SUCCESS,
            response=answer,
            conversation_id=conversation_id,
            metadata={
                "query_type": query_type,
                "elapsed_time": response_time,
                "docs_retrieved": len(source_docs)
            },
            sources=formatted_sources,
            confidence=analysis["confidence_label"],
            confidence_score=analysis["confidence"],
            response_time=response_time,
            timestamp=datetime.now(),
            disclaimer=disclaimer
        )
        
        logger.info(
            f"Chat request completed: conv={conversation_id}, confidence={analysis['confidence']:.2f}, "
            f"sources={len(formatted_sources)}, time={response_time:.2f}s"
        )
        
        return response
        
    except (EmergencyDetectedError, HarmfulQueryError) as e:
        # Safety exceptions - record but re-raise for middleware
        metrics.record_query(
            success=False,
            response_time=time.time() - start_time,
            is_emergency=isinstance(e, EmergencyDetectedError)
        )
        raise
        
    except Exception as e:
        # Record failure
        response_time = time.time() - start_time
        metrics.record_query(
            success=False,
            response_time=response_time
        )
        logger.error(f"Chat request failed: {e}")
        raise


@router.get("/history", response_model=HistoryResponse)
async def get_history(
    session_id: Optional[str] = None,
    memory_manager = Depends(get_memory_service)
):
    """
    Get conversation history
    
    Args:
        session_id: Optional session ID
        
    Returns:
        HistoryResponse: Conversation history
    """
    logger.info(f"Retrieving conversation history (session: {session_id})")
    
    try:
        # Get session-specific memory
        session_memory = memory_manager.get_memory(session_id)
        memory_vars = session_memory.load_memory_variables({})
        chat_history = memory_vars.get("chat_history", [])
        
        # Parse history into messages
        messages = []
        if chat_history:
            # Handle list of message objects (return_messages=True)
            if isinstance(chat_history, list):
                for msg in chat_history:
                    # LangChain message objects have 'type' and 'content' attributes
                    role = "human" if msg.type == "human" else "ai"
                    messages.append(
                        ConversationMessage(
                            role=role,
                            content=msg.content,
                            timestamp=datetime.now()
                        )
                    )
            # Handle string format (return_messages=False)
            elif isinstance(chat_history, str):
                # Split by common patterns
                parts = chat_history.split("\n")
                current_role = None
                current_content = []
                
                for part in parts:
                    part = part.strip()
                    if not part:
                        continue
                    
                    if part.lower().startswith(("human:", "user:")):
                        if current_role and current_content:
                            messages.append(
                                ConversationMessage(
                                    role=current_role,
                                    content=" ".join(current_content),
                                    timestamp=datetime.now()
                                )
                            )
                        current_role = "human"
                        current_content = [part.split(":", 1)[1].strip()]
                        
                    elif part.lower().startswith(("ai:", "assistant:", "bot:")):
                        if current_role and current_content:
                            messages.append(
                                ConversationMessage(
                                    role=current_role,
                                    content=" ".join(current_content),
                                    timestamp=datetime.now()
                                )
                            )
                        current_role = "ai"
                        current_content = [part.split(":", 1)[1].strip()]
                        
                    else:
                        if current_content:
                            current_content.append(part)
                
                # Add last message
                if current_role and current_content:
                    messages.append(
                        ConversationMessage(
                            role=current_role,
                            content=" ".join(current_content),
                            timestamp=datetime.now()
                        )
                    )
        
        response = HistoryResponse(
            status=ResponseStatus.SUCCESS,
            messages=messages,
            session_id=session_id,
            total_messages=len(messages)
        )
        
        logger.info(f"Retrieved {len(messages)} messages from history")
        return response
        
    except Exception as e:
        logger.error(f"Failed to retrieve history: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve history: {str(e)}"
        )


@router.post("/reset", response_model=SuccessResponse)
async def reset_conversation(
    request: ResetRequest,
    memory_manager = Depends(get_memory_service)
):
    """
    Reset conversation memory
    
    Args:
        request: ResetRequest with optional session ID
        
    Returns:
        SuccessResponse: Confirmation message
    """
    session_id = request.session_id
    
    if not request.confirm:
        raise ValueError("Reset must be confirmed with confirm=true")
    
    logger.info(f"Resetting conversation memory (session: {session_id})")
    
    try:
        # Clear session-specific memory
        memory_manager.clear_memory(session_id)
        
        response = SuccessResponse(
            status=ResponseStatus.SUCCESS,
            message="Conversation history has been reset",
            data={"session_id": session_id} if session_id else None,
            timestamp=datetime.now()
        )
        
        logger.info("Conversation memory reset successfully")
        return response
        
    except Exception as e:
        logger.error(f"Failed to reset memory: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to reset conversation: {str(e)}"
        )


@router.post("/export")
async def export_conversation(
    request: ExportRequest,
    memory_manager = Depends(get_memory_service)
):
    """
    Export conversation history
    
    Args:
        request: ExportRequest with format specification
        
    Returns:
        Conversation history in requested format
    """
    session_id = request.session_id
    export_format = request.format
    
    logger.info(f"Exporting conversation (session: {session_id}, format: {export_format})")
    
    try:
        if export_format == "json":
            # Get structured history
            history_response = await get_history(session_id, memory_manager)
            return {
                "format": "json",
                "session_id": session_id,
                "messages": [msg.model_dump() for msg in history_response.messages],
                "exported_at": datetime.now().isoformat()
            }
        
        elif export_format == "txt":
            # Get structured history first
            history_response = await get_history(session_id, memory_manager)
            
            # Convert messages to plain text
            content = ""
            for msg in history_response.messages:
                role = "Human" if msg.role == "human" else "AI"
                content += f"{role}: {msg.content}\n\n"
            
            if not content:
                content = "No conversation history"
            
            return {
                "format": "txt",
                "session_id": session_id,
                "content": content.strip(),
                "exported_at": datetime.now().isoformat()
            }
        
        else:
            raise ValueError(f"Unsupported export format: {export_format}")
            
    except Exception as e:
        logger.error(f"Failed to export conversation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export conversation: {str(e)}"
        )


@router.get("/status")
async def chat_status():
    """
    Get chat service status
    
    Returns:
        dict: Chat service status
    """
    try:
        # Try to access RAG service
        rag_service = get_rag_service()
        memory_service = get_memory_service()
        
        return {
            "status": "operational",
            "rag_service": "available",
            "memory_service": "available",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.warning(f"Chat service status check failed: {e}")
        return {
            "status": "degraded",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
