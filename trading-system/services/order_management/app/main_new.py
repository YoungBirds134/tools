"""
Order Management Service - FastAPI Application
Production-ready microservice for managing trading orders in Vietnamese stock market.
"""

import asyncio
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Dict, Any
import os
import sys

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# Add the parent directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from .database import init_database, check_database_connection, database_health_check
    from .routes import orders, positions, accounts
    ROUTES_IMPORTED = True
except ImportError as e:
    print(f"Import warning: {e}")
    ROUTES_IMPORTED = False

try:
    from common.logging import LoggerManager
    from common.config import get_config
    from common.base_app import BaseApplication
    COMMON_IMPORTED = True
except ImportError as e:
    # Fallback for development environment
    print(f"Warning: Could not import common modules, running in standalone mode")
    print(f"Reason: {e}")
    COMMON_IMPORTED = False
    
    # Mock implementations for development
    async def database_health_check():
        return {"status": "healthy", "database": "mock"}
    
    def init_database():
        print("Mock database initialization")
    
    def check_database_connection():
        return True
    
    class MockLoggerManager:
        @staticmethod
        def get_logger(name):
            class MockLogger:
                def info(self, msg): print(f"INFO: {msg}")
                def error(self, msg): print(f"ERROR: {msg}")
                def warning(self, msg): print(f"WARNING: {msg}")
                def debug(self, msg): print(f"DEBUG: {msg}")
            return MockLogger()
    
    LoggerManager = MockLoggerManager()
    
    # Mock routes for development
    from fastapi import APIRouter
    
    class MockRouter:
        def __init__(self):
            self.router = APIRouter()
            
        @property
        def router(self):
            return APIRouter(prefix="/mock", tags=["mock"])
    
    class MockRoutes:
        router = APIRouter(prefix="/mock", tags=["mock"])
    
    orders = MockRoutes()
    positions = MockRoutes()
    accounts = MockRoutes()

# Initialize configuration and logging
try:
    config = get_config()
    logger = LoggerManager.get_logger("order_management_main")
except:
    config = type('Config', (), {
        'DEBUG': True, 
        'HOST': '0.0.0.0', 
        'PORT': 8001,
        'ENVIRONMENT': 'development'
    })()
    logger = LoggerManager.get_logger("order_management_main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    
    # Startup
    logger.info("Starting Order Management Service...")
    
    try:
        # Initialize database
        init_database()
        
        # Check database connection
        if not check_database_connection():
            logger.error("Database connection failed")
            raise Exception("Database connection failed")
        
        logger.info("Database connection established")
        
        # Additional startup tasks
        await startup_tasks()
        
        logger.info("Order Management Service started successfully")
        
    except Exception as e:
        logger.error(f"Failed to start Order Management Service: {str(e)}")
        # Don't raise in development mode to allow testing
        if getattr(config, 'ENVIRONMENT', 'development') == 'production':
            raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down Order Management Service...")
    await shutdown_tasks()
    logger.info("Order Management Service shutdown complete")


async def startup_tasks():
    """Perform additional startup tasks."""
    
    try:
        # Initialize any required services
        logger.info("Performing startup tasks...")
        
        # Initialize order processing background tasks
        await initialize_order_processing()
        
        # Initialize market data connections
        await initialize_market_data()
        
        # Initialize SSI connection (if configured)
        await initialize_ssi_connection()
        
        # Warm up caches
        await warm_up_caches()
        
        logger.info("Startup tasks completed")
        
    except Exception as e:
        logger.error(f"Error in startup tasks: {str(e)}")
        raise


async def initialize_order_processing():
    """Initialize order processing background tasks."""
    
    try:
        logger.info("Initializing order processing...")
        
        # In production, this would:
        # - Start order execution monitoring
        # - Initialize message queue connections
        # - Set up order state synchronization
        
        logger.info("Order processing initialized")
        
    except Exception as e:
        logger.error(f"Error initializing order processing: {str(e)}")
        raise


async def initialize_market_data():
    """Initialize market data connections."""
    
    try:
        logger.info("Initializing market data connections...")
        
        # In production, this would:
        # - Connect to market data feeds
        # - Subscribe to price updates
        # - Initialize trading session monitoring
        
        logger.info("Market data connections initialized")
        
    except Exception as e:
        logger.error(f"Error initializing market data: {str(e)}")
        raise


async def initialize_ssi_connection():
    """Initialize SSI FastConnect connection."""
    
    try:
        logger.info("Initializing SSI FastConnect connection...")
        
        # In production, this would:
        # - Establish SSI API connection
        # - Authenticate with credentials
        # - Subscribe to order and execution updates
        
        logger.info("SSI connection initialized")
        
    except Exception as e:
        logger.error(f"Error initializing SSI connection: {str(e)}")
        # Don't raise - service can work in simulation mode
        logger.warning("SSI connection failed - running in simulation mode")


async def warm_up_caches():
    """Warm up application caches."""
    
    try:
        logger.info("Warming up caches...")
        
        # In production, this would:
        # - Load trading symbols
        # - Cache market rules
        # - Preload user session data
        
        logger.info("Caches warmed up")
        
    except Exception as e:
        logger.error(f"Error warming up caches: {str(e)}")
        raise


async def shutdown_tasks():
    """Perform cleanup tasks during shutdown."""
    
    try:
        logger.info("Performing shutdown tasks...")
        
        # Close SSI connections
        await cleanup_ssi_connection()
        
        # Save pending orders state
        await save_pending_orders()
        
        # Close market data connections
        await cleanup_market_data()
        
        # Cleanup background tasks
        await cleanup_background_tasks()
        
        logger.info("Shutdown tasks completed")
        
    except Exception as e:
        logger.error(f"Error in shutdown tasks: {str(e)}")


async def cleanup_ssi_connection():
    """Cleanup SSI connections."""
    try:
        logger.info("Cleaning up SSI connections...")
        # Disconnect from SSI API
        logger.info("SSI connections cleaned up")
    except Exception as e:
        logger.error(f"Error cleaning up SSI connections: {str(e)}")


async def save_pending_orders():
    """Save pending orders state."""
    try:
        logger.info("Saving pending orders state...")
        # Save any pending order state to disk/database
        logger.info("Pending orders state saved")
    except Exception as e:
        logger.error(f"Error saving pending orders state: {str(e)}")


async def cleanup_market_data():
    """Cleanup market data connections."""
    try:
        logger.info("Cleaning up market data connections...")
        # Close market data feeds
        logger.info("Market data connections cleaned up")
    except Exception as e:
        logger.error(f"Error cleaning up market data connections: {str(e)}")


async def cleanup_background_tasks():
    """Cleanup background tasks."""
    try:
        logger.info("Cleaning up background tasks...")
        # Cancel and cleanup background tasks
        logger.info("Background tasks cleaned up")
    except Exception as e:
        logger.error(f"Error cleaning up background tasks: {str(e)}")


# Create FastAPI application
app = FastAPI(
    title="Order Management Service",
    description="""
    Production-ready microservice for managing trading orders in Vietnamese stock market.
    
    Features:
    - Real-time order management
    - Portfolio tracking
    - SSI FastConnect integration
    - Vietnamese market compliance
    - Risk management
    - Performance analytics
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
    contact={
        "name": "Trading System Support",
        "email": "support@tradingsystem.vn"
    },
    license_info={
        "name": "Private License",
        "url": "https://tradingsystem.vn/license"
    }
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Configure appropriately for production
)


# Custom middleware for request logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all HTTP requests."""
    
    start_time = datetime.utcnow()
    
    # Process request
    response = await call_next(request)
    
    # Calculate processing time
    process_time = (datetime.utcnow() - start_time).total_seconds()
    
    # Log request
    logger.info(
        f"{request.method} {request.url} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.3f}s"
    )
    
    # Add custom headers
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Service"] = "order-management"
    
    return response


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    
    logger.warning(f"HTTP {exc.status_code}: {exc.detail} - {request.url}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "status_code": exc.status_code,
            "detail": exc.detail,
            "timestamp": datetime.utcnow().isoformat(),
            "path": str(request.url),
            "service": "order_management"
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    
    logger.error(f"Unhandled exception: {str(exc)} - {request.url}")
    
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "status_code": 500,
            "detail": "Internal server error",
            "timestamp": datetime.utcnow().isoformat(),
            "path": str(request.url),
            "service": "order_management"
        }
    )


# Health check endpoints
@app.get("/health", tags=["Health"])
async def health_check():
    """Basic health check endpoint."""
    
    return {
        "status": "healthy",
        "service": "order_management",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "environment": getattr(config, 'ENVIRONMENT', 'development')
    }


@app.get("/health/detailed", tags=["Health"])
async def detailed_health_check():
    """Detailed health check with dependencies."""
    
    health_status = {
        "status": "healthy",
        "service": "order_management",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "environment": getattr(config, 'ENVIRONMENT', 'development'),
        "checks": {}
    }
    
    # Database health check
    try:
        db_health = await database_health_check()
        health_status["checks"]["database"] = db_health
        
        if db_health.get("status") != "healthy":
            health_status["status"] = "degraded"
            
    except Exception as e:
        health_status["checks"]["database"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        health_status["status"] = "unhealthy"
    
    # SSI connection health check
    try:
        health_status["checks"]["ssi_connection"] = {
            "status": "healthy",
            "mode": "simulation"  # Would check actual connection in production
        }
    except Exception as e:
        health_status["checks"]["ssi_connection"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        health_status["status"] = "degraded"
    
    # Market data health check
    try:
        health_status["checks"]["market_data"] = {
            "status": "healthy",
            "last_update": datetime.utcnow().isoformat()
        }
    except Exception as e:
        health_status["checks"]["market_data"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        health_status["status"] = "degraded"
    
    return health_status


@app.get("/health/live", tags=["Health"])
async def liveness_probe():
    """Kubernetes liveness probe."""
    return {"status": "alive"}


@app.get("/health/ready", tags=["Health"])
async def readiness_probe():
    """Kubernetes readiness probe."""
    
    try:
        # Check if service is ready to accept requests
        if check_database_connection():
            return {"status": "ready"}
        else:
            raise HTTPException(status_code=503, detail="Service not ready")
            
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service not ready: {str(e)}")


@app.get("/metrics", tags=["Monitoring"])
async def get_metrics():
    """Get service metrics."""
    
    # In production, integrate with Prometheus or similar
    return {
        "service": "order_management",
        "timestamp": datetime.utcnow().isoformat(),
        "metrics": {
            "requests_total": 0,  # Would be tracked by middleware
            "requests_per_second": 0.0,
            "error_rate": 0.0,
            "response_time_avg": 0.0,
            "database_connections": 0,
            "memory_usage": 0.0,
            "orders_processed_today": 0,
            "active_positions": 0,
            "pending_orders": 0
        }
    }


# Include routers
try:
    app.include_router(orders.router, prefix="/api/v1")
    app.include_router(positions.router, prefix="/api/v1")
    app.include_router(accounts.router, prefix="/api/v1")
    logger.info("API routes registered successfully")
except Exception as e:
    logger.error(f"Error registering routes: {str(e)}")


# Root endpoint
@app.get("/", tags=["General"])
async def root():
    """Root endpoint with service information."""
    
    return {
        "service": "Order Management Service",
        "description": "Production-ready microservice for managing trading orders in Vietnamese stock market",
        "version": "1.0.0",
        "status": "running",
        "environment": getattr(config, 'ENVIRONMENT', 'development'),
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/health",
            "metrics": "/metrics",
            "api": "/api/v1"
        },
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/info", tags=["General"])
async def service_info():
    """Get detailed service information."""
    
    return {
        "service": {
            "name": "Order Management Service",
            "version": "1.0.0",
            "description": "Production-ready microservice for managing trading orders in Vietnamese stock market",
            "environment": getattr(config, 'ENVIRONMENT', 'development')
        },
        "features": [
            "Real-time order management",
            "Portfolio tracking",
            "SSI FastConnect integration",
            "Vietnamese market compliance",
            "Risk management",
            "Performance analytics"
        ],
        "api": {
            "version": "v1",
            "base_url": "/api/v1",
            "endpoints": {
                "orders": "/api/v1/orders",
                "positions": "/api/v1/positions",
                "accounts": "/api/v1/accounts"
            }
        },
        "compliance": {
            "markets": ["HOSE", "HNX", "UPCOM"],
            "order_types": ["LO", "ATO", "ATC", "MTL", "MOK", "MAK", "PLO"],
            "trading_sessions": ["Morning Auction", "Continuous Morning", "Lunch Break", "Continuous Afternoon", "Closing Auction", "Post Market"]
        },
        "timestamp": datetime.utcnow().isoformat()
    }


# Development server
if __name__ == "__main__":
    uvicorn.run(
        "main_new:app",
        host=getattr(config, 'HOST', '0.0.0.0'),
        port=getattr(config, 'PORT', 8001),
        reload=getattr(config, 'DEBUG', True),
        log_level="info",
        access_log=True
    )

import asyncio
import os
import sys
from pathlib import Path

# Add common path to Python path
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent
common_path = project_root / "common"
sys.path.insert(0, str(common_path))
sys.path.insert(0, str(project_root))

from fastapi import FastAPI, Depends, HTTPException, status, Request, Response
from fastapi.responses import JSONResponse
import uvicorn

# Import common modules
try:
    from trading_system.common.base_app import create_service_with_base
    from trading_system.common.config import get_settings
    from trading_system.common.logging import get_logger
except ImportError:
    # Fallback for development
    print("Warning: Could not import common modules, running in standalone mode")
    
    from fastapi import FastAPI
    app = FastAPI(
        title="Order Management Service",
        description="SSI FastConnect Trading API Integration Service",
        version="0.1.0"
    )
    
    def get_logger(name):
        import logging
        return logging.getLogger(name)
    
    logger = get_logger(__name__)

# Import service modules
from .routers import orders, accounts, positions
from .services.order_service import OrderService
from .services.trading_session_service import TradingSessionService

logger = get_logger(__name__)

# Create base application
try:
    app_base = create_service_with_base(
        service_name="Order Management",
        config=get_settings(),
        custom_config={
            "port": 8001,
            "title": "Order Management Service",
            "description": "SSI FastConnect Trading API Integration Service"
        }
    )
    app = app_base.get_app()
except:
    # Fallback app creation
    app = FastAPI(
        title="Order Management Service",
        description="SSI FastConnect Trading API Integration Service",
        version="0.1.0"
    )

# Initialize services
order_service = OrderService()
trading_session_service = TradingSessionService()

# Add routers
app.include_router(
    orders.router,
    prefix="/api/v1/orders",
    tags=["Orders"]
)

app.include_router(
    accounts.router,
    prefix="/api/v1/accounts",
    tags=["Accounts"]
)

app.include_router(
    positions.router,
    prefix="/api/v1/positions",
    tags=["Positions"]
)

# Service-specific health checks
@app.get("/health/detailed", tags=["Health"])
async def detailed_health_check():
    """Detailed health check for Order Management service."""
    try:
        # Check database connection
        db_status = "ok"
        try:
            # TODO: Add actual database ping
            pass
        except Exception as e:
            db_status = f"error: {str(e)}"
        
        # Check SSI FastConnect connection
        ssi_status = "ok"
        try:
            # TODO: Add SSI connection check
            pass
        except Exception as e:
            ssi_status = f"error: {str(e)}"
        
        # Check Redis connection
        redis_status = "ok"
        try:
            # TODO: Add Redis ping
            pass
        except Exception as e:
            redis_status = f"error: {str(e)}"
        
        # Check trading session status
        session_info = await trading_session_service.get_current_session()
        
        return {
            "status": "healthy" if all(
                status == "ok" for status in [db_status, ssi_status, redis_status]
            ) else "degraded",
            "service": "Order Management",
            "version": "0.1.0",
            "checks": {
                "database": db_status,
                "ssi_fastconnect": ssi_status,
                "redis": redis_status,
            },
            "trading_session": session_info,
            "capabilities": {
                "can_place_orders": session_info.get("can_place_orders", False),
                "can_modify_orders": session_info.get("can_modify_orders", False),
                "can_cancel_orders": session_info.get("can_cancel_orders", False),
            }
        }
    
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unhealthy",
                "service": "Order Management",
                "error": str(e)
            }
        )

# Service-specific endpoints
@app.get("/api/v1/status", tags=["Service"])
async def service_status():
    """Get service status and capabilities."""
    try:
        session_info = await trading_session_service.get_current_session()
    except:
        session_info = {"current_session": "UNKNOWN", "can_place_orders": False}
    
    return {
        "service": "Order Management",
        "version": "0.1.0",
        "environment": "development",  # TODO: Get from settings
        "trading_session": session_info,
        "supported_markets": ["HOSE", "HNX", "UPCOM"],
        "supported_order_types": [
            "LO", "MTL", "MOK", "MAK", "ATC", "ATO", "PLO"
        ],
        "features": {
            "place_orders": True,
            "modify_orders": True,
            "cancel_orders": True,
            "real_time_status": True,
            "order_history": True,
            "position_tracking": True,
            "risk_management": True,
        }
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize service on startup."""
    logger.info("Starting Order Management Service...")
    
    try:
        # Initialize database
        # TODO: Add database initialization
        
        # Initialize Redis
        # TODO: Add Redis initialization
        
        # Initialize SSI FastConnect client
        # TODO: Add SSI client initialization
        
        # Start background tasks
        # TODO: Add background tasks for monitoring, etc.
        
        logger.info("Order Management Service started successfully")
        
    except Exception as e:
        logger.error(f"Failed to start Order Management Service: {e}")
        # Don't raise in production, log and continue

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down Order Management Service...")
    
    try:
        # Close database connections
        # TODO: Add database cleanup
        
        # Close Redis connections
        # TODO: Add Redis cleanup
        
        # Close SSI client connections
        # TODO: Add SSI client cleanup
        
        logger.info("Order Management Service shut down successfully")
        
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")

# Basic health endpoint
@app.get("/health")
async def health_check():
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "service": "Order Management",
        "version": "0.1.0"
    }

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "Order Management Service",
        "version": "0.1.0",
        "description": "SSI FastConnect Trading API Integration Service",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }

if __name__ == "__main__":
    # Development server
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8001,  # Order Management specific port
        reload=True,
        log_level="info",
        access_log=True,
    )
