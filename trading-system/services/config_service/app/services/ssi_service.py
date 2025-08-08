"""
SSI FastConnect Service for managing API tokens and authentication
"""

import asyncio
import aiohttp
import base64
import hashlib
import hmac
import json
import logging
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from urllib.parse import urlencode

from ..config import Settings

logger = logging.getLogger(__name__)


class SSIService:
    """SSI FastConnect API service for token management"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.session: Optional[aiohttp.ClientSession] = None
        self.access_token: Optional[str] = None
        self.trading_access_token: Optional[str] = None
        self.token_expires_at: Optional[datetime] = None
        self.trading_token_expires_at: Optional[datetime] = None
        self.token_expires_in: Optional[int] = None
        self.trading_token_expires_in: Optional[int] = None
        self.is_initialized = False
        self._lock = asyncio.Lock()
        
        # SSI configuration
        self.consumer_id = settings.consumer_id
        self.consumer_secret = settings.consumer_secret
        self.private_key = settings.safe_private_key
        self.fc_trading_url = settings.fc_trading_url.rstrip('/')
        self.fc_data_url = settings.fc_data_url.rstrip('/')
        self.two_fa_type = settings.two_fa_type
        self.notify_id = settings.notify_id
        
        # Circuit breaker state
        self.failure_count = 0
        self.last_failure_time = None
        self.circuit_open = False
        
    async def initialize(self):
        """Initialize the SSI service"""
        if not self.settings.enable_ssi_service:
            logger.info("SSI service is disabled")
            return
            
        if not self.consumer_id or not self.consumer_secret:
            logger.warning("SSI credentials not configured")
            return
            
        if not self.private_key:
            logger.warning("SSI private key not configured")
            return
            
        try:
            # Create HTTP session
            timeout = aiohttp.ClientTimeout(total=self.settings.http_timeout)
            connector = aiohttp.TCPConnector(
                limit=self.settings.http_max_connections,
                limit_per_host=self.settings.http_max_connections
            )
            
            self.session = aiohttp.ClientSession(
                timeout=timeout,
                connector=connector,
                headers={
                    'User-Agent': 'TradingSystem/1.0',
                    'Content-Type': 'application/json'
                }
            )
            
            # Initialize tokens
            await self._refresh_tokens()
            
            self.is_initialized = True
            logger.info("SSI service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize SSI service: {str(e)}")
            raise
    
    async def cleanup(self):
        """Cleanup resources"""
        if self.session:
            await self.session.close()
            self.session = None
        
        self.is_initialized = False
        logger.info("SSI service cleaned up")
    
    def is_healthy(self) -> bool:
        """Check if the service is healthy"""
        if not self.is_initialized:
            return False
            
        if self.circuit_open:
            return False
            
        # Check if tokens are valid
        if not self.access_token or not self.trading_access_token:
            return False
            
        # Check if tokens are expired
        now = datetime.now()
        if (self.token_expires_at and now >= self.token_expires_at) or \
           (self.trading_token_expires_at and now >= self.trading_token_expires_at):
            return False
            
        return True
    
    async def get_access_token(self) -> str:
        """Get SSI FastConnect Data API access token"""
        async with self._lock:
            if not self.is_initialized:
                raise RuntimeError("SSI service not initialized")
            
            # Check if token is expired or about to expire
            if self._should_refresh_token(self.token_expires_at):
                await self._refresh_data_token()
            
            if not self.access_token:
                raise RuntimeError("Failed to obtain access token")
            
            return self.access_token
    
    async def get_trading_access_token(self) -> str:
        """Get SSI FastConnect Trading API access token"""
        async with self._lock:
            if not self.is_initialized:
                raise RuntimeError("SSI service not initialized")
            
            # Check if token is expired or about to expire
            if self._should_refresh_token(self.trading_token_expires_at):
                await self._refresh_trading_token()
            
            if not self.trading_access_token:
                raise RuntimeError("Failed to obtain trading access token")
            
            return self.trading_access_token
    
    async def get_otp(self) -> Dict[str, Any]:
        """Get OTP for 2FA authentication"""
        if not self.is_initialized:
            raise RuntimeError("SSI service not initialized")
        
        url = f"{self.fc_trading_url}/api/v2/Trading/GetOTP"
        
        payload = {
            "consumerID": self.consumer_id,
            "consumerSecret": self.consumer_secret
        }
        
        try:
            async with self.session.post(url, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info("OTP request successful")
                    return data
                else:
                    error_text = await response.text()
                    logger.error(f"OTP request failed: {response.status} - {error_text}")
                    raise RuntimeError(f"OTP request failed: {response.status}")
                    
        except Exception as e:
            logger.error(f"OTP request error: {str(e)}")
            self._record_failure()
            raise
    
    def _should_refresh_token(self, expires_at: Optional[datetime]) -> bool:
        """Check if token should be refreshed"""
        if not expires_at:
            return True
        
        now = datetime.now()
        threshold = timedelta(seconds=self.settings.token_refresh_threshold)
        return now >= (expires_at - threshold)
    
    async def _refresh_tokens(self):
        """Refresh both data and trading tokens"""
        await asyncio.gather(
            self._refresh_data_token(),
            self._refresh_trading_token(),
            return_exceptions=True
        )
    
    async def _refresh_data_token(self):
        """Refresh SSI FastConnect Data API token"""
        url = f"{self.fc_data_url}/api/v2/Market/AccessToken"
        
        payload = {
            "consumerID": self.consumer_id,
            "consumerSecret": self.consumer_secret
        }
        
        try:
            async with self.session.post(url, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if data.get("status") == 200 and data.get("data", {}).get("accessToken"):
                        self.access_token = data["data"]["accessToken"]
                        self.token_expires_in = 3600  # 1 hour default
                        self.token_expires_at = datetime.now() + timedelta(seconds=self.token_expires_in)
                        
                        logger.info("Data API token refreshed successfully")
                        self._reset_failure_count()
                    else:
                        logger.error(f"Invalid token response: {data}")
                        raise RuntimeError("Invalid token response")
                else:
                    error_text = await response.text()
                    logger.error(f"Token refresh failed: {response.status} - {error_text}")
                    raise RuntimeError(f"Token refresh failed: {response.status}")
                    
        except Exception as e:
            logger.error(f"Data token refresh error: {str(e)}")
            self._record_failure()
            raise
    
    async def _refresh_trading_token(self):
        """Refresh SSI FastConnect Trading API token"""
        url = f"{self.fc_trading_url}/api/v2/Trading/AccessToken"
        
        payload = {
            "consumerID": self.consumer_id,
            "consumerSecret": self.consumer_secret,
            "twoFactorType": self.two_fa_type,
            "code": "",  # Empty for initial token
            "isSave": False
        }
        
        try:
            async with self.session.post(url, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if data.get("status") == 200 and data.get("data", {}).get("accessToken"):
                        self.trading_access_token = data["data"]["accessToken"]
                        self.trading_token_expires_in = 3600  # 1 hour default
                        self.trading_token_expires_at = datetime.now() + timedelta(seconds=self.trading_token_expires_in)
                        
                        logger.info("Trading API token refreshed successfully")
                        self._reset_failure_count()
                    else:
                        logger.error(f"Invalid trading token response: {data}")
                        raise RuntimeError("Invalid trading token response")
                else:
                    error_text = await response.text()
                    logger.error(f"Trading token refresh failed: {response.status} - {error_text}")
                    raise RuntimeError(f"Trading token refresh failed: {response.status}")
                    
        except Exception as e:
            logger.error(f"Trading token refresh error: {str(e)}")
            self._record_failure()
            raise
    
    def _generate_signature(self, data: str) -> str:
        """Generate SSI signature for API requests"""
        if not self.private_key:
            raise ValueError("Private key not configured")
        
        try:
            # Decode private key
            private_key_bytes = base64.b64decode(self.private_key)
            
            # Create HMAC signature
            signature = hmac.new(
                private_key_bytes,
                data.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            return signature
        except Exception as e:
            logger.error(f"Signature generation failed: {str(e)}")
            raise
    
    def _record_failure(self):
        """Record a failure for circuit breaker"""
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        
        if self.failure_count >= self.settings.circuit_breaker_failure_threshold:
            self.circuit_open = True
            logger.warning("Circuit breaker opened due to repeated failures")
    
    def _reset_failure_count(self):
        """Reset failure count for circuit breaker"""
        self.failure_count = 0
        self.circuit_open = False
    
    async def _check_circuit_breaker(self):
        """Check circuit breaker state"""
        if self.circuit_open:
            # Check if timeout has passed
            if self.last_failure_time:
                timeout_duration = timedelta(seconds=self.settings.circuit_breaker_timeout)
                if datetime.now() - self.last_failure_time > timeout_duration:
                    self._reset_failure_count()
                    logger.info("Circuit breaker reset after timeout")
                else:
                    raise RuntimeError("Circuit breaker is open")
    
    async def make_authenticated_request(
        self, 
        method: str, 
        url: str, 
        data: Optional[Dict[str, Any]] = None,
        use_trading_token: bool = False
    ) -> Dict[str, Any]:
        """Make an authenticated request to SSI API"""
        await self._check_circuit_breaker()
        
        # Get appropriate token
        if use_trading_token:
            token = await self.get_trading_access_token()
        else:
            token = await self.get_access_token()
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        # Add signature if needed
        if data and self.private_key:
            data_str = json.dumps(data, separators=(',', ':'))
            signature = self._generate_signature(data_str)
            headers['X-Signature'] = signature
        
        try:
            async with self.session.request(method, url, json=data, headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    self._reset_failure_count()
                    return result
                else:
                    error_text = await response.text()
                    logger.error(f"API request failed: {response.status} - {error_text}")
                    self._record_failure()
                    raise RuntimeError(f"API request failed: {response.status}")
                    
        except Exception as e:
            logger.error(f"API request error: {str(e)}")
            self._record_failure()
            raise 