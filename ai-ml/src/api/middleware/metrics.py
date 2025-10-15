"""
Metrics Middleware
Request metrics collection and performance monitoring
"""

import time
import logging
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware for collecting request metrics"""
    
    def __init__(self, app, collect_metrics: bool = True):
        super().__init__(app)
        self.collect_metrics = collect_metrics
        self._request_count = 0
        self._total_processing_time = 0.0
        self._error_count = 0
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if not self.collect_metrics:
            return await call_next(request)
        
        # Increment request count
        self._request_count += 1
        
        # Record start time
        start_time = time.time()
        
        try:
            response = await call_next(request)
            processing_time = time.time() - start_time
            
            # Update metrics
            self._total_processing_time += processing_time
            if response.status_code >= 400:
                self._error_count += 1
            
            # Add metrics to response headers
            response.headers["X-Processing-Time"] = str(processing_time)
            response.headers["X-Request-Count"] = str(self._request_count)
            
            # Log metrics
            await self._log_metrics(request, response, processing_time)
            
            return response
            
        except Exception as e:
            processing_time = time.time() - start_time
            self._error_count += 1
            self._total_processing_time += processing_time
            
            logger.error(f"Request failed in metrics middleware: {e}")
            raise
    
    async def _log_metrics(self, request: Request, response: Response, processing_time: float):
        """Log request metrics"""
        metrics = {
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "processing_time": processing_time,
            "total_requests": self._request_count,
            "total_processing_time": self._total_processing_time,
            "error_count": self._error_count,
            "average_processing_time": (
                self._total_processing_time / self._request_count 
                if self._request_count > 0 else 0
            )
        }
        
        logger.info(f"Request metrics: {metrics}")
    
    def get_metrics(self) -> dict:
        """Get current metrics"""
        return {
            "total_requests": self._request_count,
            "total_processing_time": self._total_processing_time,
            "error_count": self._error_count,
            "average_processing_time": (
                self._total_processing_time / self._request_count 
                if self._request_count > 0 else 0
            ),
            "error_rate": (
                self._error_count / self._request_count 
                if self._request_count > 0 else 0
            )
        }
    
    def reset_metrics(self):
        """Reset metrics counters"""
        self._request_count = 0
        self._total_processing_time = 0.0
        self._error_count = 0
