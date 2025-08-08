"""
Common security utilities and authentication helpers.
"""

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Union

from jose import JWTError, jwt
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, Request

from .config import get_settings
from .logging import get_logger
from .utils import generate_uuid, hash_password, verify_password

logger = get_logger(__name__)


class SecurityManager:
    """Security and authentication manager."""
    
    def __init__(self):
        """Initialize security manager."""
        self.settings = get_settings().security
        self.security = HTTPBearer()
    
    def create_access_token(
        self, 
        data: Dict[str, Any], 
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create JWT access token."""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=self.settings.access_token_expire_minutes
            )
        
        to_encode.update({"exp": expire, "type": "access"})
        
        encoded_jwt = jwt.encode(
            to_encode, 
            self.settings.secret_key, 
            algorithm=self.settings.algorithm
        )
        
        return encoded_jwt
    
    def create_refresh_token(self, data: Dict[str, Any]) -> str:
        """Create JWT refresh token."""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=self.settings.refresh_token_expire_days)
        to_encode.update({"exp": expire, "type": "refresh"})
        
        encoded_jwt = jwt.encode(
            to_encode, 
            self.settings.secret_key, 
            algorithm=self.settings.algorithm
        )
        
        return encoded_jwt
    
    def verify_token(self, token: str, token_type: str = "access") -> Dict[str, Any]:
        """Verify and decode JWT token."""
        try:
            payload = jwt.decode(
                token, 
                self.settings.secret_key, 
                algorithms=[self.settings.algorithm]
            )
            
            if payload.get("type") != token_type:
                raise JWTError("Invalid token type")
            
            return payload
            
        except JWTError as e:
            logger.warning(f"Token verification failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    def get_current_user(
        self, 
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
    ) -> Dict[str, Any]:
        """Get current user from JWT token."""
        token = credentials.credentials
        payload = self.verify_token(token)
        
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return payload
    
    def create_api_key(self, user_id: str, permissions: Optional[list] = None) -> str:
        """Create API key for service-to-service communication."""
        data = {
            "sub": user_id,
            "type": "api_key",
            "permissions": permissions or [],
            "created_at": datetime.utcnow().isoformat()
        }
        
        # API keys don't expire by default
        encoded_jwt = jwt.encode(
            data, 
            self.settings.secret_key, 
            algorithm=self.settings.algorithm
        )
        
        return encoded_jwt
    
    def verify_api_key(self, api_key: str) -> Dict[str, Any]:
        """Verify API key."""
        try:
            payload = jwt.decode(
                api_key, 
                self.settings.secret_key, 
                algorithms=[self.settings.algorithm]
            )
            
            if payload.get("type") != "api_key":
                raise JWTError("Invalid API key")
            
            return payload
            
        except JWTError as e:
            logger.warning(f"API key verification failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key",
            )
    
    def hash_password(self, password: str) -> str:
        """Hash password."""
        return hash_password(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password."""
        return verify_password(plain_password, hashed_password)


class PermissionChecker:
    """Permission and authorization checker."""
    
    def __init__(self, required_permissions: list):
        """Initialize permission checker."""
        self.required_permissions = required_permissions
    
    def __call__(self, current_user: Dict[str, Any] = Depends(SecurityManager().get_current_user)):
        """Check if user has required permissions."""
        user_permissions = current_user.get("permissions", [])
        
        for permission in self.required_permissions:
            if permission not in user_permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permission denied. Required: {permission}"
                )
        
        return current_user


class RoleChecker:
    """Role-based authorization checker."""
    
    def __init__(self, required_roles: list):
        """Initialize role checker."""
        self.required_roles = required_roles
    
    def __call__(self, current_user: Dict[str, Any] = Depends(SecurityManager().get_current_user)):
        """Check if user has required roles."""
        user_roles = current_user.get("roles", [])
        
        if not any(role in user_roles for role in self.required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role access denied. Required one of: {self.required_roles}"
            )
        
        return current_user


class IPWhitelistChecker:
    """IP whitelist authorization checker."""
    
    def __init__(self, allowed_ips: list):
        """Initialize IP whitelist checker."""
        self.allowed_ips = allowed_ips
    
    def __call__(self, request: Request):
        """Check if request IP is in whitelist."""
        client_ip = request.client.host
        
        if client_ip not in self.allowed_ips:
            logger.security_event(
                "unauthorized_ip_access",
                ip=client_ip,
                allowed_ips=self.allowed_ips
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="IP not authorized"
            )
        
        return True


# Global security manager instance
security_manager = SecurityManager()

# Common dependency functions
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
) -> Dict[str, Any]:
    """FastAPI dependency to get current user."""
    return security_manager.get_current_user(credentials)


def get_admin_user(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """FastAPI dependency to get admin user."""
    if "admin" not in current_user.get("roles", []):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


def get_trader_user(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """FastAPI dependency to get trader user."""
    if "trader" not in current_user.get("roles", []):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Trader access required"
        )
    return current_user


# Permission decorators
def require_permissions(*permissions):
    """Decorator to require specific permissions."""
    return PermissionChecker(list(permissions))


def require_roles(*roles):
    """Decorator to require specific roles."""
    return RoleChecker(list(roles))


def require_ip_whitelist(allowed_ips: list):
    """Decorator to require IP whitelist."""
    return IPWhitelistChecker(allowed_ips)
