"""
Config Service - Centralized configuration management for the trading system
Handles SSI FastConnect API token management and system configuration
"""

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
import logging
from typing import Optional, Dict, Any

# Import configurations and utilities
from .config import settings
from .utils.logging import setup_logging, get_logger
from .middleware import RateLimitMiddleware, RequestLoggingMiddleware, ErrorHandlingMiddleware
from .services.ssi_service import SSIService
from .services.config_service import ConfigService
from .routers import ssi, config

# Setup logging
setup_logging(settings.log_level, settings.log_format)
logger = get_logger(__name__)

# Global service instances
ssi_service: Optional[SSIService] = None
config_service: Optional[ConfigService] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    global ssi_service, config_service
    
    # Startup
    logger.info("Starting Config Service...")
    
    try:
        # Initialize services
        ssi_service = SSIService(settings)
        config_service = ConfigService(settings)
        
        # Initialize SSI service
        await ssi_service.initialize()
        
        logger.info("Config Service started successfully")
    except Exception as e:
        logger.error(f"Failed to start Config Service: {str(e)}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down Config Service...")
    if ssi_service:
        await ssi_service.cleanup()


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Centralized configuration management for the trading system",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=settings.allowed_methods,
    allow_headers=settings.allowed_headers
)

app.add_middleware(ErrorHandlingMiddleware)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(RateLimitMiddleware, requests_per_minute=settings.rate_limit_requests)

# Include routers
app.include_router(ssi.router, prefix="/api/v1/ssi", tags=["SSI FastConnect"])
app.include_router(config.router, prefix="/api/v1/config", tags=["Configuration"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "message": "Config Service - Centralized configuration management"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check SSI service health
        ssi_healthy = ssi_service.is_healthy() if ssi_service else False
        
        return {
            "status": "healthy" if ssi_healthy else "degraded",
            "version": settings.app_version,
            "services": {
                "ssi_service": "healthy" if ssi_healthy else "unhealthy",
                "config_service": "healthy"
            },
            "timestamp": "2025-07-16T00:00:00Z"
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "version": settings.app_version,
            "error": str(e),
            "timestamp": "2025-07-16T00:00:00Z"
        }


@app.get("/api/v1/ssi/access-token")
async def get_ssi_access_token():
    """Get SSI FastConnect access token"""
    try:
        if not ssi_service:
            raise HTTPException(status_code=503, detail="SSI service not initialized")
        
        token = await ssi_service.get_access_token()
        return {
            "success": True,
            "message": "Access token retrieved successfully",
            "data": {
                "access_token": token,
                "expires_in": ssi_service.token_expires_in if hasattr(ssi_service, 'token_expires_in') else None
            }
        }
    except Exception as e:
        logger.error(f"Failed to get SSI access token: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get access token: {str(e)}")


@app.get("/api/v1/ssi/trading-access-token")
async def get_ssi_trading_access_token():
    """Get SSI FastConnect trading access token"""
    try:
        if not ssi_service:
            raise HTTPException(status_code=503, detail="SSI service not initialized")
        
        token = await ssi_service.get_trading_access_token()
        return {
            "success": True,
            "message": "Trading access token retrieved successfully",
            "data": {
                "access_token": token,
                "expires_in": ssi_service.trading_token_expires_in if hasattr(ssi_service, 'trading_token_expires_in') else None
            }
        }
    except Exception as e:
        logger.error(f"Failed to get SSI trading access token: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get trading access token: {str(e)}")


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Custom HTTP exception handler"""
    logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """General exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
            "error": "An unexpected error occurred"
        }
    )


def create_app() -> FastAPI:
    """Application factory"""
    return app


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        workers=settings.workers,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
