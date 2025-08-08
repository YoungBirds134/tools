"""
Order Management Service - Simplified FastAPI Application
Production-ready microservice for managing trading orders - Standalone Mode.
"""

import os
import sys
from datetime import datetime
from typing import Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Local configuration
from .config import settings

# Initialize FastAPI application
app = FastAPI(
    title="Order Management Service",
    description="Production-ready microservice for managing trading orders in Vietnamese stock market",
    version="1.0.0",
    debug=settings.debug
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=settings.allowed_methods,
    allow_headers=settings.allowed_headers,
)

# Health check endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Order Management Service",
        "status": "running",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "mode": "standalone",
        "message": "Service is operational!"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "order_management", 
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "mode": "standalone"
    }

@app.get("/info")
async def service_info():
    """Service information endpoint"""
    return {
        "service": "Order Management Service",
        "version": "1.0.0", 
        "description": "Production-ready microservice for managing trading orders",
        "features": [
            "Vietnamese stock market support",
            "Order lifecycle management", 
            "Portfolio tracking",
            "Risk management",
            "Real-time position updates"
        ],
        "markets": ["HOSE", "HNX", "UPCOM"],
        "order_types": ["LO", "ATO", "ATC", "MTL", "MOK", "MAK", "PLO"],
        "status": "operational",
        "mode": "standalone"
    }

# API status endpoint
@app.get("/api/status")
async def api_status():
    """API status endpoint"""
    return {
        "api": "Order Management API",
        "status": "active",
        "endpoints": len(app.routes),
        "timestamp": datetime.utcnow().isoformat(),
        "environment": settings.environment,
        "debug": settings.debug
    }

# Trading session endpoint
@app.get("/api/trading-session")
async def get_trading_session():
    """Get current trading session information"""
    now = datetime.now()
    
    # Vietnam trading hours (approximate)
    if 9 <= now.hour < 11 or 13 <= now.hour < 15:
        session_status = "open"
    else:
        session_status = "closed"
    
    return {
        "session_status": session_status,
        "current_time": now.isoformat(),
        "timezone": "Asia/Ho_Chi_Minh",
        "markets": {
            "HOSE": {"status": session_status, "name": "Ho Chi Minh Stock Exchange"},
            "HNX": {"status": session_status, "name": "Hanoi Stock Exchange"},
            "UPCOM": {"status": session_status, "name": "Unlisted Public Company Market"}
        }
    }

# Mock endpoints for demonstration
@app.get("/api/orders")
async def get_orders():
    """Get orders (mock implementation)"""
    return {
        "orders": [],
        "total": 0,
        "message": "Service running in standalone mode - no actual orders",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/api/positions") 
async def get_positions():
    """Get positions (mock implementation)"""
    return {
        "positions": [],
        "total": 0,
        "message": "Service running in standalone mode - no actual positions",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/api/accounts")
async def get_accounts():
    """Get accounts (mock implementation)"""
    return {
        "accounts": [],
        "total": 0,
        "message": "Service running in standalone mode - no actual accounts",
        "timestamp": datetime.utcnow().isoformat()
    }

# Configuration endpoint
@app.get("/api/config")
async def get_config():
    """Get service configuration"""
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "debug": settings.debug,
        "host": settings.host,
        "port": settings.port,
        "timestamp": datetime.utcnow().isoformat()
    }

# Exception handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found", 
            "message": "The requested endpoint was not found",
            "timestamp": datetime.utcnow().isoformat()
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "timestamp": datetime.utcnow().isoformat()
        }
    )

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Order Management Service (Standalone Mode)...")
    uvicorn.run(
        "app.main_simple:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )
