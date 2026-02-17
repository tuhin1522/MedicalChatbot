"""
Admin Routes for Medical Chatbot API
Administrative endpoints for system management and monitoring
"""

import shutil
from pathlib import Path
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from datetime import datetime

from ...core import logger, config
from ...core.exceptions import VectorStoreError
from ..dependencies import (
    get_performance_metrics,
    get_vectorstore_service,
    get_memory_service,
    get_start_time
)
from ..models.response import (
    MetricsResponse,
    SuccessResponse,
    ResponseStatus
)


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/metrics", response_model=MetricsResponse)
async def get_metrics(
    metrics = Depends(get_performance_metrics)
):
    """
    Get performance metrics
    
    Returns detailed performance statistics:
    - Total queries processed
    - Success/failure counts
    - Average response time
    - Average confidence score
    - Service uptime
    
    Returns:
        MetricsResponse: Performance metrics
    """
    logger.info("Retrieving performance metrics")
    
    try:
        # Get metrics summary
        summary = metrics.get_summary()
        
        # Get uptime
        import time
        start_time = get_start_time()
        uptime = time.time() - start_time
        
        response = MetricsResponse(
            status=ResponseStatus.SUCCESS,
            total_queries=summary["total_queries"],
            successful_queries=summary["successful_queries"],
            failed_queries=summary["failed_queries"],
            average_response_time=summary["average_response_time"],
            average_confidence=summary["average_confidence_score"],
            uptime=uptime,
            timestamp=datetime.now()
        )
        
        logger.info(f"Metrics retrieved: {summary['total_queries']} total queries")
        return response
        
    except Exception as e:
        logger.error(f"Failed to retrieve metrics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve metrics: {str(e)}"
        )


@router.post("/metrics/reset", response_model=SuccessResponse)
async def reset_metrics(
    confirm: bool = Query(False, description="Confirmation flag"),
    metrics = Depends(get_performance_metrics)
):
    """
    Reset performance metrics
    
    Args:
        confirm: Must be true to confirm reset
        
    Returns:
        SuccessResponse: Confirmation message
    """
    if not confirm:
        raise ValueError("Metrics reset must be confirmed with confirm=true")
    
    logger.warning("Resetting performance metrics")
    
    try:
        metrics.reset()
        
        response = SuccessResponse(
            status=ResponseStatus.SUCCESS,
            message="Performance metrics have been reset",
            timestamp=datetime.now()
        )
        
        logger.info("Performance metrics reset successfully")
        return response
        
    except Exception as e:
        logger.error(f"Failed to reset metrics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to reset metrics: {str(e)}"
        )


@router.get("/metrics/export")
async def export_metrics(
    format: str = Query("json", description="Export format (json/txt)"),
    metrics = Depends(get_performance_metrics)
):
    """
    Export performance metrics
    
    Args:
        format: Export format (json or txt)
        
    Returns:
        Metrics in requested format
    """
    logger.info(f"Exporting metrics in {format} format")
    
    try:
        if format.lower() == "json":
            return {
                **metrics.get_summary(),
                "exported_at": datetime.now().isoformat()
            }
            
        elif format.lower() == "txt":
            text_content = metrics.get_summary("text")
            text_lines = [
                "Performance Metrics Report",
                "=" * 50,
                f"Generated: {datetime.now().isoformat()}",
                "",
                text_content,
                "",
                "=" * 50
            ]
            
            return {
                "format": "txt",
                "content": "\n".join(text_lines),
                "exported_at": datetime.now().isoformat()
            }
            
        else:
            raise ValueError(f"Unsupported format: {format}")
            
    except Exception as e:
        logger.error(f"Failed to export metrics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export metrics: {str(e)}"
        )


@router.post("/clear-db", response_model=SuccessResponse)
async def clear_vector_database(
    confirm: bool = Query(False, description="Confirmation flag")
):
    """
    Clear the vector database
    
    WARNING: This will delete all indexed documents!
    
    Args:
        confirm: Must be true to confirm deletion
        
    Returns:
        SuccessResponse: Confirmation message
    """
    if not confirm:
        raise ValueError("Database clearing must be confirmed with confirm=true")
    
    logger.warning("Clearing vector database")
    
    try:
        # Path to database
        db_path = Path(config.VECTOR_STORE_PATH)
        
        if not db_path.exists():
            logger.info("Vector database does not exist")
            return SuccessResponse(
                status=ResponseStatus.SUCCESS,
                message="Vector database does not exist (nothing to clear)",
                timestamp=datetime.now()
            )
        
        # Remove database directory
        shutil.rmtree(db_path)
        logger.warning(f"Vector database cleared: {db_path}")
        
        response = SuccessResponse(
            status=ResponseStatus.SUCCESS,
            message="Vector database has been cleared",
            data={"cleared_path": str(db_path)},
            timestamp=datetime.now()
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Failed to clear vector database: {e}")
        raise VectorStoreError(
            message=f"Failed to clear vector database: {str(e)}",
            operation="clear"
        )


@router.post("/rebuild-db", response_model=SuccessResponse)
async def rebuild_vector_database(
    confirm: bool = Query(False, description="Confirmation flag")
):
    """
    Rebuild the vector database from source documents
    
    This will:
    1. Clear existing database
    2. Reload documents from data directory
    3. Create new embeddings
    4. Build new vector store
    
    Args:
        confirm: Must be true to confirm rebuild
        
    Returns:
        SuccessResponse: Confirmation message with status
    """
    if not confirm:
        raise ValueError("Database rebuild must be confirmed with confirm=true")
    
    logger.warning("Rebuilding vector database")
    
    try:
        # Import services (lazy load)
        from ...services.document_service import load_pdf, text_split
        from ...services.embedding_service import embeddings
        from langchain_chroma import Chroma
        
        # Step 1: Clear existing database
        db_path = Path(config.VECTOR_STORE_PATH)
        if db_path.exists():
            shutil.rmtree(db_path)
            logger.info("Existing database cleared")
        
        # Step 2: Load documents
        data_path = Path(config.DATA_PATH)
        if not data_path.exists() or not list(data_path.glob("*.pdf")):
            raise VectorStoreError(
                message="No PDF files found in data directory",
                operation="rebuild"
            )
        
        logger.info(f"Loading documents from {data_path}")
        docs = load_pdf(str(data_path))
        
        if not docs:
            raise VectorStoreError(
                message="No documents loaded",
                operation="rebuild"
            )
        
        logger.info(f"Loaded {len(docs)} documents")
        
        # Step 3: Split documents
        logger.info("Splitting documents into chunks")
        chunks = text_split(docs)
        logger.info(f"Created {len(chunks)} text chunks")
        
        # Step 4: Create vector store
        logger.info("Creating vector store with embeddings")
        vectordb = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=str(db_path)
        )
        
        logger.warning(f"Vector database rebuilt successfully: {len(chunks)} chunks indexed")
        
        response = SuccessResponse(
            status=ResponseStatus.SUCCESS,
            message="Vector database has been rebuilt",
            data={
                "documents_loaded": len(docs),
                "chunks_created": len(chunks),
                "database_path": str(db_path)
            },
            timestamp=datetime.now()
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Failed to rebuild vector database: {e}")
        raise VectorStoreError(
            message=f"Failed to rebuild vector database: {str(e)}",
            operation="rebuild"
        )


@router.get("/database/info")
async def get_database_info():
    """
    Get vector database information
    
    Returns:
        dict: Database information
    """
    logger.info("Retrieving database information")
    
    try:
        db_path = Path(config.VECTOR_STORE_PATH)
        
        if not db_path.exists():
            return {
                "status": "not_initialized",
                "exists": False,
                "path": str(db_path),
                "message": "Vector database has not been created yet"
            }
        
        # Get database size
        total_size = sum(f.stat().st_size for f in db_path.rglob('*') if f.is_file())
        size_mb = total_size / (1024 * 1024)
        
        # Try to get collection info
        try:
            vectordb = get_vectorstore_service()
            collection = vectordb._collection
            count = collection.count()
        except Exception as e:
            logger.warning(f"Could not get collection count: {e}")
            count = None
        
        return {
            "status": "initialized",
            "exists": True,
            "path": str(db_path),
            "size_mb": round(size_mb, 2),
            "document_count": count,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to retrieve database info: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve database info: {str(e)}"
        )


@router.post("/memory/clear", response_model=SuccessResponse)
async def clear_memory(
    confirm: bool = Query(False, description="Confirmation flag"),
    memory_service = Depends(get_memory_service)
):
    """
    Clear conversation memory for all sessions
    
    Args:
        confirm: Must be true to confirm clearing
        
    Returns:
        SuccessResponse: Confirmation message
    """
    if not confirm:
        raise ValueError("Memory clearing must be confirmed with confirm=true")
    
    logger.warning("Clearing all conversation memory")
    
    try:
        memory_service.clear()
        
        response = SuccessResponse(
            status=ResponseStatus.SUCCESS,
            message="All conversation memory has been cleared",
            timestamp=datetime.now()
        )
        
        logger.info("Conversation memory cleared successfully")
        return response
        
    except Exception as e:
        logger.error(f"Failed to clear memory: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear memory: {str(e)}"
        )


@router.get("/logs")
async def get_logs(
    lines: int = Query(50, ge=1, le=1000, description="Number of lines to retrieve"),
    level: Optional[str] = Query(None, description="Filter by log level (INFO, WARNING, ERROR)")
):
    """
    Retrieve recent log entries
    
    Args:
        lines: Number of log lines to retrieve
        level: Optional log level filter
        
    Returns:
        dict: Log entries
    """
    logger.info(f"Retrieving {lines} log lines")
    
    try:
        from datetime import date
        
        # Get current log file
        log_filename = f"chatbot_{date.today().strftime('%Y%m%d')}.log"
        log_path = Path(config.LOG_DIR) / log_filename
        
        if not log_path.exists():
            return {
                "status": "not_found",
                "message": f"Log file not found: {log_filename}",
                "timestamp": datetime.now().isoformat()
            }
        
        # Read last N lines
        with open(log_path, 'r') as f:
            all_lines = f.readlines()
        
        # Get last N lines
        recent_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
        
        # Filter by level if specified
        if level:
            level_upper = level.upper()
            recent_lines = [line for line in recent_lines if level_upper in line]
        
        return {
            "status": "success",
            "log_file": log_filename,
            "total_lines": len(all_lines),
            "returned_lines": len(recent_lines),
            "logs": recent_lines,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to retrieve logs: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve logs: {str(e)}"
        )
