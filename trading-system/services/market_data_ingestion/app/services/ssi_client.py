"""
SSI FastConnect Data Client for Market Data Ingestion
Enhanced client for real-time and historical market data from Vietnamese exchanges
"""

import asyncio
import aiohttp
import json
import base64
import hashlib
import hmac
from typing import Dict, List, Optional, Any, AsyncGenerator
from datetime import datetime, timedelta
from decimal import Decimal
import structlog
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from ..config import settings
from ..models import (
    QuoteData, TradeData, OrderBookData, IndexData, MarketNewsData,
    MarketDataRequest, HistoricalDataRequest, StreamSubscriptionRequest,
    MarketEnum, DataTypeEnum, SessionEnum
)


logger = structlog.get_logger(__name__)


class SSIDataClientError(Exception):
    """Base exception for SSI data client"""
    pass


class SSIAuthenticationError(SSIDataClientError):
    """Authentication related errors"""
    pass


class SSIRateLimitError(SSIDataClientError):
    """Rate limit exceeded"""
    pass


class SSIDataUnavailableError(SSIDataClientError):
    """Requested data is not available"""
    pass


class CircuitBreakerOpen(SSIDataClientError):
    """Circuit breaker is open"""
    pass


class CircuitBreaker:
    """Simple circuit breaker implementation"""
    
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    def call(self, func):
        """Decorator for circuit breaker"""
        async def wrapper(*args, **kwargs):
            if self.state == "OPEN":
                if datetime.utcnow().timestamp() - self.last_failure_time < self.timeout:
                    raise CircuitBreakerOpen("Circuit breaker is open")
                else:
                    self.state = "HALF_OPEN"
            
            try:
                result = await func(*args, **kwargs)
                if self.state == "HALF_OPEN":
                    self.reset()
                return result
            except Exception as e:
                self.record_failure()
                raise e
        
        return wrapper
    
    def record_failure(self):
        """Record a failure"""
        self.failure_count += 1
        self.last_failure_time = datetime.utcnow().timestamp()
        
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            logger.warning("Circuit breaker opened", 
                         failure_count=self.failure_count,
                         threshold=self.failure_threshold)
    
    def reset(self):
        """Reset the circuit breaker"""
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"
        logger.info("Circuit breaker reset")


class RateLimiter:
    """Token bucket rate limiter"""
    
    def __init__(self, requests_per_minute: int = 100):
        self.capacity = requests_per_minute
        self.tokens = requests_per_minute
        self.last_refill = datetime.utcnow()
        self.refill_rate = requests_per_minute / 60.0  # tokens per second
    
    async def acquire(self) -> bool:
        """Acquire a token, returns True if successful"""
        now = datetime.utcnow()
        elapsed = (now - self.last_refill).total_seconds()
        
        # Refill tokens
        tokens_to_add = elapsed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill = now
        
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        
        return False


class SSIDataClient:
    """Enhanced SSI FastConnect client for market data"""
    
    def __init__(self):
        self.consumer_id = settings.consumer_id
        self.consumer_secret = settings.consumer_secret
        self.private_key = base64.b64decode(settings.private_key)
        self.public_key = base64.b64decode(settings.public_key)
        
        self.trading_url = settings.fc_trading_url.rstrip('/')
        self.data_url = settings.fc_data_url.rstrip('/')
        self.stream_url = settings.fc_stream_url.rstrip('/')
        
        self.session: Optional[aiohttp.ClientSession] = None
        self.access_token: Optional[str] = None
        self.token_expires_at: Optional[datetime] = None
        
        # Resilience patterns
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=settings.circuit_breaker_failure_threshold,
            timeout=settings.circuit_breaker_timeout
        )
        self.rate_limiter = RateLimiter(settings.rate_limit_requests)
        
        # Performance tracking
        self.request_count = 0
        self.error_count = 0
        self.last_request_time = None
        
        logger.info("SSI Data Client initialized",
                   trading_url=self.trading_url,
                   data_url=self.data_url,
                   stream_url=self.stream_url)
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.disconnect()
    
    async def connect(self):
        """Initialize HTTP session and authenticate"""
        if self.session is None:
            timeout = aiohttp.ClientTimeout(total=settings.http_timeout)
            connector = aiohttp.TCPConnector(
                limit=settings.http_max_connections,
                limit_per_host=20
            )
            self.session = aiohttp.ClientSession(
                timeout=timeout,
                connector=connector,
                headers={
                    "User-Agent": f"{settings.app_name}/{settings.app_version}",
                    "Content-Type": "application/json"
                }
            )
        
        if not self.access_token or self._is_token_expired():
            await self._authenticate()
        
        logger.info("SSI Data Client connected")
    
    async def disconnect(self):
        """Close HTTP session"""
        if self.session:
            await self.session.close()
            self.session = None
        logger.info("SSI Data Client disconnected")
    
    def _is_token_expired(self) -> bool:
        """Check if access token is expired"""
        if not self.token_expires_at:
            return True
        return datetime.utcnow() >= self.token_expires_at - timedelta(minutes=5)
    
    def _create_signature(self, method: str, url: str, body: str = "") -> str:
        """Create HMAC signature for request authentication"""
        timestamp = str(int(datetime.utcnow().timestamp() * 1000))
        message = f"{method}{url}{body}{timestamp}"
        
        signature = hmac.new(
            self.consumer_secret.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return f"{self.consumer_id}:{timestamp}:{signature}"
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((aiohttp.ClientError, asyncio.TimeoutError))
    )
    async def _authenticate(self):
        """Authenticate with SSI API"""
        url = f"{self.trading_url}/api/v2/auth/login"
        
        auth_data = {
            "consumerID": self.consumer_id,
            "consumerSecret": self.consumer_secret
        }
        
        try:
            signature = self._create_signature("POST", "/api/v2/auth/login", json.dumps(auth_data))
            headers = {"X-API-Signature": signature}
            
            async with self.session.post(url, json=auth_data, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    self.access_token = data.get("data", {}).get("accessToken")
                    self.token_expires_at = datetime.utcnow() + timedelta(hours=24)
                    
                    logger.info("SSI authentication successful")
                elif response.status == 429:
                    raise SSIRateLimitError("Rate limit exceeded during authentication")
                else:
                    error_text = await response.text()
                    raise SSIAuthenticationError(f"Authentication failed: {response.status} - {error_text}")
                    
        except aiohttp.ClientError as e:
            logger.error("SSI authentication failed", error=str(e))
            raise SSIAuthenticationError(f"Authentication request failed: {str(e)}")
    
    async def _make_request(self, method: str, endpoint: str, params: Optional[Dict] = None, 
                          data: Optional[Dict] = None, use_data_url: bool = False) -> Dict[str, Any]:
        """Make authenticated request to SSI API"""
        
        # Rate limiting
        if not await self.rate_limiter.acquire():
            await asyncio.sleep(1.0)  # Wait before retry
            if not await self.rate_limiter.acquire():
                raise SSIRateLimitError("Rate limit exceeded")
        
        # Circuit breaker check
        if self.circuit_breaker.state == "OPEN":
            raise CircuitBreakerOpen("Circuit breaker is open")
        
        # Ensure authentication
        if not self.access_token or self._is_token_expired():
            await self._authenticate()
        
        # Prepare request
        base_url = self.data_url if use_data_url else self.trading_url
        url = f"{base_url}{endpoint}"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "X-API-Key": self.consumer_id
        }
        
        try:
            self.request_count += 1
            self.last_request_time = datetime.utcnow()
            
            async with self.session.request(method, url, params=params, json=data, headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    logger.debug("SSI API request successful", 
                               endpoint=endpoint, 
                               status=response.status)
                    return result
                elif response.status == 401:
                    # Token expired, re-authenticate and retry
                    logger.warning("Token expired, re-authenticating")
                    await self._authenticate()
                    headers["Authorization"] = f"Bearer {self.access_token}"
                    
                    async with self.session.request(method, url, params=params, json=data, headers=headers) as retry_response:
                        if retry_response.status == 200:
                            return await retry_response.json()
                        else:
                            error_text = await retry_response.text()
                            raise SSIDataClientError(f"Request failed after re-auth: {retry_response.status} - {error_text}")
                elif response.status == 429:
                    raise SSIRateLimitError("Rate limit exceeded")
                elif response.status == 404:
                    raise SSIDataUnavailableError("Requested data not found")
                else:
                    error_text = await response.text()
                    raise SSIDataClientError(f"Request failed: {response.status} - {error_text}")
                    
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            self.error_count += 1
            self.circuit_breaker.record_failure()
            logger.error("SSI API request failed", 
                        endpoint=endpoint, 
                        error=str(e))
            raise SSIDataClientError(f"Request error: {str(e)}")
    
    # Market Data Methods
    
    async def get_market_data(self, symbols: List[str], data_types: List[DataTypeEnum] = None) -> Dict[str, Any]:
        """Get real-time market data for symbols"""
        if data_types is None:
            data_types = [DataTypeEnum.QUOTE]
        
        params = {
            "symbols": ",".join(symbols),
            "types": ",".join([dt.value for dt in data_types])
        }
        
        return await self._make_request("GET", "/api/v1/market-data/quotes", params=params, use_data_url=True)
    
    async def get_quote_data(self, symbol: str) -> QuoteData:
        """Get detailed quote data for a symbol"""
        params = {"symbol": symbol.upper()}
        
        response = await self._make_request("GET", "/api/v1/market-data/quote", params=params, use_data_url=True)
        quote_data = response.get("data", {})
        
        # Map SSI response to our model
        return QuoteData(
            symbol=symbol.upper(),
            market=MarketEnum(quote_data.get("exchange", "HOSE")),
            session=self._determine_current_session(),
            last_price=Decimal(str(quote_data.get("lastPrice", 0))),
            last_volume=quote_data.get("lastVolume", 0),
            ceiling_price=Decimal(str(quote_data.get("ceilingPrice", 0))),
            floor_price=Decimal(str(quote_data.get("floorPrice", 0))),
            reference_price=Decimal(str(quote_data.get("referencePrice", 0))),
            bid_price=Decimal(str(quote_data.get("bidPrice", 0))) if quote_data.get("bidPrice") else None,
            bid_volume=quote_data.get("bidVolume"),
            ask_price=Decimal(str(quote_data.get("askPrice", 0))) if quote_data.get("askPrice") else None,
            ask_volume=quote_data.get("askVolume"),
            open_price=Decimal(str(quote_data.get("openPrice", 0))) if quote_data.get("openPrice") else None,
            high_price=Decimal(str(quote_data.get("highPrice", 0))) if quote_data.get("highPrice") else None,
            low_price=Decimal(str(quote_data.get("lowPrice", 0))) if quote_data.get("lowPrice") else None,
            total_volume=quote_data.get("totalVolume", 0),
            total_value=Decimal(str(quote_data.get("totalValue", 0))),
            foreign_buy_volume=quote_data.get("foreignBuyVolume"),
            foreign_sell_volume=quote_data.get("foreignSellVolume"),
            lot_size=quote_data.get("lotSize", 100)
        )
    
    async def get_trade_data(self, symbol: str, limit: int = 100) -> List[TradeData]:
        """Get recent trade data for a symbol"""
        params = {
            "symbol": symbol.upper(),
            "limit": min(limit, 1000)
        }
        
        response = await self._make_request("GET", "/api/v1/market-data/trades", params=params, use_data_url=True)
        trades_data = response.get("data", [])
        
        trades = []
        for trade in trades_data:
            trades.append(TradeData(
                symbol=symbol.upper(),
                market=MarketEnum(trade.get("exchange", "HOSE")),
                session=self._determine_current_session(),
                trade_id=trade.get("tradeId", ""),
                price=Decimal(str(trade.get("price", 0))),
                volume=trade.get("volume", 0),
                value=Decimal(str(trade.get("value", 0))),
                side=trade.get("side", ""),
                trade_time=datetime.fromisoformat(trade.get("tradeTime", datetime.utcnow().isoformat())),
                match_type=trade.get("matchType"),
                is_foreign=trade.get("isForeign")
            ))
        
        return trades
    
    async def get_order_book(self, symbol: str, depth: int = 10) -> OrderBookData:
        """Get order book data for a symbol"""
        params = {
            "symbol": symbol.upper(),
            "depth": min(depth, 10)
        }
        
        response = await self._make_request("GET", "/api/v1/market-data/orderbook", params=params, use_data_url=True)
        book_data = response.get("data", {})
        
        from ..models import OrderBookLevel
        
        bids = [
            OrderBookLevel(
                price=Decimal(str(level.get("price", 0))),
                volume=level.get("volume", 0),
                orders=level.get("orders")
            )
            for level in book_data.get("bids", [])
        ]
        
        asks = [
            OrderBookLevel(
                price=Decimal(str(level.get("price", 0))),
                volume=level.get("volume", 0),
                orders=level.get("orders")
            )
            for level in book_data.get("asks", [])
        ]
        
        return OrderBookData(
            symbol=symbol.upper(),
            market=MarketEnum(book_data.get("exchange", "HOSE")),
            session=self._determine_current_session(),
            bids=bids,
            asks=asks,
            total_bid_volume=sum(b.volume for b in bids),
            total_ask_volume=sum(a.volume for a in asks),
            spread=bids[0].price - asks[0].price if bids and asks else None
        )
    
    async def get_historical_data(self, request: HistoricalDataRequest) -> List[Dict[str, Any]]:
        """Get historical price data"""
        params = {
            "symbol": request.symbol,
            "fromDate": request.from_date.strftime("%Y-%m-%d"),
            "toDate": request.to_date.strftime("%Y-%m-%d"),
            "resolution": request.resolution
        }
        
        response = await self._make_request("GET", "/api/v1/market-data/historical", params=params, use_data_url=True)
        return response.get("data", [])
    
    async def get_index_data(self, index_codes: List[str] = None) -> List[IndexData]:
        """Get market index data"""
        if index_codes is None:
            index_codes = ["VN-Index", "HNX-Index", "UPCOM-Index"]
        
        params = {"indices": ",".join(index_codes)}
        
        response = await self._make_request("GET", "/api/v1/market-data/indices", params=params, use_data_url=True)
        indices_data = response.get("data", [])
        
        indices = []
        for index in indices_data:
            indices.append(IndexData(
                index_code=index.get("indexCode", ""),
                index_value=Decimal(str(index.get("indexValue", 0))),
                change=Decimal(str(index.get("change", 0))),
                change_percent=Decimal(str(index.get("changePercent", 0))),
                volume=index.get("volume", 0),
                value=Decimal(str(index.get("value", 0))),
                advances=index.get("advances"),
                declines=index.get("declines"),
                unchanged=index.get("unchanged")
            ))
        
        return indices
    
    def _determine_current_session(self) -> SessionEnum:
        """Determine current trading session based on time"""
        now = datetime.now()
        current_time = now.time()
        
        # Vietnamese market sessions (ICT timezone)
        if current_time < time(8, 0):
            return SessionEnum.PRE_OPEN
        elif time(8, 0) <= current_time < time(9, 0):
            return SessionEnum.PRE_OPEN
        elif time(9, 0) <= current_time < time(11, 30):
            return SessionEnum.CONTINUOUS
        elif time(11, 30) <= current_time < time(13, 0):
            return SessionEnum.INTERMISSION
        elif time(13, 0) <= current_time < time(15, 0):
            return SessionEnum.CONTINUOUS
        elif time(15, 0) <= current_time < time(15, 15):
            return SessionEnum.CLOSE
        elif time(15, 15) <= current_time < time(15, 30):
            return SessionEnum.POST_CLOSE
        elif time(15, 30) <= current_time < time(16, 30):
            return SessionEnum.AFTER_HOURS
        else:
            return SessionEnum.POST_CLOSE
    
    # Streaming Methods
    
    async def subscribe_real_time(self, symbols: List[str], data_types: List[DataTypeEnum] = None) -> AsyncGenerator[Dict[str, Any], None]:
        """Subscribe to real-time data stream"""
        if data_types is None:
            data_types = [DataTypeEnum.QUOTE]
        
        # This would implement WebSocket connection for real-time data
        # For now, we'll simulate with periodic polling
        logger.info("Starting real-time data stream", symbols=symbols, data_types=data_types)
        
        while True:
            try:
                for symbol in symbols:
                    if DataTypeEnum.QUOTE in data_types:
                        quote = await self.get_quote_data(symbol)
                        yield {
                            "type": "quote",
                            "symbol": symbol,
                            "data": quote.dict(),
                            "timestamp": datetime.utcnow().isoformat()
                        }
                
                await asyncio.sleep(settings.data_refresh_interval)
                
            except Exception as e:
                logger.error("Error in real-time stream", error=str(e))
                await asyncio.sleep(5)  # Wait before retry
    
    # Utility Methods
    
    def get_stats(self) -> Dict[str, Any]:
        """Get client statistics"""
        return {
            "request_count": self.request_count,
            "error_count": self.error_count,
            "error_rate": self.error_count / max(self.request_count, 1),
            "last_request_time": self.last_request_time.isoformat() if self.last_request_time else None,
            "circuit_breaker_state": self.circuit_breaker.state,
            "is_authenticated": bool(self.access_token and not self._is_token_expired())
        }
