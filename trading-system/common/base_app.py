"""
Base FastAPI application factory and common middleware.
"""

import time
from typing import Any, Callable, Dict, List, Optional

from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException

from .config import BaseConfig, get_settings
from .logging import get_logger
from .utils import generate_request_id

logger = get_logger(__name__)


class BaseApplication:
    """Base application factory for microservices."""
    
    def __init__(
        self, 
        service_name: str,
        config: Optional[BaseConfig] = None,
        custom_config: Optional[Dict[str, Any]] = None
    ):
        """Initialize base application."""
        self.service_name = service_name
        self.config = config or get_settings()
        self.custom_config = custom_config or {}
        
        # Create FastAPI app
        self.app = FastAPI(
            title=f"{self.config.app_name} - {service_name}",
            version=self.config.app_version,
            debug=self.config.debug,
            docs_url=self.config.docs_url,
            redoc_url=self.config.redoc_url,
            openapi_url=self.config.openapi_url,
        )
        
        # Setup middleware and handlers
        self._setup_middleware()
        self._setup_exception_handlers()
        self._setup_health_checks()
    
    def _setup_middleware(self):
        """Setup application middleware."""
        
        # Request ID middleware
        @self.app.middleware("http")
        async def add_request_id(request: Request, call_next: Callable):
            request_id = generate_request_id()
            request.state.request_id = request_id
            
            start_time = time.time()
            
            # Process request
            response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Add headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = str(round(duration, 4))
            
            # Log request
            logger.log_api_request(
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                duration=duration,
                request_id=request_id,
                user_agent=request.headers.get("user-agent"),
                ip=request.client.host if request.client else "unknown"
            )
            
            return response
        
        # CORS middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=self.config.cors_origins,
            allow_credentials=self.config.cors_credentials,
            allow_methods=self.config.cors_methods,
            allow_headers=self.config.cors_headers,
        )
        
        # Gzip compression
        self.app.add_middleware(GZipMiddleware, minimum_size=1000)
    
    def _setup_exception_handlers(self):
        """Setup exception handlers."""
        
        @self.app.exception_handler(HTTPException)
        async def http_exception_handler(request: Request, exc: HTTPException):
            """Handle HTTP exceptions."""
            logger.warning(
                f"HTTP Exception: {exc.status_code} - {exc.detail}",
                request_id=getattr(request.state, "request_id", "unknown"),
                path=request.url.path,
                method=request.method
            )
            
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "error": "HTTP Exception",
                    "message": exc.detail,
                    "status_code": exc.status_code,
                    "request_id": getattr(request.state, "request_id", "unknown")
                }
            )
        
        @self.app.exception_handler(StarletteHTTPException)
        async def starlette_exception_handler(request: Request, exc: StarletteHTTPException):
            """Handle Starlette HTTP exceptions."""
            logger.warning(
                f"Starlette Exception: {exc.status_code} - {exc.detail}",
                request_id=getattr(request.state, "request_id", "unknown"),
                path=request.url.path,
                method=request.method
            )
            
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "error": "Server Error",
                    "message": exc.detail,
                    "status_code": exc.status_code,
                    "request_id": getattr(request.state, "request_id", "unknown")
                }
            )
        
        @self.app.exception_handler(RequestValidationError)
        async def validation_exception_handler(request: Request, exc: RequestValidationError):
            """Handle request validation errors."""
            logger.warning(
                f"Validation Error: {exc.errors()}",
                request_id=getattr(request.state, "request_id", "unknown"),
                path=request.url.path,
                method=request.method
            )
            
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={
                    "error": "Validation Error",
                    "message": "Request validation failed",
                    "details": exc.errors(),
                    "status_code": 422,
                    "request_id": getattr(request.state, "request_id", "unknown")
                }
            )
        
        @self.app.exception_handler(Exception)
        async def general_exception_handler(request: Request, exc: Exception):
            """Handle general exceptions."""
            logger.error(
                f"Unexpected error: {str(exc)}",
                request_id=getattr(request.state, "request_id", "unknown"),
                path=request.url.path,
                method=request.method,
                exc_info=True
            )
            
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": "Internal Server Error",
                    "message": "An unexpected error occurred",
                    "status_code": 500,
                    "request_id": getattr(request.state, "request_id", "unknown")
                }
            )
    
    def _setup_health_checks(self):
        """Setup health check endpoints."""
        
        @self.app.get("/health", tags=["Health"])
        async def health_check():
            """Basic health check endpoint."""
            return {
                "status": "healthy",
                "service": self.service_name,
                "version": self.config.app_version,
                "timestamp": time.time()
            }
        
        @self.app.get("/health/ready", tags=["Health"])
        async def readiness_check():
            """Readiness check endpoint for Kubernetes."""
            # TODO: Add actual readiness checks (database, redis, etc.)
            return {
                "status": "ready",
                "service": self.service_name,
                "checks": {
                    "database": "ok",  # Will be implemented per service
                    "redis": "ok",     # Will be implemented per service
                    "external_apis": "ok"  # Will be implemented per service
                }
            }
        
        @self.app.get("/health/live", tags=["Health"])
        async def liveness_check():
            """Liveness check endpoint for Kubernetes."""
            return {
                "status": "alive",
                "service": self.service_name,
                "timestamp": time.time()
            }
        
        @self.app.get("/metrics", tags=["Monitoring"])
        async def metrics_endpoint():
            """Prometheus metrics endpoint."""
            # TODO: Implement Prometheus metrics
            return {
                "message": "Metrics endpoint - TODO: Implement Prometheus metrics"
            }
    
    def add_router(self, router, prefix: str = "", tags: Optional[List[str]] = None):
        """Add router to application."""
        self.app.include_router(router, prefix=prefix, tags=tags)
    
    def add_startup_handler(self, handler: Callable):
        """Add startup event handler."""
        self.app.add_event_handler("startup", handler)
    
    def add_shutdown_handler(self, handler: Callable):
        """Add shutdown event handler."""
        self.app.add_event_handler("shutdown", handler)
    
    def get_app(self) -> FastAPI:
        """Get FastAPI application instance."""
        return self.app


def create_service_app(
    service_name: str,
    config: Optional[BaseConfig] = None,
    custom_config: Optional[Dict[str, Any]] = None
) -> FastAPI:
    """Factory function to create a FastAPI app for a microservice."""
    base_app = BaseApplication(service_name, config, custom_config)
    return base_app.get_app()


def create_service_with_base(
    service_name: str,
    config: Optional[BaseConfig] = None,
    custom_config: Optional[Dict[str, Any]] = None
) -> BaseApplication:
    """Factory function to create BaseApplication instance."""
    return BaseApplication(service_name, config, custom_config)
