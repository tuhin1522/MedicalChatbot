"""
Medical Chatbot REST API
FastAPI application for the medical chatbot backend
"""

from fastapi import FastAPI

from .routes import health_router, chat_router, admin_router
from .middleware import setup_middleware
from ..core import logger

__version__ = "1.0.0"


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application
    
    Returns:
        FastAPI: Configured application instance
    """
    app = FastAPI(
        title="Medical Chatbot API",
        description="REST API for AI-powered medical information chatbot using RAG",
        version=__version__,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )
    
    # Setup middleware
    setup_middleware(app)
    
    # Include routers
    app.include_router(health_router)
    app.include_router(chat_router)
    app.include_router(admin_router)
    
    # Root endpoint
    @app.get("/", tags=["Root"])
    async def root():
        """Root endpoint with API information"""
        return {
            "service": "Medical Chatbot API",
            "version": __version__,
            "status": "operational",
            "endpoints": {
                "docs": "/docs",
                "health": "/health",
                "chat": "/chat",
                "admin": "/admin"
            }
        }
    
    # Startup event
    @app.on_event("startup")
    async def startup_event():
        """Initialize services on startup"""
        logger.info(f"Starting Medical Chatbot API v{__version__}")
        logger.info("API documentation available at /docs")
    
    # Shutdown event
    @app.on_event("shutdown")
    async def shutdown_event():
        """Cleanup on shutdown"""
        logger.info("Shutting down Medical Chatbot API")
    
    return app


# Create app instance
app = create_app()


__all__ = [
    "app",
    "create_app",
    "__version__"
]
