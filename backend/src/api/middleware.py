"""
Middleware for Medical Chatbot API
Error handling, logging, and request/response processing
"""

import time
import traceback
from typing import Callable, Optional
from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from ..core import logger
from ..core.exceptions import (
    ChatbotException,
    ModelNotFoundError,
    ServiceInitializationError,
    VectorStoreError,
    QueryValidationError,
    EmergencyDetectedError,
    HarmfulQueryError,
    ConfigurationError
)
from .models.response import ErrorResponse, ResponseStatus


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """
    Middleware for handling exceptions and converting them to proper HTTP responses
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process request and handle any exceptions
        
        Args:
            request: FastAPI request
            call_next: Next middleware/route handler
            
        Returns:
            Response: HTTP response
        """
        try:
            response = await call_next(request)
            return response
            
        except QueryValidationError as e:
            logger.warning(f"Query validation error: {e.message}")
            return self._create_error_response(
                error_message=e.message,
                error_type="QueryValidationError",
                status_code=status.HTTP_400_BAD_REQUEST,
                details={"suggestions": e.suggestions}
            )
        
        except EmergencyDetectedError as e:
            logger.critical(f"EMERGENCY DETECTED: {e.message} - Type: {e.emergency_type}")
            return self._create_error_response(
                error_message=e.message,
                error_type="EmergencyDetected",
                status_code=status.HTTP_200_OK,  # 200 to ensure emergency message is delivered
                details={
                    "emergency_type": e.emergency_type,
                    "emergency_contacts": e.emergency_contacts,
                    "is_emergency": True
                }
            )
        
        except HarmfulQueryError as e:
            logger.warning(f"Harmful query blocked: {e.message}")
            return self._create_error_response(
                error_message=e.message,
                error_type="HarmfulQueryError",
                status_code=status.HTTP_403_FORBIDDEN,
                details={"reason": e.reason}
            )
        
        except ModelNotFoundError as e:
            logger.error(f"Model not found: {e.message}")
            return self._create_error_response(
                error_message=e.message,
                error_type="ModelNotFoundError",
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                details={"install_command": e.install_command}
            )
        
        except ServiceInitializationError as e:
            logger.error(f"Service initialization error: {e.message}")
            return self._create_error_response(
                error_message=e.message,
                error_type="ServiceInitializationError",
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                details={
                    "service_name": e.service_name,
                    "resolution": e.resolution
                }
            )
        
        except VectorStoreError as e:
            logger.error(f"Vector store error: {e.message}")
            return self._create_error_response(
                error_message=e.message,
                error_type="VectorStoreError",
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                details={"operation": e.operation}
            )
        
        except ConfigurationError as e:
            logger.error(f"Configuration error: {e.message}")
            return self._create_error_response(
                error_message=e.message,
                error_type="ConfigurationError",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                details={"config_key": e.config_key}
            )
        
        except ChatbotException as e:
            logger.error(f"Chatbot error: {e.message}")
            return self._create_error_response(
                error_message=e.message,
                error_type=e.__class__.__name__,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        except ValueError as e:
            logger.warning(f"Validation error: {str(e)}")
            return self._create_error_response(
                error_message=str(e),
                error_type="ValidationError",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}\n{traceback.format_exc()}")
            return self._create_error_response(
                error_message="An unexpected error occurred",
                error_type="InternalServerError",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                details={"error": str(e)} if logger.level <= 10 else None  # Only in debug mode
            )
    
    def _create_error_response(
        self,
        error_message: str,
        error_type: str,
        status_code: int,
        details: Optional[dict] = None
    ) -> JSONResponse:
        """
        Create a standardized error response
        
        Args:
            error_message: Error message
            error_type: Type of error
            status_code: HTTP status code
            details: Additional error details
            
        Returns:
            JSONResponse: Formatted error response
        """
        error_response = ErrorResponse(
            status=ResponseStatus.ERROR,
            error=error_message,
            error_type=error_type,
            details=details
        )
        
        return JSONResponse(
            status_code=status_code,
            content=error_response.model_dump(mode='json')
        )


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for logging all requests and responses
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Log request and response information
        
        Args:
            request: FastAPI request
            call_next: Next middleware/route handler
            
        Returns:
            Response: HTTP response
        """
        # Generate request ID
        request_id = self._generate_request_id()
        
        # Log request
        logger.info(
            f"[{request_id}] {request.method} {request.url.path} "
            f"from {request.client.host if request.client else 'unknown'}"
        )
        
        # Record start time
        start_time = time.time()
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Log response
        logger.info(
            f"[{request_id}] Response: {response.status_code} "
            f"in {duration:.3f}s"
        )
        
        # Add custom headers
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Response-Time"] = f"{duration:.3f}s"
        
        return response
    
    def _generate_request_id(self) -> str:
        """
        Generate a unique request ID
        
        Returns:
            str: Request ID
        """
        import uuid
        return str(uuid.uuid4())[:8]


class CORSMiddleware:
    """
    CORS middleware configuration
    Note: Use FastAPI's built-in CORSMiddleware in practice
    This is for documentation purposes
    """
    
    @staticmethod
    def get_cors_config():
        """
        Get CORS configuration
        
        Returns:
            dict: CORS configuration
        """
        return {
            "allow_origins": ["*"],  # In production, specify exact origins
            "allow_credentials": True,
            "allow_methods": ["*"],
            "allow_headers": ["*"],
        }


def setup_middleware(app):
    """
    Setup all middleware for the FastAPI app
    
    Args:
        app: FastAPI application instance
    """
    # Add CORS middleware (should be first)
    from fastapi.middleware.cors import CORSMiddleware as FastAPICORS
    app.add_middleware(
        FastAPICORS,
        **CORSMiddleware.get_cors_config()
    )
    
    # Add logging middleware
    app.add_middleware(LoggingMiddleware)
    
    # Add error handler middleware (should be last)
    app.add_middleware(ErrorHandlerMiddleware)
    
    logger.info("Middleware configured successfully")
