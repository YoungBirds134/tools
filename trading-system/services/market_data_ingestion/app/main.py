"""
Market Data Ingestion Service - FastAPI Application
Enhanced service for Vietnamese stock market data ingestion from SSI FastConnect
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import asyncio
import structlog
from datetime import datetime
from typing import Dict, Any

from .config import settings
from .services.ssi_client import SSIDataClient
from .models import (
    MarketDataRequest, MarketDataResponse, HistoricalDataRequest,
    StreamSubscriptionRequest, QuoteData, TradeData, OrderBookData,
    IndexData, MarketDataError
)


# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer() if settings.log_json else structlog.dev.ConsoleRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)


# Global instances
ssi_client: SSIDataClient = None
background_tasks_running = False


async def startup_tasks():
    """Initialize services on startup"""
    global ssi_client, background_tasks_running
    
    logger.info("Starting Market Data Ingestion Service",
               version=settings.app_version,
               environment=settings.environment)
    
    # Initialize SSI client
    ssi_client = SSIDataClient()
    await ssi_client.connect()
    
    # Start background tasks
    if settings.enable_data_collection:
        background_tasks_running = True
        asyncio.create_task(periodic_data_collection())
    
    logger.info("Market Data Ingestion Service started successfully")


async def shutdown_tasks():
    """Cleanup on shutdown"""
    global ssi_client, background_tasks_running
    
    logger.info("Shutting down Market Data Ingestion Service")
    
    # Stop background tasks
    background_tasks_running = False
    
    # Disconnect SSI client
    if ssi_client:
        await ssi_client.disconnect()
    
    logger.info("Market Data Ingestion Service stopped")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    await startup_tasks()
    yield
    await shutdown_tasks()


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Enhanced market data ingestion service for Vietnamese stock exchanges",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=settings.allowed_methods,
    allow_headers=settings.allowed_headers,
)

if settings.is_production:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["localhost", "127.0.0.1", settings.host]
    )


# Dependency to get SSI client
async def get_ssi_client() -> SSIDataClient:
    """Dependency to get SSI client instance"""
    if ssi_client is None:
        raise HTTPException(status_code=503, detail="SSI client not initialized")
    return ssi_client


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error("Unhandled exception", 
                path=request.url.path,
                method=request.method,
                error=str(exc),
                exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc) if settings.debug else "Server error"}
    )


# Health check endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.app_version,
        "environment": settings.environment
    }


@app.get("/health/ready")
async def readiness_check(client: SSIDataClient = Depends(get_ssi_client)):
    """Readiness check endpoint"""
    try:
        stats = client.get_stats()
        is_ready = stats["is_authenticated"] and stats["circuit_breaker_state"] != "OPEN"
        
        return {
            "status": "ready" if is_ready else "not_ready",
            "timestamp": datetime.utcnow().isoformat(),
            "ssi_client_stats": stats
        }
    except Exception as e:
        logger.error("Readiness check failed", error=str(e))
        raise HTTPException(status_code=503, detail="Service not ready")


@app.get("/metrics")
async def get_metrics(client: SSIDataClient = Depends(get_ssi_client)):
    """Get service metrics"""
    stats = client.get_stats()
    
    return {
        "service_metrics": {
            "uptime_seconds": (datetime.utcnow() - datetime.utcnow()).total_seconds(),  # Placeholder
            "total_requests": stats["request_count"],
            "error_count": stats["error_count"],
            "error_rate": stats["error_rate"],
            "last_request_time": stats["last_request_time"]
        },
        "ssi_client_metrics": stats,
        "timestamp": datetime.utcnow().isoformat()
    }


# Market data endpoints
@app.post("/api/v1/market-data", response_model=MarketDataResponse)
async def get_market_data(
    request: MarketDataRequest,
    client: SSIDataClient = Depends(get_ssi_client)
):
    """Get real-time market data for specified symbols"""
    try:
        logger.info("Market data request", 
                   symbols=request.symbols,
                   data_types=request.data_types)
        
        # Get data from SSI
        raw_data = await client.get_market_data(request.symbols, request.data_types)
        
        # Process and structure response
        processed_data = {}
        for symbol in request.symbols:
            try:
                quote = await client.get_quote_data(symbol)
                processed_data[symbol] = quote.dict()
            except Exception as e:
                logger.warning("Failed to get data for symbol", symbol=symbol, error=str(e))
                processed_data[symbol] = {"error": str(e)}
        
        return MarketDataResponse(
            data=processed_data,
            total_symbols=len(request.symbols),
            session_info={
                "current_session": client._determine_current_session().value,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
    except Exception as e:
        logger.error("Market data request failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/quote/{symbol}", response_model=QuoteData)
async def get_quote(
    symbol: str,
    client: SSIDataClient = Depends(get_ssi_client)
):
    """Get detailed quote data for a specific symbol"""
    try:
        symbol = symbol.upper()
        logger.info("Quote request", symbol=symbol)
        
        quote = await client.get_quote_data(symbol)
        return quote
        
    except Exception as e:
        logger.error("Quote request failed", symbol=symbol, error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/trades/{symbol}")
async def get_trades(
    symbol: str,
    limit: int = 100,
    client: SSIDataClient = Depends(get_ssi_client)
):
    """Get recent trade data for a symbol"""
    try:
        symbol = symbol.upper()
        limit = min(max(limit, 1), 1000)  # Limit between 1-1000
        
        logger.info("Trades request", symbol=symbol, limit=limit)
        
        trades = await client.get_trade_data(symbol, limit)
        return {
            "symbol": symbol,
            "trades": [trade.dict() for trade in trades],
            "count": len(trades),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error("Trades request failed", symbol=symbol, error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/orderbook/{symbol}", response_model=OrderBookData)
async def get_order_book(
    symbol: str,
    depth: int = 10,
    client: SSIDataClient = Depends(get_ssi_client)
):
    """Get order book data for a symbol"""
    try:
        symbol = symbol.upper()
        depth = min(max(depth, 1), 10)  # Limit between 1-10
        
        logger.info("Order book request", symbol=symbol, depth=depth)
        
        order_book = await client.get_order_book(symbol, depth)
        return order_book
        
    except Exception as e:
        logger.error("Order book request failed", symbol=symbol, error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/historical")
async def get_historical_data(
    request: HistoricalDataRequest,
    client: SSIDataClient = Depends(get_ssi_client)
):
    """Get historical price data"""
    try:
        logger.info("Historical data request", 
                   symbol=request.symbol,
                   from_date=request.from_date,
                   to_date=request.to_date,
                   resolution=request.resolution)
        
        historical_data = await client.get_historical_data(request)
        
        return {
            "symbol": request.symbol,
            "from_date": request.from_date.isoformat(),
            "to_date": request.to_date.isoformat(),
            "resolution": request.resolution,
            "data": historical_data,
            "count": len(historical_data),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error("Historical data request failed", 
                    symbol=request.symbol, error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/indices")
async def get_indices(
    indices: str = "VN-Index,HNX-Index,UPCOM-Index",
    client: SSIDataClient = Depends(get_ssi_client)
):
    """Get market indices data"""
    try:
        index_codes = [idx.strip() for idx in indices.split(",")]
        logger.info("Indices request", indices=index_codes)
        
        indices_data = await client.get_index_data(index_codes)
        
        return {
            "indices": [index.dict() for index in indices_data],
            "count": len(indices_data),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error("Indices request failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


# Background tasks
async def periodic_data_collection():
    """Background task for periodic data collection"""
    logger.info("Starting periodic data collection")
    
    while background_tasks_running:
        try:
            if ssi_client and settings.enable_data_collection:
                # Collect data for default symbols
                for symbol in settings.market_symbols:
                    try:
                        quote = await ssi_client.get_quote_data(symbol)
                        # Here you would typically store to database or send to Kafka
                        logger.debug("Collected data for symbol", symbol=symbol)
                    except Exception as e:
                        logger.warning("Failed to collect data for symbol", 
                                     symbol=symbol, error=str(e))
            
            await asyncio.sleep(settings.data_refresh_interval)
            
        except Exception as e:
            logger.error("Error in periodic data collection", error=str(e))
            await asyncio.sleep(30)  # Wait longer on error


# WebSocket endpoint for real-time streaming
@app.websocket("/ws/stream")
async def websocket_stream(websocket):
    """WebSocket endpoint for real-time data streaming"""
    await websocket.accept()
    
    try:
        # Wait for subscription request
        subscription_data = await websocket.receive_json()
        request = StreamSubscriptionRequest(**subscription_data)
        
        logger.info("WebSocket subscription", 
                   symbols=request.symbols,
                   data_types=request.data_types)
        
        # Start streaming data
        if ssi_client:
            async for data in ssi_client.subscribe_real_time(request.symbols, request.data_types):
                await websocket.send_json(data)
        
    except Exception as e:
        logger.error("WebSocket error", error=str(e))
        await websocket.send_json({
            "type": "error",
            "message": str(e),
            "timestamp": datetime.utcnow().isoformat()
        })
    finally:
        await websocket.close()


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        workers=settings.workers,
        reload=settings.reload,
        log_level=settings.log_level.lower()
    )
