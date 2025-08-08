"""
Configuration management router for Config Service
"""

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional, List
import logging

from ..models import (
    ConfigRequest, ConfigResponse, ConfigBatchRequest, ConfigBatchResponse,
    FeatureFlagsResponse, CacheResponse, HealthResponse
)
from ..services.config_service import ConfigService
from ..config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


def get_config_service() -> ConfigService:
    """Get config service instance"""
    # This would be injected from the main app
    # For now, we'll create a new instance
    return ConfigService(settings)


@router.get("/{key}")
async def get_config(key: str, config_service: ConfigService = Depends(get_config_service)):
    """Get configuration value by key"""
    try:
        value = await config_service.get_config(key)
        if value is None:
            return ConfigResponse(
                success=False,
                message=f"Configuration key '{key}' not found",
                data=None
            )
        
        return ConfigResponse(
            success=True,
            message="Configuration retrieved successfully",
            data={key: value}
        )
    except Exception as e:
        logger.error(f"Failed to get config {key}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get config: {str(e)}")


@router.post("/")
async def set_config(request: ConfigRequest, config_service: ConfigService = Depends(get_config_service)):
    """Set configuration value"""
    try:
        success = await config_service.set_config(
            request.key,
            request.value,
            request.config_type.value,
            request.description
        )
        
        if success:
            return ConfigResponse(
                success=True,
                message="Configuration set successfully",
                data={request.key: request.value}
            )
        else:
            return ConfigResponse(
                success=False,
                message="Failed to set configuration",
                data=None
            )
    except Exception as e:
        logger.error(f"Failed to set config {request.key}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to set config: {str(e)}")


@router.delete("/{key}")
async def delete_config(key: str, config_service: ConfigService = Depends(get_config_service)):
    """Delete configuration value"""
    try:
        success = await config_service.delete_config(key)
        
        if success:
            return ConfigResponse(
                success=True,
                message=f"Configuration '{key}' deleted successfully",
                data=None
            )
        else:
            return ConfigResponse(
                success=False,
                message=f"Failed to delete configuration '{key}'",
                data=None
            )
    except Exception as e:
        logger.error(f"Failed to delete config {key}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete config: {str(e)}")


@router.post("/batch")
async def get_config_batch(request: ConfigBatchRequest, config_service: ConfigService = Depends(get_config_service)):
    """Get multiple configuration values"""
    try:
        results = await config_service.get_config_batch(request.keys)
        
        # Find missing keys
        missing_keys = [key for key in request.keys if key not in results]
        
        return ConfigBatchResponse(
            success=True,
            message="Batch configuration retrieved successfully",
            data=results,
            missing_keys=missing_keys
        )
    except Exception as e:
        logger.error(f"Failed to get batch config: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get batch config: {str(e)}")


@router.get("/all")
async def get_all_configs(config_service: ConfigService = Depends(get_config_service)):
    """Get all configuration values"""
    try:
        configs = await config_service.get_all_configs()
        
        return ConfigResponse(
            success=True,
            message="All configurations retrieved successfully",
            data=configs
        )
    except Exception as e:
        logger.error(f"Failed to get all configs: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get all configs: {str(e)}")


@router.get("/ssi/config")
async def get_ssi_config(config_service: ConfigService = Depends(get_config_service)):
    """Get SSI-specific configuration"""
    try:
        ssi_config = await config_service.get_ssi_config()
        
        return ConfigResponse(
            success=True,
            message="SSI configuration retrieved successfully",
            data=ssi_config
        )
    except Exception as e:
        logger.error(f"Failed to get SSI config: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get SSI config: {str(e)}")


@router.get("/database/config")
async def get_database_config(config_service: ConfigService = Depends(get_config_service)):
    """Get database configuration"""
    try:
        db_config = await config_service.get_database_config()
        
        return ConfigResponse(
            success=True,
            message="Database configuration retrieved successfully",
            data=db_config
        )
    except Exception as e:
        logger.error(f"Failed to get database config: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get database config: {str(e)}")


@router.get("/security/config")
async def get_security_config(config_service: ConfigService = Depends(get_config_service)):
    """Get security configuration"""
    try:
        security_config = await config_service.get_security_config()
        
        return ConfigResponse(
            success=True,
            message="Security configuration retrieved successfully",
            data=security_config
        )
    except Exception as e:
        logger.error(f"Failed to get security config: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get security config: {str(e)}")


@router.get("/feature-flags")
async def get_feature_flags(config_service: ConfigService = Depends(get_config_service)):
    """Get feature flags configuration"""
    try:
        feature_flags = await config_service.get_feature_flags()
        
        return FeatureFlagsResponse(
            success=True,
            message="Feature flags retrieved successfully",
            data=feature_flags
        )
    except Exception as e:
        logger.error(f"Failed to get feature flags: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get feature flags: {str(e)}")


@router.post("/cache/clear")
async def clear_cache(config_service: ConfigService = Depends(get_config_service)):
    """Clear configuration cache"""
    try:
        await config_service.clear_cache()
        
        return CacheResponse(
            success=True,
            message="Cache cleared successfully",
            data={
                "cache_size": 0,
                "redis_keys_deleted": "unknown"
            }
        )
    except Exception as e:
        logger.error(f"Failed to clear cache: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to clear cache: {str(e)}")


@router.get("/health")
async def health_check(config_service: ConfigService = Depends(get_config_service)):
    """Health check for configuration service"""
    try:
        # Check if service is initialized
        is_initialized = config_service.is_initialized
        
        # Get cache size
        cache_size = len(config_service._cache) if hasattr(config_service, '_cache') else 0
        
        health_data = {
            "initialized": is_initialized,
            "cache_size": cache_size,
            "database": "unknown",
            "redis": "unknown"
        }
        
        # Check database connection
        if config_service.engine:
            try:
                async with config_service.engine.begin() as conn:
                    await conn.execute("SELECT 1")
                health_data["database"] = "healthy"
            except Exception as e:
                health_data["database"] = f"unhealthy: {str(e)}"
        
        # Check Redis connection
        if config_service.redis_client:
            try:
                await config_service.redis_client.ping()
                health_data["redis"] = "healthy"
            except Exception as e:
                health_data["redis"] = f"unhealthy: {str(e)}"
        
        overall_healthy = (
            is_initialized and 
            health_data["database"] == "healthy" and 
            health_data["redis"] == "healthy"
        )
        
        return HealthResponse(
            success=overall_healthy,
            message="Configuration service health check",
            data=health_data
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return HealthResponse(
            success=False,
            message="Health check failed",
            data={
                "initialized": False,
                "error": str(e)
            }
        ) 