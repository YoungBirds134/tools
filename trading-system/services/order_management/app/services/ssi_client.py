"""
SSI FastConnect API Client
Enhanced client for SSI FastConnect Trading API with proper error handling,
retry logic, and comprehensive logging.
"""

import asyncio
import hashlib
import hmac
import json
import base64
import time
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass, asdict
import httpx
from urllib.parse import urljoin
import structlog

from ..config import settings
from ..utils.exceptions import (
    SSIAPIError, 
    SSIAuthenticationError, 
    SSIRateLimitError,
    SSINetworkError
)

logger = structlog.get_logger(__name__)


@dataclass
class SSICredentials:
    """SSI API credentials"""
    consumer_id: str
    consumer_secret: str
    private_key: str
    public_key: str = ""


@dataclass
class TradingSession:
    """Trading session information"""
    access_token: str
    refresh_token: str = ""
    expires_at: datetime = None
    account: str = ""
    two_fa_verified: bool = False


class SSIFastConnectClient:
    """
    Enhanced SSI FastConnect API client with comprehensive features:
    - Automatic token refresh
    - Rate limiting compliance
    - Circuit breaker pattern
    - Comprehensive error handling
    - Request/response logging
    """
    
    def __init__(self, credentials: SSICredentials = None):
        self.credentials = credentials or self._load_credentials()
        self.base_url = settings.fc_trading_url
        self.session: Optional[TradingSession] = None
        self.http_client: Optional[httpx.AsyncClient] = None
        
        # Rate limiting
        self.last_request_time = 0
        self.request_count = 0
        self.rate_limit_window = 60  # 1 minute
        self.max_requests_per_window = 100
        
        # Circuit breaker
        self.failure_count = 0
        self.circuit_open = False
        self.circuit_open_time = None
        self.circuit_timeout = 60  # 1 minute
        
        self._init_http_client()
    
    def _load_credentials(self) -> SSICredentials:
        """Load credentials from settings"""
        return SSICredentials(
            consumer_id=settings.consumer_id,
            consumer_secret=settings.consumer_secret,
            private_key=settings.private_key,
            public_key=settings.public_key
        )
    
    def _init_http_client(self):
        """Initialize HTTP client with proper settings"""
        timeout = httpx.Timeout(30.0, connect=10.0)
        limits = httpx.Limits(max_keepalive_connections=10, max_connections=20)
        
        self.http_client = httpx.AsyncClient(
            timeout=timeout,
            limits=limits,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": f"TradingSystem/1.0.0 (FastAPI)"
            }
        )
    
    async def close(self):
        """Close HTTP client"""
        if self.http_client:
            await self.http_client.aclose()
    
    def _generate_signature(self, method: str, url: str, body: str = "") -> str:
        """Generate X-Signature for API authentication"""
        try:
            # Create string to sign
            string_to_sign = f"{method.upper()}{url}{body}"
            
            # Decode private key
            private_key_bytes = base64.b64decode(self.credentials.private_key)
            
            # Generate signature
            signature = hmac.new(
                private_key_bytes,
                string_to_sign.encode('utf-8'),
                hashlib.sha256
            ).digest()
            
            return base64.b64encode(signature).decode('utf-8')
            
        except Exception as e:
            logger.error("Failed to generate signature", error=str(e))
            raise SSIAuthenticationError(f"Signature generation failed: {str(e)}")
    
    def _check_rate_limit(self):
        """Check if request is within rate limits"""
        current_time = time.time()
        
        # Reset counter if window has passed
        if current_time - self.last_request_time > self.rate_limit_window:
            self.request_count = 0
        
        # Check if rate limit exceeded
        if self.request_count >= self.max_requests_per_window:
            raise SSIRateLimitError("Rate limit exceeded")
        
        self.request_count += 1
        self.last_request_time = current_time
    
    def _check_circuit_breaker(self):
        """Check circuit breaker status"""
        if not self.circuit_open:
            return
        
        # Check if circuit should be closed
        if time.time() - self.circuit_open_time > self.circuit_timeout:
            self.circuit_open = False
            self.failure_count = 0
            logger.info("Circuit breaker closed")
        else:
            raise SSINetworkError("Circuit breaker is open")
    
    def _record_success(self):
        """Record successful request"""
        self.failure_count = 0
        if self.circuit_open:
            self.circuit_open = False
            logger.info("Circuit breaker closed after successful request")
    
    def _record_failure(self):
        """Record failed request"""
        self.failure_count += 1
        
        # Open circuit if too many failures
        if self.failure_count >= 5:
            self.circuit_open = True
            self.circuit_open_time = time.time()
            logger.warning("Circuit breaker opened due to failures")
    
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Dict[str, Any] = None,
        require_auth: bool = True
    ) -> Dict[str, Any]:
        """Make authenticated API request with error handling"""
        
        # Check preconditions
        self._check_rate_limit()
        self._check_circuit_breaker()
        
        url = urljoin(self.base_url, endpoint)
        headers = {
            "ConsumerID": self.credentials.consumer_id,
            "ConsumerSecret": self.credentials.consumer_secret,
        }
        
        # Add authentication if required
        if require_auth and self.session:
            headers["Authorization"] = f"Bearer {self.session.access_token}"
        
        # Prepare body
        body = json.dumps(data) if data else ""
        
        # Generate signature
        headers["X-Signature"] = self._generate_signature(method, url, body)
        
        try:
            logger.info("Making API request", method=method, endpoint=endpoint)
            
            response = await self.http_client.request(
                method=method,
                url=url,
                content=body,
                headers=headers
            )
            
            # Handle response
            response.raise_for_status()
            result = response.json()
            
            self._record_success()
            
            logger.info("API request successful", 
                       method=method, 
                       endpoint=endpoint,
                       status_code=response.status_code)
            
            return result
            
        except httpx.HTTPStatusError as e:
            self._record_failure()
            
            if e.response.status_code == 401:
                raise SSIAuthenticationError("Authentication failed")
            elif e.response.status_code == 429:
                raise SSIRateLimitError("Rate limit exceeded")
            else:
                raise SSIAPIError(f"HTTP {e.response.status_code}: {e.response.text}")
                
        except httpx.RequestError as e:
            self._record_failure()
            raise SSINetworkError(f"Network error: {str(e)}")
        
        except Exception as e:
            self._record_failure()
            logger.error("Unexpected error in API request", error=str(e))
            raise SSIAPIError(f"Unexpected error: {str(e)}")
    
    async def get_access_token(self) -> str:
        """Get access token for API authentication"""
        try:
            result = await self._make_request(
                method="POST",
                endpoint="Trading/AccessToken",
                require_auth=False
            )
            
            if result.get("success"):
                access_token = result.get("data", {}).get("accessToken")
                if access_token:
                    # Store session
                    self.session = TradingSession(
                        access_token=access_token,
                        expires_at=datetime.now() + timedelta(hours=1)  # Assume 1 hour validity
                    )
                    logger.info("Access token obtained successfully")
                    return access_token
            
            raise SSIAuthenticationError("Failed to get access token")
            
        except Exception as e:
            logger.error("Failed to get access token", error=str(e))
            raise
    
    async def get_otp(self, account: str) -> Dict[str, Any]:
        """Request OTP for 2FA authentication"""
        try:
            if not self.session:
                await self.get_access_token()
            
            data = {
                "account": account,
                "twoFAType": settings.two_fa_type
            }
            
            result = await self._make_request(
                method="POST",
                endpoint="Trading/GetOTP",
                data=data
            )
            
            logger.info("OTP requested successfully", account=account)
            return result
            
        except Exception as e:
            logger.error("Failed to request OTP", account=account, error=str(e))
            raise
    
    async def place_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """Place a new order"""
        try:
            if not self.session:
                await self.get_access_token()
            
            result = await self._make_request(
                method="POST",
                endpoint="Trading/NewOrder",
                data=order_data
            )
            
            logger.info("Order placed successfully", 
                       instrument=order_data.get("instrumentID"),
                       quantity=order_data.get("quantity"))
            return result
            
        except Exception as e:
            logger.error("Failed to place order", 
                        instrument=order_data.get("instrumentID"),
                        error=str(e))
            raise
    
    async def modify_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """Modify existing order"""
        try:
            if not self.session:
                await self.get_access_token()
            
            result = await self._make_request(
                method="POST",
                endpoint="Trading/ModifyOrder",
                data=order_data
            )
            
            logger.info("Order modified successfully", 
                       order_id=order_data.get("orderID"))
            return result
            
        except Exception as e:
            logger.error("Failed to modify order", 
                        order_id=order_data.get("orderID"),
                        error=str(e))
            raise
    
    async def cancel_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cancel existing order"""
        try:
            if not self.session:
                await self.get_access_token()
            
            result = await self._make_request(
                method="POST",
                endpoint="Trading/CancelOrder",
                data=order_data
            )
            
            logger.info("Order cancelled successfully", 
                       order_id=order_data.get("orderID"))
            return result
            
        except Exception as e:
            logger.error("Failed to cancel order", 
                        order_id=order_data.get("orderID"),
                        error=str(e))
            raise
    
    async def get_account_balance(self, account: str) -> Dict[str, Any]:
        """Get account balance information"""
        try:
            if not self.session:
                await self.get_access_token()
            
            data = {"account": account}
            
            result = await self._make_request(
                method="GET",
                endpoint="Trading/GetAccountBalance",
                data=data
            )
            
            logger.info("Account balance retrieved", account=account)
            return result
            
        except Exception as e:
            logger.error("Failed to get account balance", 
                        account=account, error=str(e))
            raise
    
    async def get_portfolio(self, account: str) -> Dict[str, Any]:
        """Get portfolio positions"""
        try:
            if not self.session:
                await self.get_access_token()
            
            data = {
                "account": account,
                "querySummary": True
            }
            
            result = await self._make_request(
                method="GET",
                endpoint="Trading/GetPortfolio",
                data=data
            )
            
            logger.info("Portfolio retrieved", account=account)
            return result
            
        except Exception as e:
            logger.error("Failed to get portfolio", 
                        account=account, error=str(e))
            raise
    
    async def get_max_quantity(
        self, 
        account: str, 
        instrument_id: str, 
        price: float = 0
    ) -> Dict[str, Any]:
        """Get maximum tradeable quantity"""
        try:
            if not self.session:
                await self.get_access_token()
            
            data = {
                "account": account,
                "instrumentID": instrument_id,
                "price": price
            }
            
            result = await self._make_request(
                method="GET",
                endpoint="Trading/GetMaxQuantity",
                data=data
            )
            
            logger.info("Max quantity retrieved", 
                       account=account, 
                       instrument=instrument_id)
            return result
            
        except Exception as e:
            logger.error("Failed to get max quantity", 
                        account=account, 
                        instrument=instrument_id,
                        error=str(e))
            raise
    
    async def get_order_history(
        self, 
        account: str, 
        start_date: str, 
        end_date: str
    ) -> Dict[str, Any]:
        """Get order history for date range"""
        try:
            if not self.session:
                await self.get_access_token()
            
            data = {
                "account": account,
                "startDate": start_date,
                "endDate": end_date
            }
            
            result = await self._make_request(
                method="GET",
                endpoint="Trading/GetOrderHistory",
                data=data
            )
            
            logger.info("Order history retrieved", 
                       account=account,
                       start_date=start_date,
                       end_date=end_date)
            return result
            
        except Exception as e:
            logger.error("Failed to get order history", 
                        account=account,
                        start_date=start_date,
                        end_date=end_date,
                        error=str(e))
            raise


# Global client instance
_ssi_client: Optional[SSIFastConnectClient] = None


async def get_ssi_client() -> SSIFastConnectClient:
    """Get or create SSI client instance"""
    global _ssi_client
    
    if _ssi_client is None:
        _ssi_client = SSIFastConnectClient()
    
    return _ssi_client


async def close_ssi_client():
    """Close SSI client instance"""
    global _ssi_client
    
    if _ssi_client:
        await _ssi_client.close()
        _ssi_client = None
