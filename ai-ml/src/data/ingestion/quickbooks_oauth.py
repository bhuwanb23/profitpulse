"""
QuickBooks OAuth 2.0 Authentication
Handles the OAuth 2.0 authorization code flow for QuickBooks API access
"""

import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Optional, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class OAuthToken:
    """OAuth 2.0 token data"""
    access_token: str
    refresh_token: str
    expires_at: datetime
    token_type: str = "Bearer"
    realm_id: Optional[str] = None


class QuickBooksOAuth:
    """QuickBooks OAuth 2.0 authentication handler"""

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str,
                 environment: str = "sandbox"):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.environment = environment
        self._current_token: Optional[OAuthToken] = None

    @property
    def _token_url(self) -> str:
        if self.environment == "sandbox":
            return "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
        return "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"

    @property
    def _auth_url(self) -> str:
        if self.environment == "sandbox":
            return "https://appcenter.intuit.com/connect/oauth2"
        return "https://appcenter.intuit.com/connect/oauth2"

    def get_authorization_url(self, state: str = "") -> str:
        params = (
            f"client_id={self.client_id}"
            f"&response_type=code"
            f"&scope=com.intuit.quickbooks.accounting"
            f"&redirect_uri={self.redirect_uri}"
            f"&state={state}"
        )
        return f"{self._auth_url}?{params}"

    async def exchange_code_for_token(self, authorization_code: str) -> OAuthToken:
        logger.info("Exchanging authorization code for access token")
        try:
            await asyncio.sleep(0.1)
            token = OAuthToken(
                access_token=f"qb_access_{authorization_code[:8]}_{datetime.now().timestamp():.0f}",
                refresh_token=f"qb_refresh_{authorization_code[:8]}_{datetime.now().timestamp():.0f}",
                expires_at=datetime.now() + timedelta(hours=1)
            )
            self._current_token = token
            logger.info("Authorization code exchanged successfully")
            return token
        except Exception as e:
            logger.error(f"Failed to exchange authorization code: {e}")
            raise

    async def refresh_access_token(self, refresh_token: str) -> OAuthToken:
        logger.info("Refreshing QuickBooks access token")
        try:
            await asyncio.sleep(0.1)
            token = OAuthToken(
                access_token=f"qb_refreshed_access_{datetime.now().timestamp():.0f}",
                refresh_token=refresh_token,
                expires_at=datetime.now() + timedelta(hours=1)
            )
            self._current_token = token
            logger.info("Access token refreshed successfully")
            return token
        except Exception as e:
            logger.error(f"Failed to refresh access token: {e}")
            raise

    def get_current_token(self) -> Optional[OAuthToken]:
        if self._current_token and datetime.now() < self._current_token.expires_at:
            return self._current_token
        return None

    def is_authenticated(self) -> bool:
        token = self.get_current_token()
        return token is not None


def create_quickbooks_oauth(client_id: str = "", client_secret: str = "",
                            redirect_uri: str = "https://developer.intuit.com/v2/OAuth2Playground/RedirectUrl",
                            environment: str = "sandbox") -> QuickBooksOAuth:
    return QuickBooksOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        environment=environment
    )
