"""
Authentication Middleware
API key-based authentication and authorization
"""

import logging
from typing import Optional, Dict, Any
from fastapi import Request, HTTPException, Depends
from fastapi.security import APIKeyHeader
import hashlib
import time

logger = logging.getLogger(__name__)

# In production, this would be stored in a database or secure storage
API_KEYS = {
    "admin_key": {
        "name": "admin",
        "permissions": ["read", "write", "admin"],
        "rate_limit": 1000  # requests per hour
    },
    "user_key": {
        "name": "user", 
        "permissions": ["read"],
        "rate_limit": 100  # requests per hour
    },
    "service_key": {
        "name": "service",
        "permissions": ["read", "write"],
        "rate_limit": 500  # requests per hour
    }
}

# Simple in-memory rate limiting (in production, use Redis or similar)
rate_limit_store: Dict[str, Dict[str, Any]] = {}


class AuthMiddleware:
    """Authentication and authorization middleware"""
    
    def __init__(self, app):
        self.app = app
        self.api_key_header = APIKeyHeader(name="Authorization", auto_error=False)
    
    async def __call__(self, scope, receive, send):
        # Handle HTTP requests
        if scope["type"] == "http":
            request = Request(scope, receive)
            
            # Check if authentication is required for this path
            if self._requires_auth(request.url.path):
                # Extract API key
                api_key = await self._extract_api_key(request)
                if not api_key:
                    raise HTTPException(
                        status_code=401, 
                        detail="Missing or invalid API key"
                    )
                
                # Validate API key
                user_info = self._validate_api_key(api_key)
                if not user_info:
                    raise HTTPException(
                        status_code=401, 
                        detail="Invalid API key"
                    )
                
                # Check rate limits
                if not self._check_rate_limit(api_key, user_info):
                    raise HTTPException(
                        status_code=429, 
                        detail="Rate limit exceeded"
                    )
                
                # Add user info to request state
                request.state.user = user_info
            
        await self.app(scope, receive, send)
    
    def _requires_auth(self, path: str) -> bool:
        """Check if authentication is required for a path"""
        # Skip authentication for health checks and docs
        skip_paths = ["/api/health", "/docs", "/redoc", "/openapi.json"]
        for skip_path in skip_paths:
            if path.startswith(skip_path):
                return False
        return True
    
    async def _extract_api_key(self, request: Request) -> Optional[str]:
        """Extract API key from request"""
        # Try header first
        auth_header = request.headers.get("Authorization")
        if auth_header:
            # Handle "Bearer {key}" format
            if auth_header.startswith("Bearer "):
                return auth_header[7:]  # Remove "Bearer " prefix
            return auth_header
        
        # Try query parameter
        api_key = request.query_params.get("api_key")
        if api_key:
            return api_key
        
        return None
    
    def _validate_api_key(self, api_key: str) -> Optional[Dict[str, Any]]:
        """Validate API key and return user info"""
        # In production, hash the key before comparison
        for key, user_info in API_KEYS.items():
            if api_key == key:
                return user_info
        return None
    
    def _check_rate_limit(self, api_key: str, user_info: Dict[str, Any]) -> bool:
        """Check rate limits for API key"""
        current_time = int(time.time())
        hour_ago = current_time - 3600  # 1 hour ago
        
        # Initialize rate limit store for this key if needed
        if api_key not in rate_limit_store:
            rate_limit_store[api_key] = {
                "requests": [],
                "limit": user_info.get("rate_limit", 100)
            }
        
        # Clean old requests
        rate_limit_store[api_key]["requests"] = [
            req_time for req_time in rate_limit_store[api_key]["requests"]
            if req_time > hour_ago
        ]
        
        # Check if limit exceeded
        current_requests = len(rate_limit_store[api_key]["requests"])
        limit = rate_limit_store[api_key]["limit"]
        
        if current_requests >= limit:
            return False
        
        # Add current request
        rate_limit_store[api_key]["requests"].append(current_time)
        return True


# Dependency for FastAPI routes
api_key_header = APIKeyHeader(name="Authorization", auto_error=False)


async def get_current_user(api_key_header: str = Depends(api_key_header)):
    """Dependency to get current user from API key"""
    if not api_key_header:
        raise HTTPException(
            status_code=401, 
            detail="Missing API key in Authorization header"
        )
    
    # Handle "Bearer {key}" format
    api_key = api_key_header
    if api_key.startswith("Bearer "):
        api_key = api_key[7:]  # Remove "Bearer " prefix
    
    # Validate API key
    user_info = _validate_api_key_dependency(api_key)
    if not user_info:
        raise HTTPException(
            status_code=401, 
            detail="Invalid API key"
        )
    
    return user_info


def _validate_api_key_dependency(api_key: str) -> Optional[Dict[str, Any]]:
    """Validate API key for dependency"""
    for key, user_info in API_KEYS.items():
        if api_key == key:
            return user_info
    return None


def require_permission(permission: str):
    """Dependency to check specific permissions"""
    def permission_checker(current_user: dict = Depends(get_current_user)):
        if permission not in current_user.get("permissions", []):
            raise HTTPException(
                status_code=403,
                detail=f"Permission '{permission}' required"
            )
        return current_user
    return permission_checker