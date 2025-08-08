"""
Configuration Service for managing system configuration
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import redis.asyncio as redis

from ..config import Settings

logger = logging.getLogger(__name__)


class ConfigService:
    """Configuration service for managing system settings"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.engine = None
        self.redis_client = None
        self.is_initialized = False
        self._cache: Dict[str, Any] = {}
        self._cache_timestamps: Dict[str, datetime] = {}
        self._lock = asyncio.Lock()
        
    async def initialize(self):
        """Initialize the configuration service"""
        try:
            # Initialize database connection
            if self.settings.database_url:
                self.engine = create_async_engine(
                    self.settings.database_url,
                    pool_size=self.settings.database_pool_size,
                    echo=self.settings.database_echo
                )
                
                # Test database connection
                async with self.engine.begin() as conn:
                    await conn.execute(text("SELECT 1"))
                
                logger.info("Database connection established")
            
            # Initialize Redis connection
            if self.settings.redis_url:
                self.redis_client = redis.from_url(
                    self.settings.redis_url,
                    db=self.settings.redis_db,
                    password=self.settings.redis_password,
                    max_connections=self.settings.redis_max_connections,
                    decode_responses=True
                )
                
                # Test Redis connection
                await self.redis_client.ping()
                
                logger.info("Redis connection established")
            
            self.is_initialized = True
            logger.info("Config service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize config service: {str(e)}")
            raise
    
    async def cleanup(self):
        """Cleanup resources"""
        if self.engine:
            await self.engine.dispose()
            self.engine = None
        
        if self.redis_client:
            await self.redis_client.close()
            self.redis_client = None
        
        self.is_initialized = False
        logger.info("Config service cleaned up")
    
    async def get_config(self, key: str, use_cache: bool = True) -> Optional[str]:
        """Get configuration value by key"""
        if not self.is_initialized:
            raise RuntimeError("Config service not initialized")
        
        # Check cache first
        if use_cache and key in self._cache:
            cache_age = datetime.now() - self._cache_timestamps.get(key, datetime.min)
            if cache_age < timedelta(seconds=self.settings.token_cache_ttl):
                return self._cache[key]
        
        # Try Redis first
        if self.redis_client:
            try:
                value = await self.redis_client.get(f"config:{key}")
                if value:
                    self._cache[key] = value
                    self._cache_timestamps[key] = datetime.now()
                    return value
            except Exception as e:
                logger.warning(f"Redis get failed for key {key}: {str(e)}")
        
        # Try database
        if self.engine:
            try:
                async with self.engine.begin() as conn:
                    result = await conn.execute(
                        text("SELECT config_value FROM system_config WHERE config_key = :key AND is_active = true"),
                        {"key": key}
                    )
                    row = result.fetchone()
                    if row:
                        value = row[0]
                        self._cache[key] = value
                        self._cache_timestamps[key] = datetime.now()
                        
                        # Cache in Redis
                        if self.redis_client:
                            try:
                                await self.redis_client.setex(
                                    f"config:{key}",
                                    self.settings.token_cache_ttl,
                                    value
                                )
                            except Exception as e:
                                logger.warning(f"Redis set failed for key {key}: {str(e)}")
                        
                        return value
            except Exception as e:
                logger.error(f"Database get failed for key {key}: {str(e)}")
        
        return None
    
    async def set_config(self, key: str, value: str, config_type: str = "string", description: str = "") -> bool:
        """Set configuration value"""
        if not self.is_initialized:
            raise RuntimeError("Config service not initialized")
        
        try:
            # Update database
            if self.engine:
                async with self.engine.begin() as conn:
                    await conn.execute(
                        text("""
                            INSERT INTO system_config (config_key, config_value, config_type, description, is_active)
                            VALUES (:key, :value, :config_type, :description, true)
                            ON CONFLICT (config_key) 
                            DO UPDATE SET 
                                config_value = EXCLUDED.config_value,
                                config_type = EXCLUDED.config_type,
                                description = EXCLUDED.description,
                                updated_at = CURRENT_TIMESTAMP
                        """),
                        {
                            "key": key,
                            "value": value,
                            "config_type": config_type,
                            "description": description
                        }
                    )
            
            # Update cache
            self._cache[key] = value
            self._cache_timestamps[key] = datetime.now()
            
            # Update Redis
            if self.redis_client:
                try:
                    await self.redis_client.setex(
                        f"config:{key}",
                        self.settings.token_cache_ttl,
                        value
                    )
                except Exception as e:
                    logger.warning(f"Redis set failed for key {key}: {str(e)}")
            
            logger.info(f"Configuration updated: {key} = {value}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to set config {key}: {str(e)}")
            return False
    
    async def get_all_configs(self) -> Dict[str, Any]:
        """Get all configuration values"""
        if not self.is_initialized:
            raise RuntimeError("Config service not initialized")
        
        configs = {}
        
        try:
            if self.engine:
                async with self.engine.begin() as conn:
                    result = await conn.execute(
                        text("SELECT config_key, config_value, config_type, description FROM system_config WHERE is_active = true")
                    )
                    rows = result.fetchall()
                    
                    for row in rows:
                        configs[row[0]] = {
                            "value": row[1],
                            "type": row[2],
                            "description": row[3]
                        }
            
            return configs
            
        except Exception as e:
            logger.error(f"Failed to get all configs: {str(e)}")
            return {}
    
    async def delete_config(self, key: str) -> bool:
        """Delete configuration value"""
        if not self.is_initialized:
            raise RuntimeError("Config service not initialized")
        
        try:
            # Update database
            if self.engine:
                async with self.engine.begin() as conn:
                    await conn.execute(
                        text("UPDATE system_config SET is_active = false WHERE config_key = :key"),
                        {"key": key}
                    )
            
            # Remove from cache
            if key in self._cache:
                del self._cache[key]
                del self._cache_timestamps[key]
            
            # Remove from Redis
            if self.redis_client:
                try:
                    await self.redis_client.delete(f"config:{key}")
                except Exception as e:
                    logger.warning(f"Redis delete failed for key {key}: {str(e)}")
            
            logger.info(f"Configuration deleted: {key}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete config {key}: {str(e)}")
            return False
    
    async def get_config_batch(self, keys: List[str]) -> Dict[str, str]:
        """Get multiple configuration values at once"""
        if not self.is_initialized:
            raise RuntimeError("Config service not initialized")
        
        results = {}
        
        # Check cache first
        cache_miss_keys = []
        for key in keys:
            if key in self._cache:
                cache_age = datetime.now() - self._cache_timestamps.get(key, datetime.min)
                if cache_age < timedelta(seconds=self.settings.token_cache_ttl):
                    results[key] = self._cache[key]
                else:
                    cache_miss_keys.append(key)
            else:
                cache_miss_keys.append(key)
        
        # Get missing keys from Redis
        if cache_miss_keys and self.redis_client:
            try:
                redis_keys = [f"config:{key}" for key in cache_miss_keys]
                values = await self.redis_client.mget(redis_keys)
                
                for key, value in zip(cache_miss_keys, values):
                    if value:
                        results[key] = value
                        self._cache[key] = value
                        self._cache_timestamps[key] = datetime.now()
            except Exception as e:
                logger.warning(f"Redis mget failed: {str(e)}")
        
        # Get remaining keys from database
        remaining_keys = [key for key in cache_miss_keys if key not in results]
        if remaining_keys and self.engine:
            try:
                async with self.engine.begin() as conn:
                    for key in remaining_keys:
                        result = await conn.execute(
                            text("SELECT config_value FROM system_config WHERE config_key = :key AND is_active = true"),
                            {"key": key}
                        )
                        row = result.fetchone()
                        if row:
                            value = row[0]
                            results[key] = value
                            self._cache[key] = value
                            self._cache_timestamps[key] = datetime.now()
                            
                            # Cache in Redis
                            if self.redis_client:
                                try:
                                    await self.redis_client.setex(
                                        f"config:{key}",
                                        self.settings.token_cache_ttl,
                                        value
                                    )
                                except Exception as e:
                                    logger.warning(f"Redis set failed for key {key}: {str(e)}")
            except Exception as e:
                logger.error(f"Database batch get failed: {str(e)}")
        
        return results
    
    async def clear_cache(self):
        """Clear the configuration cache"""
        self._cache.clear()
        self._cache_timestamps.clear()
        
        if self.redis_client:
            try:
                # Delete all config keys from Redis
                pattern = "config:*"
                keys = await self.redis_client.keys(pattern)
                if keys:
                    await self.redis_client.delete(*keys)
            except Exception as e:
                logger.warning(f"Redis cache clear failed: {str(e)}")
        
        logger.info("Configuration cache cleared")
    
    async def get_ssi_config(self) -> Dict[str, str]:
        """Get SSI-specific configuration"""
        ssi_keys = [
            "SSI_CONSUMER_ID",
            "SSI_CONSUMER_SECRET", 
            "SSI_PRIVATE_KEY",
            "SSI_FC_TRADING_URL",
            "SSI_FC_DATA_URL"
        ]
        
        return await self.get_config_batch(ssi_keys)
    
    async def get_database_config(self) -> Dict[str, str]:
        """Get database configuration"""
        db_keys = [
            "DATABASE_URL",
            "REDIS_URL"
        ]
        
        return await self.get_config_batch(db_keys)
    
    async def get_security_config(self) -> Dict[str, str]:
        """Get security configuration"""
        security_keys = [
            "JWT_SECRET_KEY",
            "JWT_ALGORITHM",
            "JWT_ACCESS_TOKEN_EXPIRE_MINUTES"
        ]
        
        return await self.get_config_batch(security_keys)
    
    async def get_feature_flags(self) -> Dict[str, bool]:
        """Get feature flags configuration"""
        feature_keys = [
            "ENABLE_TRADING",
            "ENABLE_REAL_API",
            "ENABLE_AUDIT_LOGGING",
            "ENABLE_PERFORMANCE_LOGGING"
        ]
        
        configs = await self.get_config_batch(feature_keys)
        
        # Convert string values to boolean
        feature_flags = {}
        for key, value in configs.items():
            if value is not None:
                feature_flags[key] = value.lower() in ('true', '1', 'yes', 'on')
        
        return feature_flags 