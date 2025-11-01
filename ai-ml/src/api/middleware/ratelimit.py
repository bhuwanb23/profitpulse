"""
Rate Limiting Middleware
Request rate limiting and throttling
"""

import logging
import time
from typing import Dict, Any
from collections import defaultdict
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

# In-memory store for rate limiting (in production, use Redis)
rate_limit_store: Dict[str, Dict[str, Any]] = defaultdict(dict)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware for request rate limiting and throttling"""
    
    def __init__(self, app, 
                 requests_per_minute: int = 100,
                 requests_per_hour: int = 1000,
                 ip_requests_per_minute: int = 100):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
        self.ip_requests_per_minute = ip_requests_per_minute
    
    async def dispatch(self, request: Request, call_next):
        client_ip = self._get_client_ip(request)
        
        # Check IP-based rate limits
        if not self._check_ip_rate_limit(client_ip):
            raise HTTPException(
                status_code=429,
                detail="Too many requests from this IP address"
            )
        
        # Check API key-based rate limits (if authenticated)
        if hasattr(request.state, 'user') and request.state.user:
            api_key = request.headers.get("Authorization", "")
            if api_key.startswith("Bearer "):
                api_key = api_key[7:]
            
            if not self._check_api_key_rate_limit(api_key, request.state.user):
                raise HTTPException(
                    status_code=429,
                    detail="Rate limit exceeded for your API key"
                )
        
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers to response
        response.headers["X-RateLimit-Limit-Minute"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Limit-Hour"] = str(self.requests_per_hour)
        response.headers["X-RateLimit-IP-Limit-Minute"] = str(self.ip_requests_per_minute)
        
        return response
    
    def _get_client_ip(self, request: Request) -> str:
        """Get client IP address"""
        # Check for forwarded IP (from load balancer/proxy)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        # Check for real IP
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # Fallback to client host
        if request.client:
            return request.client.host
        
        return "unknown"
    
    def _check_ip_rate_limit(self, ip: str) -> bool:
        """Check rate limits for IP address"""
        current_time = int(time.time())
        minute_ago = current_time - 60
        hour_ago = current_time - 3600
        
        # Initialize store for this IP if needed
        if ip not in rate_limit_store:
            rate_limit_store[ip] = {
                "requests": [],
                "minute_requests": []
            }
        
        # Clean old requests
        rate_limit_store[ip]["requests"] = [
            req_time for req_time in rate_limit_store[ip]["requests"]
            if req_time > hour_ago
        ]
        rate_limit_store[ip]["minute_requests"] = [
            req_time for req_time in rate_limit_store[ip]["minute_requests"]
            if req_time > minute_ago
        ]
        
        # Check limits
        total_requests = len(rate_limit_store[ip]["requests"])
        minute_requests = len(rate_limit_store[ip]["minute_requests"])
        
        if total_requests >= self.requests_per_hour or minute_requests >= self.ip_requests_per_minute:
            return False
        
        # Add current request
        rate_limit_store[ip]["requests"].append(current_time)
        rate_limit_store[ip]["minute_requests"].append(current_time)
        
        return True
    
    def _check_api_key_rate_limit(self, api_key: str, user_info: Dict[str, Any]) -> bool:
        """Check rate limits for API key"""
        current_time = int(time.time())
        minute_ago = current_time - 60
        hour_ago = current_time - 3600
        
        # Use API key as identifier
        key_id = f"api_key:{api_key}"
        
        # Initialize store for this key if needed
        if key_id not in rate_limit_store:
            rate_limit_store[key_id] = {
                "requests": [],
                "minute_requests": []
            }
        
        # Clean old requests
        rate_limit_store[key_id]["requests"] = [
            req_time for req_time in rate_limit_store[key_id]["requests"]
            if req_time > hour_ago
        ]
        rate_limit_store[key_id]["minute_requests"] = [
            req_time for req_time in rate_limit_store[key_id]["minute_requests"]
            if req_time > minute_ago
        ]
        
        # Get user-specific limits
        user_limit_hour = user_info.get("rate_limit", self.requests_per_hour)
        user_limit_minute = min(user_limit_hour // 60, self.requests_per_minute)
        
        # Check limits
        total_requests = len(rate_limit_store[key_id]["requests"])
        minute_requests = len(rate_limit_store[key_id]["minute_requests"])
        
        if total_requests >= user_limit_hour or minute_requests >= user_limit_minute:
            return False
        
        # Add current request
        rate_limit_store[key_id]["requests"].append(current_time)
        rate_limit_store[key_id]["minute_requests"].append(current_time)
        
        return True