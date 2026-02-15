"""
Health Check Routes for Medical Chatbot API
Endpoints for monitoring service status and availability
"""

from fastapi import APIRouter, Depends
from datetime import datetime

from ...core import config, logger
from ..dependencies import (
    get_chatbot_config,
    verify_ollama_models,
    get_vectorstore_service,
    get_start_time
)
from ..models.response import HealthResponse, ResponseStatus


router = APIRouter(
    prefix="/health",
    tags=["Health"]
)


@router.get("", response_model=HealthResponse)
@router.get("/", response_model=HealthResponse)
async def health_check(
    cfg = Depends(get_chatbot_config)
):
    """
    Health check endpoint
    
    Returns comprehensive status of all services:
    - Ollama service status
    - Model availability
    - Vector database status
    - Configuration
    
    Returns:
        HealthResponse: Service health status
    """
    logger.info("Health check requested")
    
    try:
        # Verify Ollama models
        ollama_status = verify_ollama_models()
        
        # Check vector database
        try:
            vectordb = get_vectorstore_service()
            db_status = "connected"
            logger.debug("Vector database connection verified")
        except Exception as e:
            db_status = f"unavailable: {str(e)}"
            logger.warning(f"Vector database check failed: {e}")
        
        response = HealthResponse(
            status=ResponseStatus.SUCCESS,
            ollama_status=ollama_status["status"],
            llm_model=ollama_status["llm_model"],
            embedding_model=ollama_status["embedding_model"],
            database_status=db_status,
            memory_window=cfg.MEMORY_WINDOW_SIZE,
            timestamp=datetime.now()
        )
        
        logger.info("Health check passed")
        return response
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        # Return partial health info
        return HealthResponse(
            status=ResponseStatus.ERROR,
            ollama_status="error",
            llm_model=cfg.LLM_MODEL,
            embedding_model=cfg.EMBEDDING_MODEL,
            database_status="error",
            memory_window=cfg.MEMORY_WINDOW_SIZE,
            timestamp=datetime.now()
        )


@router.get("/ping")
async def ping():
    """
    Simple ping endpoint for basic availability check
    
    Returns:
        dict: Ping response
    """
    return {
        "status": "ok",
        "message": "pong",
        "timestamp": datetime.now().isoformat()
    }


@router.get("/version")
async def version(cfg = Depends(get_chatbot_config)):
    """
    Get service version and configuration information
    
    Returns:
        dict: Version information
    """
    return {
        "service": "Medical Chatbot API",
        "version": "1.0.0",
        "llm_model": cfg.LLM_MODEL,
        "embedding_model": cfg.EMBEDDING_MODEL,
        "memory_window": cfg.MEMORY_WINDOW_SIZE,
        "retrieval_k": cfg.RETRIEVAL_K,
        "timestamp": datetime.now().isoformat()
    }


@router.get("/uptime")
async def uptime():
    """
    Get service uptime
    
    Returns:
        dict: Uptime information
    """
    import time
    start_time = get_start_time()
    current_time = time.time()
    uptime_seconds = current_time - start_time
    
    # Convert to human-readable format
    days = int(uptime_seconds // 86400)
    hours = int((uptime_seconds % 86400) // 3600)
    minutes = int((uptime_seconds % 3600) // 60)
    seconds = int(uptime_seconds % 60)
    
    return {
        "uptime_seconds": uptime_seconds,
        "uptime_formatted": f"{days}d {hours}h {minutes}m {seconds}s",
        "start_time": datetime.fromtimestamp(start_time).isoformat(),
        "current_time": datetime.fromtimestamp(current_time).isoformat()
    }
