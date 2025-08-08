#!/usr/bin/env python3

import uvicorn
from app.main_simple import app

# Get configuration
try:
    from app.config import settings
    host = settings.host
    port = settings.port
    debug = settings.debug
except ImportError:
    # Fallback configuration
    host = "0.0.0.0"
    port = 8001
    debug = True

if __name__ == "__main__":
    print("🚀 Starting Order Management Service...")
    print(f"📍 Server will run at: http://{host}:{port}")
    print("📝 API Documentation will be available at: http://localhost:8001/docs")
    print("🔍 Health check: http://localhost:8001/health")
    
    uvicorn.run(
        "app.main_simple:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info",
        access_log=True
    )
