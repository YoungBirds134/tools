"""
Main FastAPI application for notification service
Production-ready setup with middleware, logging, and error handling
"""

import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from telegram import Bot
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

from .core.config import settings
from .api.routers import notifications_router, users_router, health_router
from .telegram.handlers import TelegramHandlers
from .telegram.bot import NotificationBot

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global variables for telegram bot
telegram_app = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan manager
    Handles startup and shutdown events
    """
    global telegram_app
    
    # Startup
    logger.info("🚀 Starting Notification Service...")
    
    try:
        # Initialize Telegram bot if token is provided
        if settings.TELEGRAM_BOT_TOKEN:
            logger.info("🤖 Initializing Telegram bot...")
            
            # Create telegram application
            telegram_app = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
            
            # Initialize handlers
            handlers = TelegramHandlers()
            
            # Add command handlers
            telegram_app.add_handler(CommandHandler("start", handlers.start_command))
            telegram_app.add_handler(CommandHandler("help", handlers.help_command))
            telegram_app.add_handler(CommandHandler("menu", handlers.menu_command))
            telegram_app.add_handler(CommandHandler("status", handlers.status_command))
            
            # Add callback query handler
            telegram_app.add_handler(CallbackQueryHandler(handlers.handle_callback_query))
            
            # Start telegram bot
            await telegram_app.initialize()
            await telegram_app.start()
            
            # Start polling in background
            if not settings.WEBHOOK_MODE:
                logger.info("📡 Starting Telegram polling...")
                asyncio.create_task(telegram_app.updater.start_polling())
            
            logger.info("✅ Telegram bot initialized successfully")
        
        else:
            logger.warning("⚠️ Telegram bot token not provided, skipping bot initialization")
        
        logger.info("🎯 Notification Service started successfully")
        
    except Exception as e:
        logger.error(f"❌ Error during startup: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Notification Service...")
    
    try:
        if telegram_app:
            logger.info("🔌 Stopping Telegram bot...")
            await telegram_app.stop()
            await telegram_app.shutdown()
            logger.info("✅ Telegram bot stopped")
        
        logger.info("✅ Notification Service shutdown complete")
        
    except Exception as e:
        logger.error(f"❌ Error during shutdown: {e}")


# Create FastAPI application
app = FastAPI(
    title="Trading Notification Service",
    description="Enterprise-grade notification service for trading platform",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)


# Custom middleware for request logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests"""
    start_time = asyncio.get_event_loop().time()
    
    response = await call_next(request)
    
    process_time = asyncio.get_event_loop().time() - start_time
    
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.3f}s"
    )
    
    return response


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": "2025-01-16T10:30:00Z"
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "status_code": 500,
            "timestamp": "2025-01-16T10:30:00Z"
        }
    )


# Include routers
app.include_router(notifications_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(health_router, prefix="/api/v1")


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with service information"""
    return {
        "service": "Trading Notification Service",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs" if settings.DEBUG else "disabled",
        "health": "/api/v1/health/",
        "timestamp": "2025-01-16T10:30:00Z"
    }


# Webhook endpoint for Telegram (if using webhook mode)
@app.post("/webhook/telegram")
async def telegram_webhook(request: Request):
    """Handle Telegram webhook updates"""
    if not settings.WEBHOOK_MODE or not telegram_app:
        raise HTTPException(status_code=404, detail="Webhook not configured")
    
    try:
        update_data = await request.json()
        update = Update.de_json(update_data, telegram_app.bot)
        
        # Process update
        await telegram_app.process_update(update)
        
        return {"status": "ok"}
        
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail="Error processing update")


# Development helper endpoints
if settings.DEBUG:
    
    @app.get("/debug/info")
    async def debug_info():
        """Debug information (only in development)"""
        return {
            "settings": {
                "debug": settings.DEBUG,
                "log_level": settings.LOG_LEVEL,
                "telegram_enabled": bool(settings.TELEGRAM_BOT_TOKEN),
                "redis_url": settings.REDIS_URL[:20] + "...",
                "webhook_mode": settings.WEBHOOK_MODE
            },
            "environment": "development",
            "telegram_app": bool(telegram_app),
            "timestamp": "2025-01-16T10:30:00Z"
        }
    
    @app.post("/debug/test-notification/{user_id}")
    async def debug_test_notification(user_id: str, message: str = "Test notification"):
        """Send debug test notification"""
        from .services.notification_service import NotificationService
        from .models.notification_models import NotificationType, NotificationPriority
        
        service = NotificationService()
        
        result = await service.send_notification(
            user_id=user_id,
            notification_type=NotificationType.SYSTEM_MAINTENANCE,
            title="🔧 Debug Test",
            message=f"Debug test notification: {message}",
            priority=NotificationPriority.LOW
        )
        
        return result


if __name__ == "__main__":
    import uvicorn
    
    logger.info("🚀 Starting Notification Service in development mode...")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level=settings.LOG_LEVEL.lower()
    )
