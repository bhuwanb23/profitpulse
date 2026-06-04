"""
Token Manager for OAuth 2.0 token management
Handles access token caching, refresh, and lifecycle management
"""

import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Optional
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class TokenEntry:
    """Internal token data entry"""
    access_token: str
    refresh_token: Optional[str] = None
    expires_at: Optional[datetime] = None
    token_type: str = "Bearer"
    scope: str = ""


class TokenManager:
    """Manages OAuth tokens across multiple providers"""

    def __init__(self):
        self._tokens: Dict[str, Dict[str, TokenEntry]] = {}

    def _get_key(self, provider: str, identifier: str) -> str:
        return f"{provider}:{identifier}"

    async def get_valid_token(self, provider: str, identifier: str) -> Optional[str]:
        key = self._get_key(provider, identifier)
        provider_tokens = self._tokens.get(provider)
        if not provider_tokens:
            return None
        entry = provider_tokens.get(identifier)
        if not entry:
            return None
        if entry.expires_at and datetime.now() >= entry.expires_at:
            logger.info(f"Token expired for {key}")
            return None
        logger.debug(f"Valid token found for {key}")
        return entry.access_token

    async def refresh_token(self, provider: str, identifier: str) -> bool:
        key = self._get_key(provider, identifier)
        logger.info(f"Refreshing token for {key}")
        try:
            # Simulate OAuth refresh — in production this calls the actual
            # /oauth/token endpoint with grant_type=refresh_token
            await asyncio.sleep(0.1)
            entry = self._tokens.get(provider, {}).get(identifier)
            new_token = f"refreshed_{provider}_token_{datetime.now().timestamp():.0f}"
            if entry:
                entry.access_token = new_token
                entry.expires_at = datetime.now() + timedelta(hours=1)
            else:
                if provider not in self._tokens:
                    self._tokens[provider] = {}
                self._tokens[provider][identifier] = TokenEntry(
                    access_token=new_token,
                    expires_at=datetime.now() + timedelta(hours=1)
                )
            logger.info(f"Token refreshed successfully for {key}")
            return True
        except Exception as e:
            logger.error(f"Failed to refresh token for {key}: {e}")
            return False

    def store_token(self, provider: str, identifier: str,
                    access_token: str, refresh_token: Optional[str] = None,
                    expires_in: int = 3600) -> None:
        if provider not in self._tokens:
            self._tokens[provider] = {}
        self._tokens[provider][identifier] = TokenEntry(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=datetime.now() + timedelta(seconds=expires_in)
        )

    def invalidate_token(self, provider: str, identifier: str) -> None:
        key = self._get_key(provider, identifier)
        provider_tokens = self._tokens.get(provider)
        if provider_tokens and identifier in provider_tokens:
            del provider_tokens[identifier]
            logger.info(f"Token invalidated for {key}")


_token_manager_instance: Optional[TokenManager] = None


def create_token_manager() -> TokenManager:
    global _token_manager_instance
    if _token_manager_instance is None:
        _token_manager_instance = TokenManager()
    return _token_manager_instance
