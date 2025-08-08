"""
Redis cache utility for SSI Integration Service
"""
import json
import pickle
from typing import Any, Optional, Union, TypeVar, Generic
from datetime import timedelta
import aioredis
from config import settings
from app.core.logging_config import LoggerMixin
from app.core.exceptions import SSICacheError

T = TypeVar('T')


class CacheManager(LoggerMixin, Generic[T]):
    """Redis cache manager with type hints"""
    
    def __init__(self):
        self._redis: Optional[aioredis.Redis] = None
    
    async def connect(self) -> None:
        """Connect to Redis"""
        try:
            self._redis = aioredis.from_url(
                settings.redis_url,
                encoding="utf-8",
                decode_responses=False,
                socket_timeout=settings.redis_timeout,
                socket_connect_timeout=settings.connection_timeout,
                retry_on_timeout=True,
                health_check_interval=30
            )
            # Test connection
            await self._redis.ping()
            self.log_info("Connected to Redis", url=settings.redis_url)
        except Exception as e:
            self.log_error("Failed to connect to Redis", error=str(e))
            raise SSICacheError(f"Failed to connect to Redis: {e}")
    
    async def disconnect(self) -> None:
        """Disconnect from Redis"""
        if self._redis:
            await self._redis.close()
            self.log_info("Disconnected from Redis")
    
    @property
    def redis(self) -> aioredis.Redis:
        """Get Redis connection"""
        if not self._redis:
            raise SSICacheError("Redis not connected")
        return self._redis
    
    async def get(self, key: str, use_json: bool = True) -> Optional[T]:
        """Get value from cache"""
        try:
            value = await self.redis.get(key)
            if value is None:
                return None
            
            if use_json:
                return json.loads(value)
            else:
                return pickle.loads(value)
                
        except Exception as e:
            self.log_error("Failed to get from cache", key=key, error=str(e))
            raise SSICacheError(f"Failed to get from cache: {e}")
    
    async def set(
        self, 
        key: str, 
        value: T, 
        ttl: Optional[int] = None,
        use_json: bool = True
    ) -> None:
        """Set value in cache"""
        try:
            if use_json:
                serialized_value = json.dumps(value, default=str)
            else:
                serialized_value = pickle.dumps(value)
            
            await self.redis.set(key, serialized_value, ex=ttl)
            self.log_debug("Set cache value", key=key, ttl=ttl)
            
        except Exception as e:
            self.log_error("Failed to set cache", key=key, error=str(e))
            raise SSICacheError(f"Failed to set cache: {e}")
    
    async def delete(self, key: str) -> bool:
        """Delete key from cache"""
        try:
            result = await self.redis.delete(key)
            self.log_debug("Deleted cache key", key=key, existed=bool(result))
            return bool(result)
            
        except Exception as e:
            self.log_error("Failed to delete from cache", key=key, error=str(e))
            raise SSICacheError(f"Failed to delete from cache: {e}")
    
    async def exists(self, key: str) -> bool:
        """Check if key exists in cache"""
        try:
            result = await self.redis.exists(key)
            return bool(result)
            
        except Exception as e:
            self.log_error("Failed to check cache existence", key=key, error=str(e))
            raise SSICacheError(f"Failed to check cache existence: {e}")
    
    async def set_with_expiry(
        self, 
        key: str, 
        value: T, 
        expiry: timedelta,
        use_json: bool = True
    ) -> None:
        """Set value with expiry time"""
        await self.set(key, value, ttl=int(expiry.total_seconds()), use_json=use_json)
    
    async def get_or_set(
        self, 
        key: str, 
        factory_func, 
        ttl: Optional[int] = None,
        use_json: bool = True
    ) -> T:
        """Get value from cache or set using factory function"""
        value = await self.get(key, use_json)
        if value is not None:
            return value
        
        # Generate new value
        new_value = await factory_func() if callable(factory_func) else factory_func
        await self.set(key, new_value, ttl, use_json)
        return new_value
    
    async def clear_pattern(self, pattern: str) -> int:
        """Clear all keys matching pattern"""
        try:
            keys = await self.redis.keys(pattern)
            if keys:
                deleted = await self.redis.delete(*keys)
                self.log_info("Cleared cache pattern", pattern=pattern, count=deleted)
                return deleted
            return 0
            
        except Exception as e:
            self.log_error("Failed to clear cache pattern", pattern=pattern, error=str(e))
            raise SSICacheError(f"Failed to clear cache pattern: {e}")


# Cache key builders
class CacheKeys:
    """Cache key builders for different data types"""
    
    @staticmethod
    def token_key(service: str, consumer_id: str) -> str:
        """Build cache key for access tokens"""
        return f"token:{service}:{consumer_id}"
    
    @staticmethod
    def market_data_key(symbol: str, market: str, data_type: str) -> str:
        """Build cache key for market data"""
        return f"market_data:{market}:{symbol}:{data_type}"
    
    @staticmethod
    def master_data_key(data_type: str, identifier: str = "") -> str:
        """Build cache key for master data"""
        key = f"master_data:{data_type}"
        if identifier:
            key += f":{identifier}"
        return key
    
    @staticmethod
    def user_session_key(user_id: str, session_id: str) -> str:
        """Build cache key for user sessions"""
        return f"session:{user_id}:{session_id}"
    
    @staticmethod
    def rate_limit_key(user_id: str, endpoint: str) -> str:
        """Build cache key for rate limiting"""
        return f"rate_limit:{user_id}:{endpoint}"


# Global cache manager instance
cache_manager = CacheManager()
