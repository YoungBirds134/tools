"""
Common Redis utilities and connection management.
"""

import json
from typing import Any, Dict, List, Optional, Union

import redis
from redis.connection import ConnectionPool

from .config import get_settings
from .logging import get_logger

logger = get_logger(__name__)


class RedisManager:
    """Redis connection and operations manager."""
    
    def __init__(self, redis_settings: Optional[Any] = None):
        """Initialize Redis manager."""
        self.settings = redis_settings or get_settings().redis
        
        self.pool = ConnectionPool(
            host=self.settings.host,
            port=self.settings.port,
            db=self.settings.db,
            password=self.settings.password,
            ssl=self.settings.ssl,
            max_connections=self.settings.max_connections,
            decode_responses=self.settings.decode_responses,
        )
        
        self.client = redis.Redis(connection_pool=self.pool)
    
    async def ping(self) -> bool:
        """Test Redis connection."""
        try:
            return self.client.ping()
        except Exception as e:
            logger.error(f"Redis ping failed: {e}")
            return False
    
    def set_json(self, key: str, value: Dict[str, Any], ttl: Optional[int] = None) -> bool:
        """Set JSON value in Redis."""
        try:
            json_str = json.dumps(value, default=str)
            return self.client.set(key, json_str, ex=ttl)
        except Exception as e:
            logger.error(f"Failed to set JSON in Redis: {e}")
            return False
    
    def get_json(self, key: str) -> Optional[Dict[str, Any]]:
        """Get JSON value from Redis."""
        try:
            value = self.client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Failed to get JSON from Redis: {e}")
            return None
    
    def set_string(self, key: str, value: str, ttl: Optional[int] = None) -> bool:
        """Set string value in Redis."""
        try:
            return self.client.set(key, value, ex=ttl)
        except Exception as e:
            logger.error(f"Failed to set string in Redis: {e}")
            return False
    
    def get_string(self, key: str) -> Optional[str]:
        """Get string value from Redis."""
        try:
            return self.client.get(key)
        except Exception as e:
            logger.error(f"Failed to get string from Redis: {e}")
            return None
    
    def delete(self, *keys: str) -> int:
        """Delete keys from Redis."""
        try:
            return self.client.delete(*keys)
        except Exception as e:
            logger.error(f"Failed to delete keys from Redis: {e}")
            return 0
    
    def exists(self, key: str) -> bool:
        """Check if key exists in Redis."""
        try:
            return bool(self.client.exists(key))
        except Exception as e:
            logger.error(f"Failed to check key existence in Redis: {e}")
            return False
    
    def expire(self, key: str, ttl: int) -> bool:
        """Set TTL for a key."""
        try:
            return self.client.expire(key, ttl)
        except Exception as e:
            logger.error(f"Failed to set TTL in Redis: {e}")
            return False
    
    def incr(self, key: str, amount: int = 1) -> Optional[int]:
        """Increment counter in Redis."""
        try:
            return self.client.incr(key, amount)
        except Exception as e:
            logger.error(f"Failed to increment counter in Redis: {e}")
            return None
    
    def set_list(self, key: str, values: List[Any], ttl: Optional[int] = None) -> bool:
        """Set list value in Redis."""
        try:
            pipe = self.client.pipeline()
            pipe.delete(key)
            for value in values:
                pipe.rpush(key, json.dumps(value, default=str))
            if ttl:
                pipe.expire(key, ttl)
            pipe.execute()
            return True
        except Exception as e:
            logger.error(f"Failed to set list in Redis: {e}")
            return False
    
    def get_list(self, key: str) -> List[Any]:
        """Get list value from Redis."""
        try:
            raw_values = self.client.lrange(key, 0, -1)
            return [json.loads(value) for value in raw_values]
        except Exception as e:
            logger.error(f"Failed to get list from Redis: {e}")
            return []
    
    def push_to_list(self, key: str, value: Any) -> Optional[int]:
        """Push value to list in Redis."""
        try:
            json_str = json.dumps(value, default=str)
            return self.client.rpush(key, json_str)
        except Exception as e:
            logger.error(f"Failed to push to list in Redis: {e}")
            return None
    
    def pop_from_list(self, key: str, from_left: bool = False) -> Optional[Any]:
        """Pop value from list in Redis."""
        try:
            if from_left:
                value = self.client.lpop(key)
            else:
                value = self.client.rpop(key)
            
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Failed to pop from list in Redis: {e}")
            return None
    
    def set_hash(self, key: str, mapping: Dict[str, Any], ttl: Optional[int] = None) -> bool:
        """Set hash value in Redis."""
        try:
            # Convert all values to strings
            str_mapping = {k: json.dumps(v, default=str) for k, v in mapping.items()}
            result = self.client.hset(key, mapping=str_mapping)
            if ttl:
                self.client.expire(key, ttl)
            return True
        except Exception as e:
            logger.error(f"Failed to set hash in Redis: {e}")
            return False
    
    def get_hash(self, key: str) -> Dict[str, Any]:
        """Get hash value from Redis."""
        try:
            raw_hash = self.client.hgetall(key)
            return {k: json.loads(v) for k, v in raw_hash.items()}
        except Exception as e:
            logger.error(f"Failed to get hash from Redis: {e}")
            return {}
    
    def get_hash_field(self, key: str, field: str) -> Optional[Any]:
        """Get single field from hash in Redis."""
        try:
            value = self.client.hget(key, field)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Failed to get hash field from Redis: {e}")
            return None
    
    def set_hash_field(self, key: str, field: str, value: Any) -> bool:
        """Set single field in hash in Redis."""
        try:
            json_str = json.dumps(value, default=str)
            return bool(self.client.hset(key, field, json_str))
        except Exception as e:
            logger.error(f"Failed to set hash field in Redis: {e}")
            return False
    
    def delete_hash_field(self, key: str, *fields: str) -> int:
        """Delete fields from hash in Redis."""
        try:
            return self.client.hdel(key, *fields)
        except Exception as e:
            logger.error(f"Failed to delete hash fields from Redis: {e}")
            return 0
    
    def get_keys_pattern(self, pattern: str) -> List[str]:
        """Get keys matching pattern."""
        try:
            return self.client.keys(pattern)
        except Exception as e:
            logger.error(f"Failed to get keys with pattern from Redis: {e}")
            return []
    
    def close(self):
        """Close Redis connection."""
        try:
            self.client.close()
        except Exception as e:
            logger.error(f"Failed to close Redis connection: {e}")


# Global Redis manager instance
redis_manager = RedisManager()

# Convenience functions
def get_redis() -> RedisManager:
    """Get Redis manager instance."""
    return redis_manager
