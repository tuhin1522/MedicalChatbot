"""
Medical Chatbot API Server
Main entry point for running the FastAPI application
"""

import uvicorn
from src.api import app
from src.core import logger, config


def main():
    """
    Start the FastAPI server
    """
    logger.info("="*60)
    logger.info("Medical Chatbot API Server")
    logger.info("="*60)
    logger.info(f"LLM Model: {config.LLM_MODEL}")
    logger.info(f"Embedding Model: {config.EMBEDDING_MODEL}")
    logger.info(f"Memory Window: {config.MEMORY_WINDOW_SIZE} messages")
    logger.info("="*60)
    
    # Run server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        access_log=True
    )


if __name__ == "__main__":
    main()
