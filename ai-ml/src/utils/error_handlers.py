"""
Error Handlers
Comprehensive error handling for API-specific errors, retries, and circuit breakers
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Callable, Optional, List
from dataclasses import dataclass
from enum import Enum
import time

logger = logging.getLogger(__name__)


class ErrorType(Enum):
    """Types of errors that can occur"""
    NETWORK_ERROR = "network_error"
    AUTHENTICATION_ERROR = "authentication_error"
    RATE_LIMIT_ERROR = "rate_limit_error"
    VALIDATION_ERROR = "validation_error"
    SERVER_ERROR = "server_error"
    TIMEOUT_ERROR = "timeout_error"
    GRAPHQL_ERROR = "graphql_error"
    OAUTH_ERROR = "oauth_error"
    UNKNOWN_ERROR = "unknown_error"


class CircuitState(Enum):
    """Circuit breaker states"""
    CLOSED = "closed"  # Normal operation
    OPEN = "open"      # Circuit is open, failing fast
    HALF_OPEN = "half_open"  # Testing if service is back


@dataclass
class ErrorContext:
    """Context information for error handling"""
    error_type: ErrorType
    error_message: str
    status_code: Optional[int] = None
    retry_count: int = 0
    max_retries: int = 3
    backoff_delay: float = 1.0
    timestamp: datetime = None
    request_id: Optional[str] = None
    endpoint: Optional[str] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class CircuitBreaker:
    """Circuit breaker implementation for API calls"""
    
    def __init__(self, failure_threshold: int = 5, timeout: int = 60, expected_exception: type = Exception):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.expected_exception = expected_exception
        
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
        
    def can_execute(self) -> bool:
        """Check if the circuit breaker allows execution"""
        if self.state == CircuitState.CLOSED:
            return True
        
        if self.state == CircuitState.OPEN:
            if self.last_failure_time and datetime.now() - self.last_failure_time > timedelta(seconds=self.timeout):
                self.state = CircuitState.HALF_OPEN
                return True
            return False
        
        if self.state == CircuitState.HALF_OPEN:
            return True
        
        return False
    
    def record_success(self):
        """Record a successful call"""
        self.failure_count = 0
        self.state = CircuitState.CLOSED
        logger.debug("Circuit breaker: Success recorded, circuit closed")
    
    def record_failure(self):
        """Record a failed call"""
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            logger.warning(f"Circuit breaker: Circuit opened after {self.failure_count} failures")
        else:
            logger.debug(f"Circuit breaker: Failure recorded ({self.failure_count}/{self.failure_threshold})")


class APIErrorHandler:
    """Comprehensive error handling for API calls"""
    
    def __init__(self):
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.error_stats: Dict[str, Dict[str, int]] = {}
    
    def get_circuit_breaker(self, service_name: str) -> CircuitBreaker:
        """Get or create circuit breaker for a service"""
        if service_name not in self.circuit_breakers:
            self.circuit_breakers[service_name] = CircuitBreaker()
        return self.circuit_breakers[service_name]
    
    def classify_error(self, error: Exception, status_code: Optional[int] = None) -> ErrorType:
        """Classify error type based on exception and status code"""
        error_name = type(error).__name__.lower()
        error_message = str(error).lower()
        
        # Network-related errors
        if any(keyword in error_name for keyword in ['connection', 'timeout', 'network', 'socket']):
            return ErrorType.NETWORK_ERROR
        
        # Authentication errors
        if status_code == 401 or 'unauthorized' in error_message or 'authentication' in error_message:
            return ErrorType.AUTHENTICATION_ERROR
        
        # Rate limiting errors
        if status_code == 429 or 'rate limit' in error_message or 'too many requests' in error_message:
            return ErrorType.RATE_LIMIT_ERROR
        
        # Validation errors
        if status_code == 400 or 'validation' in error_message or 'bad request' in error_message:
            return ErrorType.VALIDATION_ERROR
        
        # Server errors
        if status_code and 500 <= status_code < 600:
            return ErrorType.SERVER_ERROR
        
        # GraphQL specific errors
        if 'graphql' in error_name or 'graphql' in error_message:
            return ErrorType.GRAPHQL_ERROR
        
        # OAuth specific errors
        if 'oauth' in error_name or 'oauth' in error_message:
            return ErrorType.OAUTH_ERROR
        
        return ErrorType.UNKNOWN_ERROR
    
    def should_retry(self, error_context: ErrorContext) -> bool:
        """Determine if an error should be retried"""
        # Don't retry if max retries exceeded
        if error_context.retry_count >= error_context.max_retries:
            return False
        
        # Retry for transient errors
        retryable_errors = {
            ErrorType.NETWORK_ERROR,
            ErrorType.RATE_LIMIT_ERROR,
            ErrorType.SERVER_ERROR,
            ErrorType.TIMEOUT_ERROR
        }
        
        return error_context.error_type in retryable_errors
    
    def calculate_backoff_delay(self, error_context: ErrorContext) -> float:
        """Calculate exponential backoff delay"""
        base_delay = error_context.backoff_delay
        
        # Special handling for rate limiting
        if error_context.error_type == ErrorType.RATE_LIMIT_ERROR:
            # Use longer delay for rate limiting
            return base_delay * (2 ** error_context.retry_count) * 2
        
        # Exponential backoff for other errors
        return base_delay * (2 ** error_context.retry_count)
    
    async def with_retry(self, func: Callable, service_name: str, *args, **kwargs) -> Any:
        """Execute function with retry logic and circuit breaker"""
        circuit_breaker = self.get_circuit_breaker(service_name)
        
        # Check circuit breaker
        if not circuit_breaker.can_execute():
            raise Exception(f"Circuit breaker is open for {service_name}")
        
        retry_count = 0
        max_retries = 3
        base_delay = 1.0
        
        while retry_count <= max_retries:
            try:
                # Execute the function
                result = await func(*args, **kwargs)
                
                # Record success
                circuit_breaker.record_success()
                self._record_error_stats(service_name, "success")
                
                return result
                
            except Exception as e:
                # Classify error
                error_type = self.classify_error(e)
                
                # Create error context
                error_context = ErrorContext(
                    error_type=error_type,
                    error_message=str(e),
                    retry_count=retry_count,
                    max_retries=max_retries,
                    backoff_delay=base_delay,
                    endpoint=getattr(e, 'endpoint', None),
                    request_id=getattr(e, 'request_id', None)
                )
                
                # Record error stats
                self._record_error_stats(service_name, error_type.value)
                
                # Check if we should retry
                if not self.should_retry(error_context):
                    circuit_breaker.record_failure()
                    logger.error(f"Non-retryable error in {service_name}: {e}")
                    raise
                
                # Calculate delay and wait
                delay = self.calculate_backoff_delay(error_context)
                logger.warning(f"Retrying {service_name} after {delay}s (attempt {retry_count + 1}/{max_retries + 1}): {e}")
                
                await asyncio.sleep(delay)
                retry_count += 1
        
        # All retries exhausted
        circuit_breaker.record_failure()
        raise Exception(f"Max retries exceeded for {service_name}")
    
    def _record_error_stats(self, service_name: str, error_type: str):
        """Record error statistics"""
        if service_name not in self.error_stats:
            self.error_stats[service_name] = {}
        
        self.error_stats[service_name][error_type] = self.error_stats[service_name].get(error_type, 0) + 1
    
    def get_error_stats(self, service_name: Optional[str] = None) -> Dict[str, Any]:
        """Get error statistics"""
        if service_name:
            return self.error_stats.get(service_name, {})
        return self.error_stats
    
    def reset_error_stats(self, service_name: Optional[str] = None):
        """Reset error statistics"""
        if service_name:
            self.error_stats[service_name] = {}
        else:
            self.error_stats = {}


class GraphQLErrorHandler:
    """Specialized error handler for GraphQL errors"""
    
    @staticmethod
    def handle_graphql_errors(response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Handle GraphQL-specific errors"""
        errors = response.get("errors", [])
        if not errors:
            return []
        
        processed_errors = []
        for error in errors:
            processed_error = {
                "message": error.get("message", "Unknown GraphQL error"),
                "locations": error.get("locations", []),
                "path": error.get("path", []),
                "extensions": error.get("extensions", {}),
                "timestamp": datetime.now().isoformat()
            }
            processed_errors.append(processed_error)
        
        logger.error(f"GraphQL errors: {processed_errors}")
        return processed_errors
    
    @staticmethod
    def is_graphql_error(response: Dict[str, Any]) -> bool:
        """Check if response contains GraphQL errors"""
        return "errors" in response and len(response["errors"]) > 0


class OAuthErrorHandler:
    """Specialized error handler for OAuth errors"""
    
    @staticmethod
    def handle_oauth_errors(response: Dict[str, Any]) -> Dict[str, Any]:
        """Handle OAuth-specific errors"""
        error_code = response.get("error", "")
        error_description = response.get("error_description", "")
        
        processed_error = {
            "error": error_code,
            "error_description": error_description,
            "error_uri": response.get("error_uri", ""),
            "timestamp": datetime.now().isoformat()
        }
        
        # Log specific OAuth errors
        if error_code == "invalid_grant":
            logger.error("OAuth error: Invalid grant - token may be expired or revoked")
        elif error_code == "invalid_client":
            logger.error("OAuth error: Invalid client credentials")
        elif error_code == "invalid_request":
            logger.error("OAuth error: Invalid request parameters")
        elif error_code == "unauthorized_client":
            logger.error("OAuth error: Client not authorized for this grant type")
        elif error_code == "unsupported_grant_type":
            logger.error("OAuth error: Unsupported grant type")
        else:
            logger.error(f"OAuth error: {error_code} - {error_description}")
        
        return processed_error
    
    @staticmethod
    def is_oauth_error(response: Dict[str, Any]) -> bool:
        """Check if response contains OAuth errors"""
        return "error" in response


class RateLimitHandler:
    """Handler for rate limiting scenarios"""
    
    def __init__(self):
        self.rate_limit_info: Dict[str, Dict[str, Any]] = {}
    
    def parse_rate_limit_headers(self, headers: Dict[str, str]) -> Dict[str, Any]:
        """Parse rate limit headers from response"""
        rate_limit_info = {}
        
        # Common rate limit headers
        if "X-RateLimit-Limit" in headers:
            rate_limit_info["limit"] = int(headers["X-RateLimit-Limit"])
        
        if "X-RateLimit-Remaining" in headers:
            rate_limit_info["remaining"] = int(headers["X-RateLimit-Remaining"])
        
        if "X-RateLimit-Reset" in headers:
            rate_limit_info["reset_time"] = int(headers["X-RateLimit-Reset"])
        
        if "X-RateLimit-Retry-After" in headers:
            rate_limit_info["retry_after"] = int(headers["X-RateLimit-Retry-After"])
        
        return rate_limit_info
    
    def calculate_wait_time(self, rate_limit_info: Dict[str, Any]) -> float:
        """Calculate how long to wait before retrying"""
        if "retry_after" in rate_limit_info:
            return float(rate_limit_info["retry_after"])
        
        if "reset_time" in rate_limit_info:
            current_time = time.time()
            wait_time = rate_limit_info["reset_time"] - current_time
            return max(0, wait_time)
        
        # Default exponential backoff
        return 60.0
    
    async def handle_rate_limit(self, service_name: str, rate_limit_info: Dict[str, Any]):
        """Handle rate limiting by waiting appropriate time"""
        wait_time = self.calculate_wait_time(rate_limit_info)
        
        logger.warning(f"Rate limited for {service_name}, waiting {wait_time}s")
        await asyncio.sleep(wait_time)
        
        # Store rate limit info for monitoring
        self.rate_limit_info[service_name] = {
            **rate_limit_info,
            "last_rate_limit": datetime.now().isoformat()
        }


# Global error handler instance
error_handler = APIErrorHandler()
graphql_error_handler = GraphQLErrorHandler()
oauth_error_handler = OAuthErrorHandler()
rate_limit_handler = RateLimitHandler()


def get_error_handler() -> APIErrorHandler:
    """Get the global error handler instance"""
    return error_handler


def get_graphql_error_handler() -> GraphQLErrorHandler:
    """Get the GraphQL error handler instance"""
    return graphql_error_handler


def get_oauth_error_handler() -> OAuthErrorHandler:
    """Get the OAuth error handler instance"""
    return oauth_error_handler


def get_rate_limit_handler() -> RateLimitHandler:
    """Get the rate limit handler instance"""
    return rate_limit_handler
