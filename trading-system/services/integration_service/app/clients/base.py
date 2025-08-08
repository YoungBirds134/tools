"""
Base HTTP client for SSI APIs
"""
import asyncio
import json
from typing import Any, Dict, Optional, Union
from urllib.parse import urljoin
import httpx
from app.core.logging_config import LoggerMixin
from app.core.exceptions import (
    SSIAPIError, SSINetworkError, SSIAuthenticationError,
    SSIRateLimitError, SSIServerError
)
from config import settings


class BaseHTTPClient(LoggerMixin):
    """Base HTTP client with common functionality"""
    
    def __init__(
        self,
        base_url: str,
        timeout: int = None,
        retries: int = None,
        headers: Optional[Dict[str, str]] = None
    ):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout or settings.request_timeout
        self.retries = retries or settings.max_retries
        self.default_headers = headers or {}
        self._client: Optional[httpx.AsyncClient] = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.disconnect()
    
    async def connect(self) -> None:
        """Initialize HTTP client"""
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=httpx.Timeout(self.timeout),
                headers=self.default_headers,
                limits=httpx.Limits(
                    max_keepalive_connections=20,
                    max_connections=100
                ),
                follow_redirects=True
            )
            self.log_info("HTTP client connected", base_url=self.base_url)
    
    async def disconnect(self) -> None:
        """Close HTTP client"""
        if self._client:
            await self._client.aclose()
            self._client = None
            self.log_info("HTTP client disconnected")
    
    @property
    def client(self) -> httpx.AsyncClient:
        """Get HTTP client instance"""
        if not self._client:
            raise SSINetworkError("HTTP client not connected")
        return self._client
    
    def _build_url(self, endpoint: str) -> str:
        """Build full URL from endpoint"""
        return urljoin(f"{self.base_url}/", endpoint.lstrip('/'))
    
    def _handle_response_errors(self, response: httpx.Response) -> None:
        """Handle HTTP response errors"""
        if response.status_code == 401:
            raise SSIAuthenticationError("Authentication failed")
        elif response.status_code == 403:
            raise SSIAuthenticationError("Access forbidden")
        elif response.status_code == 429:
            raise SSIRateLimitError("Rate limit exceeded")
        elif response.status_code >= 500:
            raise SSIServerError(f"Server error: {response.status_code}")
        elif response.status_code >= 400:
            try:
                error_data = response.json()
                message = error_data.get('message', f"HTTP {response.status_code}")
                raise SSIAPIError(message, response.status_code, details=error_data)
            except Exception:
                raise SSIAPIError(
                    f"HTTP {response.status_code}: {response.text[:200]}", 
                    response.status_code
                )
    
    async def _make_request_with_retry(
        self,
        method: str,
        url: str,
        **kwargs
    ) -> httpx.Response:
        """Make HTTP request with retry logic"""
        import time
        start_time = time.time()
        last_exception = None
        
        # Log request details
        request_data = {
            "method": method,
            "url": url,
            "headers": kwargs.get("headers", {}),
            "params": kwargs.get("params", {}),
            "json": kwargs.get("json", {}),
            "data": kwargs.get("data", {})
        }
        
        # Mask sensitive data in logs
        masked_request = self._mask_sensitive_data(request_data.copy())
        self.log_info(
            "SSI API Request",
            **masked_request
        )
        
        for attempt in range(self.retries + 1):
            try:
                self.log_debug(
                    "Making request",
                    method=method,
                    url=url,
                    attempt=attempt + 1,
                    max_attempts=self.retries + 1
                )
                
                response = await self.client.request(method, url, **kwargs)
                
                # Calculate duration
                duration_ms = (time.time() - start_time) * 1000
                
                # Log response details
                try:
                    response_data = response.json() if response.content else {}
                    masked_response = self._mask_sensitive_data(response_data.copy())
                    
                    self.log_info(
                        "SSI API Response",
                        method=method,
                        url=url,
                        status_code=response.status_code,
                        response_size=len(response.content) if response.content else 0,
                        response_data=masked_response
                    )
                except Exception as e:
                    # If response is not JSON, log text content (truncated)
                    response_text = response.text[:500] if response.text else ""
                    self.log_info(
                        "SSI API Response (non-JSON)",
                        method=method,
                        url=url,
                        status_code=response.status_code,
                        response_size=len(response.content) if response.content else 0,
                        response_text=response_text,
                        parse_error=str(e)
                    )
                
                # Log performance metrics
                self._log_api_performance(
                    method=method,
                    endpoint=url.split(self.base_url)[-1] if self.base_url in url else url,
                    duration_ms=duration_ms,
                    status_code=response.status_code,
                    response_size=len(response.content) if response.content else 0
                )
                
                # Check for errors
                self._handle_response_errors(response)
                return response
                
            except (httpx.TimeoutException, httpx.ConnectError) as e:
                last_exception = SSINetworkError(f"Network error: {e}")
                if attempt < self.retries:
                    wait_time = settings.retry_delay * (2 ** attempt)  # Exponential backoff
                    self.log_warning(
                        "Request failed, retrying",
                        error=str(e),
                        attempt=attempt + 1,
                        wait_time=wait_time
                    )
                    await asyncio.sleep(wait_time)
                else:
                    break
            except SSIAPIError:
                # Don't retry API errors
                raise
            except Exception as e:
                last_exception = SSINetworkError(f"Unexpected error: {e}")
                break
        
        # If we get here, all retries failed
        raise last_exception or SSINetworkError("All retry attempts failed")
    
    def _mask_sensitive_data(self, data: Any) -> Any:
        """Mask sensitive data in logs"""
        if isinstance(data, dict):
            masked = {}
            for key, value in data.items():
                key_lower = key.lower()
                if any(sensitive in key_lower for sensitive in [
                    'password', 'token', 'secret', 'key', 'auth', 
                    'consumer_secret', 'access_token', 'accesstoken',
                    'code', 'otp', 'pin'
                ]):
                    # Show only first 4 and last 4 characters for tokens/secrets
                    if isinstance(value, str) and len(value) > 8:
                        masked[key] = f"{value[:4]}***{value[-4:]}"
                    else:
                        masked[key] = "***MASKED***"
                else:
                    masked[key] = self._mask_sensitive_data(value)
            return masked
        elif isinstance(data, list):
            return [self._mask_sensitive_data(item) for item in data]
        else:
            return data
    
    def _log_api_performance(
        self, 
        method: str, 
        endpoint: str, 
        duration_ms: float,
        status_code: int,
        response_size: int = 0
    ) -> None:
        """Log API performance metrics"""
        self.log_info(
            "SSI API Performance",
            method=method,
            endpoint=endpoint,
            duration_ms=round(duration_ms, 2),
            status_code=status_code,
            response_size_bytes=response_size,
            provider="SSI"
        )
    
    async def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Make GET request"""
        url = self._build_url(endpoint)
        response = await self._make_request_with_retry(
            "GET", url, params=params, headers=headers, **kwargs
        )
        return response.json()
    
    async def post(
        self,
        endpoint: str,
        data: Optional[Union[Dict[str, Any], str]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Make POST request"""
        url = self._build_url(endpoint)
        response = await self._make_request_with_retry(
            "POST", url, data=data, json=json, headers=headers, **kwargs
        )
        return response.json()
    
    async def put(
        self,
        endpoint: str,
        data: Optional[Union[Dict[str, Any], str]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Make PUT request"""
        url = self._build_url(endpoint)
        response = await self._make_request_with_retry(
            "PUT", url, data=data, json=json, headers=headers, **kwargs
        )
        return response.json()
    
    async def delete(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Make DELETE request"""
        url = self._build_url(endpoint)
        response = await self._make_request_with_retry(
            "DELETE", url, headers=headers, **kwargs
        )
        return response.json()
