"""
Logging Middleware
Request/response logging and correlation ID management
"""

import logging
import time
import uuid
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from config import settings

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for request/response logging"""
    
    def __init__(self, app, log_requests: bool = True, log_responses: bool = True):
        super().__init__(app)
        self.log_requests = log_requests
        self.log_responses = log_responses
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Generate correlation ID
        correlation_id = str(uuid.uuid4())
        request.state.correlation_id = correlation_id
        
        # Log request
        if self.log_requests:
            await self._log_request(request, correlation_id)
        
        # Process request
        start_time = time.time()
        try:
            response = await call_next(request)
            processing_time = time.time() - start_time
            
            # Log response
            if self.log_responses:
                await self._log_response(request, response, processing_time, correlation_id)
            
            # Add correlation ID to response headers
            response.headers["X-Correlation-ID"] = correlation_id
            
            return response
            
        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(
                f"Request failed - {request.method} {request.url.path} - "
                f"Error: {str(e)} - Time: {processing_time:.3f}s - "
                f"Correlation ID: {correlation_id}"
            )
            raise
    
    async def _log_request(self, request: Request, correlation_id: str):
        """Log incoming request"""
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")
        
        # Get user info if available
        user_info = getattr(request.state, "user", None)
        user_name = user_info.get("name", "anonymous") if user_info else "anonymous"
        
        # Log basic request info
        logger.info(
            f"Request started - {request.method} {request.url.path} - "
            f"Client IP: {client_ip} - User-Agent: {user_agent} - "
            f"User: {user_name} - Correlation ID: {correlation_id}"
        )
        
        # Log request body for POST/PUT requests (in debug mode only)
        if hasattr(settings, 'debug') and settings.debug and request.method in ["POST", "PUT", "PATCH"]:
            try:
                body = await request.body()
                if body:
                    logger.debug(f"Request body: {body.decode('utf-8')[:500]}...")
            except Exception:
                pass  # Ignore if we can't read the body
    
    async def _log_response(self, request: Request, response: Response, 
                          processing_time: float, correlation_id: str):
        """Log outgoing response"""
        status_code = response.status_code
        content_length = response.headers.get("content-length", "unknown")
        
        log_level = logging.INFO
        if status_code >= 400:
            log_level = logging.WARNING
        if status_code >= 500:
            log_level = logging.ERROR
        
        logger.log(
            log_level,
            f"Request completed - {request.method} {request.url.path} - "
            f"Status: {status_code} - Time: {processing_time:.3f}s - "
            f"Size: {content_length} - Correlation ID: {correlation_id}"
        )
