"""
Error Handler Middleware
Global error handling and response formatting
"""

import logging
import traceback
from typing import Callable
from fastapi import Request, Response, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Middleware for global error handling"""
    
    def __init__(self, app, include_traceback: bool = False):
        super().__init__(app)
        self.include_traceback = include_traceback
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            return await call_next(request)
            
        except HTTPException as e:
            # Handle FastAPI HTTP exceptions
            return self._handle_http_exception(request, e)
            
        except Exception as e:
            # Handle unexpected exceptions
            return self._handle_unexpected_exception(request, e)
    
    def _handle_http_exception(self, request: Request, exc: HTTPException) -> JSONResponse:
        """Handle HTTP exceptions"""
        correlation_id = getattr(request.state, "correlation_id", "unknown")
        
        logger.warning(
            f"HTTP exception - {request.method} {request.url.path} - "
            f"Status: {exc.status_code} - Detail: {exc.detail} - "
            f"Correlation ID: {correlation_id}"
        )
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "HTTP Error",
                "message": exc.detail,
                "status_code": exc.status_code,
                "correlation_id": correlation_id,
                "path": request.url.path,
                "method": request.method
            }
        )
    
    def _handle_unexpected_exception(self, request: Request, exc: Exception) -> JSONResponse:
        """Handle unexpected exceptions"""
        correlation_id = getattr(request.state, "correlation_id", "unknown")
        
        # Log the full exception
        logger.error(
            f"Unexpected exception - {request.method} {request.url.path} - "
            f"Error: {str(exc)} - Correlation ID: {correlation_id}",
            exc_info=True
        )
        
        # Prepare error response
        error_response = {
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "status_code": 500,
            "correlation_id": correlation_id,
            "path": request.url.path,
            "method": request.method
        }
        
        # Include traceback in development mode
        if self.include_traceback:
            error_response["traceback"] = traceback.format_exc()
        
        return JSONResponse(
            status_code=500,
            content=error_response
        )
