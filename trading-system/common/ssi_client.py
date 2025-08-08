"""
SSI FastConnect API client for data and trading operations.
"""

import asyncio
import hashlib
import hmac
import json
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import httpx
import websockets
from jose import jwt

from .config import get_settings
from .logging import get_logger
from .utils import HTTPClient, RateLimiter

logger = get_logger(__name__)


class SSIFastConnectClient:
    """SSI FastConnect API client for trading operations."""
    
    def __init__(self, settings: Optional[Any] = None):
        """Initialize SSI FastConnect client."""
        self.settings = settings or get_settings().ssi
        self.http_client = HTTPClient(timeout=self.settings.timeout)
        self.rate_limiter = RateLimiter(max_requests=100, time_window=60)
        self._access_token: Optional[str] = None
        self._token_expires_at: Optional[datetime] = None
    
    def _create_signature(self, data: str) -> str:
        """Create X-Signature for SSI API authentication."""
        return hmac.new(
            self.settings.private_key.encode('utf-8'),
            data.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    def _get_headers(self, include_auth: bool = True) -> Dict[str, str]:
        """Get common headers for API requests."""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Consumer-ID": self.settings.consumer_id,
        }
        
        if include_auth and self._access_token:
            headers["Authorization"] = f"Bearer {self._access_token}"
        
        return headers
    
    async def _check_rate_limit(self, endpoint: str) -> bool:
        """Check rate limit for endpoint."""
        if not self.rate_limiter.is_allowed(endpoint):
            remaining = self.rate_limiter.get_remaining_requests(endpoint)
            reset_time = self.rate_limiter.get_reset_time(endpoint)
            
            logger.warning(
                f"Rate limit exceeded for {endpoint}",
                remaining=remaining,
                reset_time=reset_time
            )
            return False
        
        return True
    
    async def authenticate(self) -> str:
        """Authenticate and get access token."""
        if self._access_token and self._token_expires_at:
            if datetime.utcnow() < self._token_expires_at:
                return self._access_token
        
        endpoint = "/api/v2/Trading/AccessToken"
        url = f"{self.settings.trading_base_url}{endpoint}"
        
        if not await self._check_rate_limit(endpoint):
            raise Exception("Rate limit exceeded for authentication")
        
        data = {
            "consumerID": self.settings.consumer_id,
            "consumerSecret": self.settings.consumer_secret
        }
        
        data_str = json.dumps(data, separators=(',', ':'))
        signature = self._create_signature(data_str)
        
        headers = self._get_headers(include_auth=False)
        headers["X-Signature"] = signature
        
        try:
            response = await self.http_client.post(
                url, 
                headers=headers, 
                json_data=data
            )
            
            result = response.json()
            
            if result.get("status") == 200:
                self._access_token = result["data"]["accessToken"]
                # Token expires in 24 hours, refresh 1 hour early
                self._token_expires_at = datetime.utcnow().replace(hour=23, minute=0)
                
                logger.info("SSI FastConnect authentication successful")
                return self._access_token
            else:
                raise Exception(f"Authentication failed: {result}")
        
        except Exception as e:
            logger.error(f"SSI authentication error: {e}")
            raise
    
    async def get_otp(self, pin: str) -> Dict[str, Any]:
        """Get OTP for 2FA authentication."""
        await self.authenticate()
        
        endpoint = "/api/v2/Trading/GetOTP"
        url = f"{self.settings.trading_base_url}{endpoint}"
        
        if not await self._check_rate_limit(endpoint):
            raise Exception("Rate limit exceeded for OTP request")
        
        data = {"pin": pin}
        
        try:
            response = await self.http_client.post(
                url,
                headers=self._get_headers(),
                json_data=data
            )
            
            result = response.json()
            logger.info("OTP request completed", status=result.get("status"))
            return result
        
        except Exception as e:
            logger.error(f"OTP request error: {e}")
            raise
    
    async def place_order(
        self,
        instrument_id: str,
        market: str,
        buy_sell: str,
        order_type: str,
        price: float,
        quantity: int,
        account: str,
        request_id: Optional[str] = None,
        otp: Optional[str] = None
    ) -> Dict[str, Any]:
        """Place a new order."""
        await self.authenticate()
        
        endpoint = "/api/v2/Trading/NewOrder"
        url = f"{self.settings.trading_base_url}{endpoint}"
        
        if not await self._check_rate_limit(endpoint):
            raise Exception("Rate limit exceeded for order placement")
        
        data = {
            "instrumentID": instrument_id,
            "market": market,
            "buySell": buy_sell,
            "orderType": order_type,
            "price": price,
            "quantity": quantity,
            "account": account
        }
        
        if request_id:
            data["requestID"] = request_id
        
        if otp:
            data["otp"] = otp
        
        try:
            response = await self.http_client.post(
                url,
                headers=self._get_headers(),
                json_data=data
            )
            
            result = response.json()
            logger.info(
                "Order placement completed",
                instrument=instrument_id,
                order_type=order_type,
                quantity=quantity,
                status=result.get("status")
            )
            return result
        
        except Exception as e:
            logger.error(f"Order placement error: {e}")
            raise
    
    async def modify_order(
        self,
        order_id: str,
        price: Optional[float] = None,
        quantity: Optional[int] = None,
        otp: Optional[str] = None
    ) -> Dict[str, Any]:
        """Modify an existing order."""
        await self.authenticate()
        
        endpoint = "/api/v2/Trading/ModifyOrder"
        url = f"{self.settings.trading_base_url}{endpoint}"
        
        if not await self._check_rate_limit(endpoint):
            raise Exception("Rate limit exceeded for order modification")
        
        data = {"orderID": order_id}
        
        if price is not None:
            data["price"] = price
        
        if quantity is not None:
            data["quantity"] = quantity
        
        if otp:
            data["otp"] = otp
        
        try:
            response = await self.http_client.post(
                url,
                headers=self._get_headers(),
                json_data=data
            )
            
            result = response.json()
            logger.info(
                "Order modification completed",
                order_id=order_id,
                status=result.get("status")
            )
            return result
        
        except Exception as e:
            logger.error(f"Order modification error: {e}")
            raise
    
    async def cancel_order(
        self,
        order_id: str,
        otp: Optional[str] = None
    ) -> Dict[str, Any]:
        """Cancel an existing order."""
        await self.authenticate()
        
        endpoint = "/api/v2/Trading/CancelOrder"
        url = f"{self.settings.trading_base_url}{endpoint}"
        
        if not await self._check_rate_limit(endpoint):
            raise Exception("Rate limit exceeded for order cancellation")
        
        data = {"orderID": order_id}
        
        if otp:
            data["otp"] = otp
        
        try:
            response = await self.http_client.post(
                url,
                headers=self._get_headers(),
                json_data=data
            )
            
            result = response.json()
            logger.info(
                "Order cancellation completed",
                order_id=order_id,
                status=result.get("status")
            )
            return result
        
        except Exception as e:
            logger.error(f"Order cancellation error: {e}")
            raise
    
    async def get_account_balance(self, account: str) -> Dict[str, Any]:
        """Get account balance information."""
        await self.authenticate()
        
        endpoint = f"/api/v2/Trading/AccountBalance/{account}"
        url = f"{self.settings.trading_base_url}{endpoint}"
        
        if not await self._check_rate_limit(endpoint):
            raise Exception("Rate limit exceeded for balance query")
        
        try:
            response = await self.http_client.get(
                url,
                headers=self._get_headers()
            )
            
            result = response.json()
            logger.debug("Account balance retrieved", account=account)
            return result
        
        except Exception as e:
            logger.error(f"Balance query error: {e}")
            raise
    
    async def get_positions(self, account: str) -> Dict[str, Any]:
        """Get account positions."""
        await self.authenticate()
        
        endpoint = f"/api/v2/Trading/Positions/{account}"
        url = f"{self.settings.trading_base_url}{endpoint}"
        
        if not await self._check_rate_limit(endpoint):
            raise Exception("Rate limit exceeded for positions query")
        
        try:
            response = await self.http_client.get(
                url,
                headers=self._get_headers()
            )
            
            result = response.json()
            logger.debug("Positions retrieved", account=account)
            return result
        
        except Exception as e:
            logger.error(f"Positions query error: {e}")
            raise
    
    async def get_order_history(
        self,
        account: str,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get order history."""
        await self.authenticate()
        
        endpoint = f"/api/v2/Trading/OrderHistory/{account}"
        url = f"{self.settings.trading_base_url}{endpoint}"
        
        params = {}
        if from_date:
            params["fromDate"] = from_date
        if to_date:
            params["toDate"] = to_date
        
        if not await self._check_rate_limit(endpoint):
            raise Exception("Rate limit exceeded for order history query")
        
        try:
            response = await self.http_client.get(
                url,
                headers=self._get_headers(),
                params=params
            )
            
            result = response.json()
            logger.debug("Order history retrieved", account=account)
            return result
        
        except Exception as e:
            logger.error(f"Order history query error: {e}")
            raise
    
    async def close(self):
        """Close HTTP client."""
        await self.http_client.close()


class SSIDataClient:
    """SSI FastConnect Data API client."""
    
    def __init__(self, settings: Optional[Any] = None):
        """Initialize SSI Data client."""
        self.settings = settings or get_settings().ssi
        self.http_client = HTTPClient(timeout=self.settings.timeout)
        self.rate_limiter = RateLimiter(max_requests=200, time_window=60)
        self._ws_connection: Optional[websockets.WebSocketServerProtocol] = None
        self._connection_key: Optional[str] = None
    
    async def get_daily_ohlc(
        self,
        symbol: str,
        from_date: str,
        to_date: str,
        resolution: str = "1D"
    ) -> Dict[str, Any]:
        """Get daily OHLC data."""
        endpoint = "/api/v1/DailyOhlc"
        url = f"{self.settings.base_url}{endpoint}"
        
        params = {
            "symbol": symbol,
            "fromDate": from_date,
            "toDate": to_date,
            "resolution": resolution
        }
        
        if not self.rate_limiter.is_allowed(endpoint):
            raise Exception("Rate limit exceeded for OHLC data")
        
        try:
            response = await self.http_client.get(url, params=params)
            result = response.json()
            logger.debug("Daily OHLC data retrieved", symbol=symbol)
            return result
        
        except Exception as e:
            logger.error(f"OHLC data error: {e}")
            raise
    
    async def get_intraday_ohlc(
        self,
        symbol: str,
        from_date: str,
        to_date: str,
        resolution: str = "1"
    ) -> Dict[str, Any]:
        """Get intraday OHLC data."""
        endpoint = "/api/v1/IntradayOhlc"
        url = f"{self.settings.base_url}{endpoint}"
        
        params = {
            "symbol": symbol,
            "fromDate": from_date,
            "toDate": to_date,
            "resolution": resolution
        }
        
        if not self.rate_limiter.is_allowed(endpoint):
            raise Exception("Rate limit exceeded for intraday OHLC data")
        
        try:
            response = await self.http_client.get(url, params=params)
            result = response.json()
            logger.debug("Intraday OHLC data retrieved", symbol=symbol)
            return result
        
        except Exception as e:
            logger.error(f"Intraday OHLC data error: {e}")
            raise
    
    async def get_stock_price(
        self,
        symbol: str,
        from_date: str,
        to_date: str,
        market: str = "HOSE"
    ) -> Dict[str, Any]:
        """Get stock price data."""
        endpoint = "/api/v1/DailyStockPrice"
        url = f"{self.settings.base_url}{endpoint}"
        
        params = {
            "symbol": symbol,
            "fromDate": from_date,
            "toDate": to_date,
            "market": market
        }
        
        if not self.rate_limiter.is_allowed(endpoint):
            raise Exception("Rate limit exceeded for stock price data")
        
        try:
            response = await self.http_client.get(url, params=params)
            result = response.json()
            logger.debug("Stock price data retrieved", symbol=symbol)
            return result
        
        except Exception as e:
            logger.error(f"Stock price data error: {e}")
            raise
    
    async def connect_websocket(self, channels: List[str]) -> None:
        """Connect to SSI WebSocket for real-time data."""
        ws_url = "wss://fc-data.ssi.com.vn/realtime"
        
        try:
            self._ws_connection = await websockets.connect(ws_url)
            
            # Subscribe to channels
            subscribe_message = {
                "action": "subscribe",
                "channels": channels
            }
            
            await self._ws_connection.send(json.dumps(subscribe_message))
            logger.info("WebSocket connected and subscribed", channels=channels)
            
        except Exception as e:
            logger.error(f"WebSocket connection error: {e}")
            raise
    
    async def listen_websocket(self, message_handler: callable) -> None:
        """Listen for WebSocket messages."""
        if not self._ws_connection:
            raise Exception("WebSocket not connected")
        
        try:
            async for message in self._ws_connection:
                try:
                    data = json.loads(message)
                    await message_handler(data)
                except Exception as e:
                    logger.error(f"Message processing error: {e}")
        
        except Exception as e:
            logger.error(f"WebSocket listening error: {e}")
            raise
    
    async def disconnect_websocket(self) -> None:
        """Disconnect WebSocket."""
        if self._ws_connection:
            await self._ws_connection.close()
            self._ws_connection = None
            logger.info("WebSocket disconnected")
    
    async def close(self):
        """Close data client."""
        await self.disconnect_websocket()
        await self.http_client.close()


# Global client instances
ssi_trading_client = SSIFastConnectClient()
ssi_data_client = SSIDataClient()

# Convenience functions
def get_trading_client() -> SSIFastConnectClient:
    """Get SSI trading client instance."""
    return ssi_trading_client

def get_data_client() -> SSIDataClient:
    """Get SSI data client instance."""
    return ssi_data_client
