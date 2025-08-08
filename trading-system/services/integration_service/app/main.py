"""
Main FastAPI application
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
import time
import uvicorn

from app.api.fc_data_routes import router as fc_data_router
from app.api.fc_trading_routes import router as fc_trading_router
from app.api.fc_trading_additional_routes import router as fc_trading_additional_router
from app.core.logging_config import setup_logging, get_logger
from app.core.exceptions import (
    SSIIntegrationError, SSIAPIError,
    ssi_integration_error_to_http_exception,
    ssi_api_error_to_http_exception
)
from app.utils.cache import cache_manager
from app.schemas.base import HealthCheckResponse, ErrorResponse
from config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler"""
    logger = get_logger("main")
    
    # Startup
    logger.info("Starting SSI Integration Service", version=settings.app_version)
    
    try:
        # Initialize cache
        await cache_manager.connect()
        logger.info("Cache manager connected")
        
        yield
        
    finally:
        # Shutdown
        logger.info("Shutting down SSI Integration Service")
        await cache_manager.disconnect()
        logger.info("Cache manager disconnected")


# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    SSI Integration Service provides unified access to SSI FastConnect Data and Trading APIs.
    
    ## Features
    
    ### FC Data API
    - Securities information
    - Daily and intraday OHLC data
    - Index data
    - Stock price data
    
    ### FC Trading API
    - Authentication and 2FA
    - Order placement, modification, and cancellation
    - Account balance and positions
    - Order history and current orders
    - Trading power calculations
    
    ## Authentication
    Most endpoints require authentication. Use the `/fc-trading/auth/token` endpoint to obtain an access token.
    
    ## Caching
    Market data and master data are cached using Redis to improve performance.
    
    ## Rate Limiting
    API calls are subject to rate limiting to comply with SSI API limits.
    """,
    docs_url="/docs" ,
    redoc_url="/redoc" ,
    openapi_url="/openapi.json" ,
    lifespan=lifespan,
    debug=settings.debug
)

# Setup logging
setup_logging()
logger = get_logger("main")

# Add middleware  
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Add request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests"""
    start_time = time.time()
    
    # Log request
    logger.info(
        "Request started",
        method=request.method,
        url=str(request.url),
        client_ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent")
    )
    
    response = await call_next(request)
    
    # Calculate processing time
    process_time = time.time() - start_time
    
    # Log response
    logger.info(
        "Request completed",
        method=request.method,
        url=str(request.url),
        status_code=response.status_code,
        process_time=round(process_time, 4)
    )
    
    # Add processing time header
    response.headers["X-Process-Time"] = str(process_time)
    
    return response


# Global exception handlers
@app.exception_handler(SSIAPIError)
async def ssi_api_exception_handler(request: Request, exc: SSIAPIError):
    """Handle SSI API errors"""
    logger.error(
        "SSI API error",
        error=exc.message,
        status_code=exc.status_code,
        error_code=exc.error_code,
        url=str(request.url)
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.message,
            "error_code": exc.error_code,
            "details": exc.details,
            "timestamp": time.time()
        }
    )


@app.exception_handler(SSIIntegrationError)
async def ssi_integration_exception_handler(request: Request, exc: SSIIntegrationError):
    """Handle SSI Integration errors"""
    logger.error(
        "Integration error",
        error=exc.message,
        details=exc.details,
        url=str(request.url)
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": exc.message,
            "error_code": "INTEGRATION_ERROR",
            "details": exc.details,
            "timestamp": time.time()
        }
    )


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle validation errors"""
    logger.warning(
        "Validation error",
        error=str(exc),
        url=str(request.url)
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "message": str(exc),
            "error_code": "VALIDATION_ERROR",
            "timestamp": time.time()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors"""
    logger.error(
        "Unexpected error",
        error=str(exc),
        error_type=type(exc).__name__,
        url=str(request.url),
        exc_info=True
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": "Internal server error",
            "error_code": "INTERNAL_ERROR",
            "timestamp": time.time()
        }
    )


# Health check endpoint
@app.get(
    "/health",
    response_model=HealthCheckResponse,
    tags=["Health"]
)
async def health_check() -> HealthCheckResponse:
    """Health check endpoint"""
    services_status = {}
    
    try:
        # Check Redis connection
        await cache_manager.redis.ping()
        services_status["redis"] = "healthy"
    except Exception:
        services_status["redis"] = "unhealthy"
    
    # Overall status
    overall_status = "healthy" if all(
        status == "healthy" for status in services_status.values()
    ) else "unhealthy"
    
    return HealthCheckResponse(
        status=overall_status,
        version=settings.app_version,
        services=services_status
    )


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "docs_url": "/docs" if settings.debug else None,
        "health_check": "/health"
    }


# Include routers
app.include_router(fc_data_router)
app.include_router(fc_trading_router)
app.include_router(fc_trading_additional_router)


# Custom OpenAPI schema
def custom_openapi():
    """Custom OpenAPI schema"""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=settings.app_name,
        version=settings.app_version,
        description=app.description,
        routes=app.routes,
    )
    
    # Add security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Access token obtained from /fc-trading/auth/token"
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        workers=settings.workers,
        log_level=settings.log_level.lower(),
        reload=settings.debug,
        access_log=True
    )
