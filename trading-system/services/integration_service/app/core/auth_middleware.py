"""
Authentication middleware for SSI APIs with Redis token caching
"""
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from app.utils.cache import cache_manager
from app.core.logging_config import get_logger
from config import settings

logger = get_logger("auth_middleware")

class SSITokenAuth:
    """SSI Token Authentication with Redis caching"""
    
    def __init__(self):
        self.cache_prefix = "ssi_token:"
        self.token_expire_minutes = 30  # SSI tokens typically expire in 30 minutes
        
    async def get_cached_token(self, consumer_id: str) -> Optional[str]:
        """Get cached access token for consumer ID"""
        try:
            cache_key = f"{self.cache_prefix}{consumer_id}"
            cached_data = await cache_manager.get(cache_key)
            
            if cached_data:
                token_data = json.loads(cached_data)
                # Check if token is still valid
                expire_time = datetime.fromisoformat(token_data['expire_time'])
                if datetime.utcnow() < expire_time:
                    logger.debug(f"Retrieved cached token for consumer {consumer_id}")
                    return token_data['access_token']
                else:
                    # Token expired, remove from cache
                    await cache_manager.delete(cache_key)
                    logger.debug(f"Cached token expired for consumer {consumer_id}")
            
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving cached token: {e}")
            return None
    
    async def cache_token(
        self, 
        consumer_id: str, 
        access_token: str, 
        expire_minutes: Optional[int] = None
    ) -> None:
        """Cache access token with expiration"""
        try:
            expire_minutes = expire_minutes or self.token_expire_minutes
            expire_time = datetime.utcnow() + timedelta(minutes=expire_minutes)
            
            token_data = {
                'access_token': access_token,
                'consumer_id': consumer_id,
                'cached_at': datetime.utcnow().isoformat(),
                'expire_time': expire_time.isoformat()
            }
            
            cache_key = f"{self.cache_prefix}{consumer_id}"
            # Cache for slightly less time than actual expiration to be safe
            cache_ttl = int((expire_minutes - 1) * 60)  # Convert to seconds
            
            await cache_manager.set(
                cache_key, 
                json.dumps(token_data), 
                expire=cache_ttl
            )
            
            logger.debug(f"Cached token for consumer {consumer_id}, expires at {expire_time}")
            
        except Exception as e:
            logger.error(f"Error caching token: {e}")
    
    async def invalidate_token(self, consumer_id: str) -> None:
        """Invalidate cached token for consumer ID"""
        try:
            cache_key = f"{self.cache_prefix}{consumer_id}"
            await cache_manager.delete(cache_key)
            logger.debug(f"Invalidated cached token for consumer {consumer_id}")
            
        except Exception as e:
            logger.error(f"Error invalidating token: {e}")
    
    async def get_consumer_from_token(self, token: str) -> Optional[str]:
        """Extract consumer ID from JWT token (if possible)"""
        try:
            # For SSI tokens, try to decode without verification to get consumer info
            # Note: This is for caching purposes only, not for security validation
            decoded = jwt.decode(token, options={"verify_signature": False})
            
            # Common JWT claims that might contain consumer info
            consumer_id = (
                decoded.get('consumer_id') or 
                decoded.get('sub') or 
                decoded.get('client_id') or
                decoded.get('cid')
            )
            
            return consumer_id
            
        except Exception as e:
            logger.debug(f"Could not extract consumer from token: {e}")
            return None


class BearerTokenMiddleware:
    """Middleware to handle Bearer token authentication"""
    
    def __init__(self):
        self.token_auth = SSITokenAuth()
        self.security = HTTPBearer(auto_error=False)
    
    async def __call__(self, request: Request) -> Optional[str]:
        """Process request and return access token if available"""
        try:
            # Skip authentication for health check and docs endpoints
            if request.url.path in ["/health", "/docs", "/redoc", "/openapi.json"]:
                return None
            
            # Get authorization header
            authorization = request.headers.get("Authorization")
            if not authorization or not authorization.startswith("Bearer "):
                return None
            
            token = authorization.replace("Bearer ", "")
            
            # Try to extract consumer ID from token for caching
            consumer_id = await self.token_auth.get_consumer_from_token(token)
            if consumer_id:
                # Check if we have a cached token for this consumer
                cached_token = await self.token_auth.get_cached_token(consumer_id)
                if cached_token:
                    return cached_token
            
            # Return the provided token (it will be validated by the service layer)
            return token
            
        except Exception as e:
            logger.error(f"Error in bearer token middleware: {e}")
            return None


# Global instance
bearer_token_middleware = BearerTokenMiddleware()
ssi_token_auth = SSITokenAuth()


async def get_authenticated_token(request: Request) -> Optional[str]:
    """Dependency to get authenticated token from request"""
    return await bearer_token_middleware(request)


async def require_authenticated_token(request: Request) -> str:
    """Dependency that requires authentication token"""
    token = await get_authenticated_token(request)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Authentication token required"},
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token


class SSIServiceAuth:
    """Authentication helper for SSI services"""
    
    @staticmethod
    async def get_or_cache_token(
        consumer_id: str,
        consumer_secret: str,
        access_token: str,
        cache_duration_minutes: Optional[int] = None
    ) -> str:
        """Cache access token and return it"""
        await ssi_token_auth.cache_token(
            consumer_id=consumer_id,
            access_token=access_token,
            expire_minutes=cache_duration_minutes
        )
        return access_token
    
    @staticmethod
    async def get_cached_token_for_consumer(consumer_id: str) -> Optional[str]:
        """Get cached token for specific consumer"""
        return await ssi_token_auth.get_cached_token(consumer_id)
    
    @staticmethod
    async def invalidate_consumer_token(consumer_id: str) -> None:
        """Invalidate cached token for consumer"""
        await ssi_token_auth.invalidate_token(consumer_id)
    
    @staticmethod
    def create_bearer_header(access_token: str) -> Dict[str, str]:
        """Create Authorization header with Bearer token"""
        return {"Authorization": f"Bearer {access_token}"}
