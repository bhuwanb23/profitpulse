"""
QuickBooks OAuth 2.0 Authentication
Handles OAuth flow, token management, and refresh for QuickBooks API
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, Any
from dataclasses import dataclass
import secrets
import base64

from authlib.integrations.aiohttp_client import OAuth2Session
from authlib.oauth2.rfc6749 import OAuth2Error
import aiohttp

from config import settings

logger = logging.getLogger(__name__)


@dataclass
class QuickBooksOAuthConfig:
    """QuickBooks OAuth configuration"""
    client_id: str
    client_secret: str
    redirect_uri: str
    base_url: str
    use_sandbox: bool = True
    scope: str = "com.intuit.quickbooks.accounting"


class QuickBooksOAuthError(Exception):
    """Custom exception for QuickBooks OAuth errors"""
    pass


class QuickBooksOAuth:
    """QuickBooks OAuth 2.0 authentication handler"""
    
    def __init__(self, config: QuickBooksOAuthConfig):
        self.config = config
        self.session: Optional[OAuth2Session] = None
        self._state_storage: Dict[str, str] = {}  # In production, use Redis or database
        
    async def initialize(self):
        """Initialize OAuth session"""
        try:
            # Determine OAuth URLs based on environment
            if self.config.use_sandbox:
                authorize_url = "https://appcenter.intuit.com/connect/oauth2"
                token_url = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
            else:
                authorize_url = "https://appcenter.intuit.com/connect/oauth2"
                token_url = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
            
            # Create OAuth session
            self.session = OAuth2Session(
                client_id=self.config.client_id,
                client_secret=self.config.client_secret,
                redirect_uri=self.config.redirect_uri,
                scope=self.config.scope,
                authorization_endpoint=authorize_url,
                token_endpoint=token_url
            )
            
            logger.info("QuickBooks OAuth session initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize QuickBooks OAuth: {e}")
            raise QuickBooksOAuthError(f"OAuth initialization failed: {e}")
    
    async def get_authorization_url(self, state: Optional[str] = None) -> str:
        """Generate OAuth authorization URL"""
        try:
            if not self.session:
                await self.initialize()
            
            # Generate state if not provided
            if not state:
                state = secrets.token_urlsafe(32)
            
            # Store state for validation
            self._state_storage[state] = datetime.now().isoformat()
            
            # Generate authorization URL
            auth_url, _ = self.session.create_authorization_url(
                self.session.authorization_endpoint,
                state=state
            )
            
            logger.info(f"Generated QuickBooks authorization URL with state: {state}")
            return auth_url
            
        except Exception as e:
            logger.error(f"Failed to generate authorization URL: {e}")
            raise QuickBooksOAuthError(f"Authorization URL generation failed: {e}")
    
    async def exchange_code_for_tokens(self, code: str, state: Optional[str] = None) -> Dict[str, Any]:
        """Exchange authorization code for access and refresh tokens"""
        try:
            if not self.session:
                await self.initialize()
            
            # Validate state if provided
            if state and state not in self._state_storage:
                raise QuickBooksOAuthError("Invalid state parameter")
            
            # Exchange code for tokens
            token_response = await self.session.fetch_token(
                self.session.token_endpoint,
                code=code,
                method="POST"
            )
            
            # Clean up state
            if state:
                self._state_storage.pop(state, None)
            
            logger.info("Successfully exchanged authorization code for tokens")
            return token_response
            
        except OAuth2Error as e:
            logger.error(f"OAuth error during token exchange: {e}")
            raise QuickBooksOAuthError(f"Token exchange failed: {e}")
        except Exception as e:
            logger.error(f"Failed to exchange code for tokens: {e}")
            raise QuickBooksOAuthError(f"Token exchange failed: {e}")
    
    async def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        """Refresh expired access token using refresh token"""
        try:
            if not self.session:
                await self.initialize()
            
            # Refresh the token
            token_response = await self.session.refresh_token(
                self.session.token_endpoint,
                refresh_token=refresh_token,
                method="POST"
            )
            
            logger.info("Successfully refreshed access token")
            return token_response
            
        except OAuth2Error as e:
            logger.error(f"OAuth error during token refresh: {e}")
            raise QuickBooksOAuthError(f"Token refresh failed: {e}")
        except Exception as e:
            logger.error(f"Failed to refresh access token: {e}")
            raise QuickBooksOAuthError(f"Token refresh failed: {e}")
    
    async def revoke_token(self, token: str, token_type: str = "access_token") -> bool:
        """Revoke access or refresh token"""
        try:
            if not self.session:
                await self.initialize()
            
            # Determine revocation endpoint
            if self.config.use_sandbox:
                revoke_url = "https://developer.api.intuit.com/v2/oauth2/tokens/revoke"
            else:
                revoke_url = "https://developer.api.intuit.com/v2/oauth2/tokens/revoke"
            
            # Prepare revocation data
            data = {
                "token": token,
                "token_type_hint": token_type
            }
            
            # Make revocation request
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    revoke_url,
                    data=data,
                    auth=aiohttp.BasicAuth(self.config.client_id, self.config.client_secret)
                ) as response:
                    if response.status == 200:
                        logger.info(f"Successfully revoked {token_type}")
                        return True
                    else:
                        logger.error(f"Token revocation failed: {response.status}")
                        return False
            
        except Exception as e:
            logger.error(f"Failed to revoke token: {e}")
            return False
    
    def validate_token(self, token_data: Dict[str, Any]) -> bool:
        """Validate token data structure and expiration"""
        try:
            # Check required fields
            required_fields = ["access_token", "token_type", "expires_in"]
            for field in required_fields:
                if field not in token_data:
                    logger.error(f"Missing required token field: {field}")
                    return False
            
            # Check token type
            if token_data.get("token_type") != "bearer":
                logger.error(f"Invalid token type: {token_data.get('token_type')}")
                return False
            
            # Check expiration
            expires_in = token_data.get("expires_in", 0)
            if expires_in <= 0:
                logger.error("Token has no expiration time")
                return False
            
            logger.info("Token validation successful")
            return True
            
        except Exception as e:
            logger.error(f"Token validation failed: {e}")
            return False
    
    def get_token_expiry(self, token_data: Dict[str, Any]) -> datetime:
        """Calculate token expiry datetime"""
        try:
            expires_in = token_data.get("expires_in", 3600)  # Default 1 hour
            return datetime.now() + timedelta(seconds=expires_in)
        except Exception as e:
            logger.error(f"Failed to calculate token expiry: {e}")
            return datetime.now() + timedelta(hours=1)  # Fallback
    
    def is_token_expired(self, token_data: Dict[str, Any]) -> bool:
        """Check if token is expired"""
        try:
            expiry = self.get_token_expiry(token_data)
            return datetime.now() >= expiry
        except Exception as e:
            logger.error(f"Failed to check token expiration: {e}")
            return True  # Assume expired if we can't check
    
    async def close(self):
        """Close OAuth session"""
        if self.session:
            await self.session.close()
            logger.info("QuickBooks OAuth session closed")


# Factory function for creating QuickBooks OAuth handler
def create_quickbooks_oauth() -> QuickBooksOAuth:
    """Create QuickBooks OAuth handler with configuration from settings"""
    config = QuickBooksOAuthConfig(
        client_id=settings.quickbooks.client_id,
        client_secret=settings.quickbooks.client_secret,
        redirect_uri=settings.quickbooks.redirect_uri,
        base_url=settings.quickbooks.base_url,
        use_sandbox=settings.quickbooks.use_sandbox,
        scope=settings.quickbooks.scope
    )
    
    return QuickBooksOAuth(config)
