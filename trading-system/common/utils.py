"""
Common utilities and helper functions.
"""

import hashlib
import secrets
import time
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union

import httpx
from passlib.context import CryptContext


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_uuid() -> str:
    """Generate UUID string."""
    return str(uuid.uuid4())


def generate_request_id() -> str:
    """Generate unique request ID."""
    return f"req_{int(time.time())}_{secrets.token_hex(8)}"


def generate_api_key() -> str:
    """Generate API key."""
    return secrets.token_urlsafe(32)


def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_signature(data: str, secret: str) -> str:
    """Create HMAC-SHA256 signature."""
    import hmac
    return hmac.new(
        secret.encode('utf-8'),
        data.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()


def verify_signature(data: str, signature: str, secret: str) -> bool:
    """Verify HMAC-SHA256 signature."""
    expected_signature = create_signature(data, secret)
    return secrets.compare_digest(signature, expected_signature)


def get_current_timestamp() -> datetime:
    """Get current UTC timestamp."""
    return datetime.now(timezone.utc)


def get_current_timestamp_ms() -> int:
    """Get current timestamp in milliseconds."""
    return int(time.time() * 1000)


def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format datetime to string."""
    return dt.strftime(format_str)


def parse_datetime(dt_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    """Parse datetime from string."""
    return datetime.strptime(dt_str, format_str)


def sanitize_string(value: str, max_length: int = 255) -> str:
    """Sanitize string input."""
    if not value:
        return ""
    
    # Remove null bytes and control characters
    sanitized = ''.join(char for char in value if ord(char) >= 32)
    
    # Truncate to max length
    return sanitized[:max_length].strip()


def validate_email(email: str) -> bool:
    """Basic email validation."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def mask_sensitive_data(data: str, mask_char: str = "*", visible_chars: int = 4) -> str:
    """Mask sensitive data showing only last few characters."""
    if len(data) <= visible_chars:
        return mask_char * len(data)
    
    masked_length = len(data) - visible_chars
    return mask_char * masked_length + data[-visible_chars:]


def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """Split list into chunks of specified size."""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
    """Flatten nested dictionary."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def safe_float(value: Any, default: float = 0.0) -> float:
    """Safely convert value to float."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def safe_int(value: Any, default: int = 0) -> int:
    """Safely convert value to int."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """Calculate percentage change between two values."""
    if old_value == 0:
        return 0.0
    return ((new_value - old_value) / old_value) * 100


def round_to_tick_size(price: float, tick_size: float) -> float:
    """Round price to nearest tick size."""
    if tick_size <= 0:
        return price
    return round(price / tick_size) * tick_size


def calculate_position_size(
    account_balance: float,
    risk_percentage: float,
    entry_price: float,
    stop_loss_price: float
) -> int:
    """Calculate position size based on risk management."""
    risk_amount = account_balance * (risk_percentage / 100)
    price_diff = abs(entry_price - stop_loss_price)
    
    if price_diff <= 0:
        return 0
    
    shares = int(risk_amount / price_diff)
    return max(0, shares)


class RateLimiter:
    """Simple in-memory rate limiter."""
    
    def __init__(self, max_requests: int, time_window: int):
        """Initialize rate limiter.
        
        Args:
            max_requests: Maximum number of requests allowed
            time_window: Time window in seconds
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = {}
    
    def is_allowed(self, key: str) -> bool:
        """Check if request is allowed for given key."""
        current_time = time.time()
        
        if key not in self.requests:
            self.requests[key] = []
        
        # Remove old requests outside time window
        self.requests[key] = [
            req_time for req_time in self.requests[key]
            if current_time - req_time < self.time_window
        ]
        
        # Check if under limit
        if len(self.requests[key]) < self.max_requests:
            self.requests[key].append(current_time)
            return True
        
        return False
    
    def get_remaining_requests(self, key: str) -> int:
        """Get remaining requests for key."""
        if key not in self.requests:
            return self.max_requests
        
        current_time = time.time()
        valid_requests = [
            req_time for req_time in self.requests[key]
            if current_time - req_time < self.time_window
        ]
        
        return max(0, self.max_requests - len(valid_requests))
    
    def get_reset_time(self, key: str) -> Optional[int]:
        """Get reset time for key."""
        if key not in self.requests or not self.requests[key]:
            return None
        
        oldest_request = min(self.requests[key])
        return int(oldest_request + self.time_window)


class HTTPClient:
    """HTTP client with retry and timeout handling."""
    
    def __init__(self, timeout: int = 30, max_retries: int = 3):
        """Initialize HTTP client."""
        self.timeout = timeout
        self.max_retries = max_retries
        self.client = httpx.AsyncClient(timeout=timeout)
    
    async def request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        retry_count: int = 0
    ) -> httpx.Response:
        """Make HTTP request with retry logic."""
        try:
            response = await self.client.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=json_data,
                data=data
            )
            response.raise_for_status()
            return response
            
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            if retry_count < self.max_retries:
                await asyncio.sleep(2 ** retry_count)  # Exponential backoff
                return await self.request(
                    method, url, headers, params, json_data, data, retry_count + 1
                )
            raise e
    
    async def get(self, url: str, **kwargs) -> httpx.Response:
        """Make GET request."""
        return await self.request("GET", url, **kwargs)
    
    async def post(self, url: str, **kwargs) -> httpx.Response:
        """Make POST request."""
        return await self.request("POST", url, **kwargs)
    
    async def put(self, url: str, **kwargs) -> httpx.Response:
        """Make PUT request."""
        return await self.request("PUT", url, **kwargs)
    
    async def delete(self, url: str, **kwargs) -> httpx.Response:
        """Make DELETE request."""
        return await self.request("DELETE", url, **kwargs)
    
    async def close(self):
        """Close HTTP client."""
        await self.client.aclose()


# Import asyncio here to avoid circular imports
import asyncio
