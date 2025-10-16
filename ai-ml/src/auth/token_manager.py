"""
Token Manager
Handles encrypted storage, retrieval, and refresh of OAuth tokens
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, Any, List
from dataclasses import dataclass
import json

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import sqlite3
import aiosqlite

from config import settings

logger = logging.getLogger(__name__)


@dataclass
class TokenData:
    """Token data structure"""
    provider: str
    access_token: str
    refresh_token: Optional[str]
    token_type: str
    expires_at: datetime
    scope: Optional[str] = None
    company_id: Optional[str] = None


class TokenManagerError(Exception):
    """Custom exception for token management errors"""
    pass


class TokenManager:
    """Manages encrypted storage and retrieval of OAuth tokens"""
    
    def __init__(self, encryption_key: str, database_url: str):
        self.encryption_key = encryption_key
        self.database_url = database_url
        self.cipher = self._create_cipher(encryption_key)
        self._init_database()
        
    def _create_cipher(self, key: str) -> Fernet:
        """Create Fernet cipher from encryption key"""
        try:
            # If key is not 32 bytes, derive it using PBKDF2
            if len(key) != 32:
                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=b'superhack_token_salt',  # In production, use random salt
                    iterations=100000,
                )
                key_bytes = kdf.derive(key.encode())
            else:
                key_bytes = key.encode()
            
            return Fernet(base64.urlsafe_b64encode(key_bytes))
            
        except Exception as e:
            logger.error(f"Failed to create cipher: {e}")
            raise TokenManagerError(f"Cipher creation failed: {e}")
    
    def _init_database(self):
        """Initialize database schema for token storage"""
        try:
            # Create database schema
            schema_sql = """
            CREATE TABLE IF NOT EXISTS oauth_tokens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                provider TEXT NOT NULL,
                access_token TEXT NOT NULL,
                refresh_token TEXT,
                token_type TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                scope TEXT,
                company_id TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(provider, company_id)
            );
            
            CREATE INDEX IF NOT EXISTS idx_provider_company ON oauth_tokens(provider, company_id);
            CREATE INDEX IF NOT EXISTS idx_expires_at ON oauth_tokens(expires_at);
            """
            
            # Run schema creation synchronously for initialization
            with sqlite3.connect(self.database_url.replace('sqlite:///', '')) as conn:
                conn.executescript(schema_sql)
                conn.commit()
            
            logger.info("Token database schema initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize database schema: {e}")
            raise TokenManagerError(f"Database initialization failed: {e}")
    
    def _encrypt_token(self, token: str) -> str:
        """Encrypt token using Fernet"""
        try:
            encrypted_bytes = self.cipher.encrypt(token.encode())
            return base64.urlsafe_b64encode(encrypted_bytes).decode()
        except Exception as e:
            logger.error(f"Failed to encrypt token: {e}")
            raise TokenManagerError(f"Token encryption failed: {e}")
    
    def _decrypt_token(self, encrypted_token: str) -> str:
        """Decrypt token using Fernet"""
        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_token.encode())
            decrypted_bytes = self.cipher.decrypt(encrypted_bytes)
            return decrypted_bytes.decode()
        except Exception as e:
            logger.error(f"Failed to decrypt token: {e}")
            raise TokenManagerError(f"Token decryption failed: {e}")
    
    async def store_token(self, token_data: TokenData) -> bool:
        """Store encrypted token in database"""
        try:
            async with aiosqlite.connect(self.database_url.replace('sqlite:///', '')) as db:
                # Encrypt tokens
                encrypted_access_token = self._encrypt_token(token_data.access_token)
                encrypted_refresh_token = None
                if token_data.refresh_token:
                    encrypted_refresh_token = self._encrypt_token(token_data.refresh_token)
                
                # Insert or update token
                await db.execute("""
                    INSERT OR REPLACE INTO oauth_tokens 
                    (provider, access_token, refresh_token, token_type, expires_at, scope, company_id, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    token_data.provider,
                    encrypted_access_token,
                    encrypted_refresh_token,
                    token_data.token_type,
                    token_data.expires_at.isoformat(),
                    token_data.scope,
                    token_data.company_id,
                    datetime.now().isoformat()
                ))
                
                await db.commit()
                
            logger.info(f"Token stored for provider: {token_data.provider}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to store token: {e}")
            return False
    
    async def get_token(self, provider: str, company_id: Optional[str] = None) -> Optional[TokenData]:
        """Retrieve and decrypt token from database"""
        try:
            async with aiosqlite.connect(self.database_url.replace('sqlite:///', '')) as db:
                # Query for token
                if company_id:
                    cursor = await db.execute("""
                        SELECT access_token, refresh_token, token_type, expires_at, scope, company_id
                        FROM oauth_tokens 
                        WHERE provider = ? AND company_id = ?
                    """, (provider, company_id))
                else:
                    cursor = await db.execute("""
                        SELECT access_token, refresh_token, token_type, expires_at, scope, company_id
                        FROM oauth_tokens 
                        WHERE provider = ?
                        ORDER BY updated_at DESC
                        LIMIT 1
                    """, (provider,))
                
                row = await cursor.fetchone()
                
                if not row:
                    logger.warning(f"No token found for provider: {provider}")
                    return None
                
                # Decrypt tokens
                access_token = self._decrypt_token(row[0])
                refresh_token = self._decrypt_token(row[1]) if row[1] else None
                
                # Parse expiry datetime
                expires_at = datetime.fromisoformat(row[3])
                
                token_data = TokenData(
                    provider=provider,
                    access_token=access_token,
                    refresh_token=refresh_token,
                    token_type=row[2],
                    expires_at=expires_at,
                    scope=row[4],
                    company_id=row[5]
                )
                
                logger.info(f"Token retrieved for provider: {provider}")
                return token_data
                
        except Exception as e:
            logger.error(f"Failed to retrieve token: {e}")
            return None
    
    async def get_valid_token(self, provider: str, company_id: Optional[str] = None) -> Optional[str]:
        """Get valid access token, return None if expired or not found"""
        try:
            token_data = await self.get_token(provider, company_id)
            
            if not token_data:
                logger.warning(f"No token found for provider: {provider}")
                return None
            
            # Check if token is expired
            if datetime.now() >= token_data.expires_at:
                logger.warning(f"Token expired for provider: {provider}")
                return None
            
            logger.info(f"Valid token retrieved for provider: {provider}")
            return token_data.access_token
            
        except Exception as e:
            logger.error(f"Failed to get valid token: {e}")
            return None
    
    async def refresh_token(self, provider: str, company_id: Optional[str] = None) -> bool:
        """Refresh token using stored refresh token"""
        try:
            token_data = await self.get_token(provider, company_id)
            
            if not token_data or not token_data.refresh_token:
                logger.error(f"No refresh token available for provider: {provider}")
                return False
            
            # Import here to avoid circular imports
            from .quickbooks_oauth import create_quickbooks_oauth
            
            # Create OAuth handler and refresh token
            oauth_handler = create_quickbooks_oauth()
            
            try:
                new_token_data = await oauth_handler.refresh_access_token(token_data.refresh_token)
                
                # Create new TokenData with updated information
                updated_token = TokenData(
                    provider=provider,
                    access_token=new_token_data["access_token"],
                    refresh_token=new_token_data.get("refresh_token", token_data.refresh_token),
                    token_type=new_token_data["token_type"],
                    expires_at=datetime.now() + timedelta(seconds=new_token_data["expires_in"]),
                    scope=new_token_data.get("scope", token_data.scope),
                    company_id=company_id
                )
                
                # Store updated token
                success = await self.store_token(updated_token)
                
                if success:
                    logger.info(f"Token refreshed successfully for provider: {provider}")
                else:
                    logger.error(f"Failed to store refreshed token for provider: {provider}")
                
                return success
                
            finally:
                await oauth_handler.close()
                
        except Exception as e:
            logger.error(f"Failed to refresh token: {e}")
            return False
    
    async def delete_token(self, provider: str, company_id: Optional[str] = None) -> bool:
        """Delete token from database"""
        try:
            async with aiosqlite.connect(self.database_url.replace('sqlite:///', '')) as db:
                if company_id:
                    await db.execute("""
                        DELETE FROM oauth_tokens 
                        WHERE provider = ? AND company_id = ?
                    """, (provider, company_id))
                else:
                    await db.execute("""
                        DELETE FROM oauth_tokens 
                        WHERE provider = ?
                    """, (provider,))
                
                await db.commit()
                
            logger.info(f"Token deleted for provider: {provider}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete token: {e}")
            return False
    
    async def cleanup_expired_tokens(self) -> int:
        """Remove expired tokens from database"""
        try:
            async with aiosqlite.connect(self.database_url.replace('sqlite:///', '')) as db:
                cursor = await db.execute("""
                    DELETE FROM oauth_tokens 
                    WHERE expires_at < ?
                """, (datetime.now().isoformat(),))
                
                deleted_count = cursor.rowcount
                await db.commit()
                
            logger.info(f"Cleaned up {deleted_count} expired tokens")
            return deleted_count
            
        except Exception as e:
            logger.error(f"Failed to cleanup expired tokens: {e}")
            return 0
    
    async def get_all_tokens(self) -> List[TokenData]:
        """Get all stored tokens (for debugging/admin purposes)"""
        try:
            tokens = []
            async with aiosqlite.connect(self.database_url.replace('sqlite:///', '')) as db:
                cursor = await db.execute("""
                    SELECT provider, access_token, refresh_token, token_type, expires_at, scope, company_id
                    FROM oauth_tokens
                    ORDER BY updated_at DESC
                """)
                
                rows = await cursor.fetchall()
                
                for row in rows:
                    # Decrypt tokens
                    access_token = self._decrypt_token(row[1])
                    refresh_token = self._decrypt_token(row[2]) if row[2] else None
                    
                    token_data = TokenData(
                        provider=row[0],
                        access_token=access_token,
                        refresh_token=refresh_token,
                        token_type=row[3],
                        expires_at=datetime.fromisoformat(row[4]),
                        scope=row[5],
                        company_id=row[6]
                    )
                    tokens.append(token_data)
            
            logger.info(f"Retrieved {len(tokens)} tokens")
            return tokens
            
        except Exception as e:
            logger.error(f"Failed to get all tokens: {e}")
            return []


# Factory function for creating token manager
def create_token_manager() -> TokenManager:
    """Create token manager with configuration from settings"""
    return TokenManager(
        encryption_key=settings.encryption_key,
        database_url=settings.database_url
    )
