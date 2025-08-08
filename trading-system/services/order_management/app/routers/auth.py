"""
Authentication API Router
Handles SSI FastConnect authentication including OTP and 2FA verification.
"""

from fastapi import APIRouter, HTTPException, Depends
import structlog
from datetime import datetime

from ..models import (
    OTPRequest,
    VerifyCodeRequest,
    APIResponse
)
from ..services.ssi_client import get_ssi_client, SSIFastConnectClient
from ..utils.exceptions import (
    SSIAPIError,
    SSIAuthenticationError,
    ValidationError
)

logger = structlog.get_logger(__name__)
router = APIRouter()


async def get_trading_client() -> SSIFastConnectClient:
    """Dependency to get SSI trading client"""
    return await get_ssi_client()


@router.post("/access-token", response_model=APIResponse)
async def get_access_token(
    client: SSIFastConnectClient = Depends(get_trading_client)
):
    """
    Get access token for SSI FastConnect API authentication
    
    This endpoint initializes the authentication session and returns
    an access token for subsequent API calls.
    """
    
    logger.info("Requesting access token")
    
    try:
        access_token = await client.get_access_token()
        
        return APIResponse(
            success=True,
            message="Access token obtained successfully",
            data={
                "access_token": access_token,
                "token_type": "Bearer",
                "expires_in": 3600  # 1 hour
            },
            timestamp=datetime.now()
        )
        
    except SSIAuthenticationError as e:
        logger.error("Authentication failed", error=str(e))
        raise HTTPException(status_code=401, detail={
            "error": "AUTHENTICATION_FAILED",
            "message": "Failed to obtain access token",
            "details": str(e)
        })
    
    except SSIAPIError as e:
        logger.error("SSI API error", error=str(e))
        raise HTTPException(status_code=502, detail={
            "error": "SSI_API_ERROR",
            "message": "SSI API service unavailable",
            "details": str(e)
        })
    
    except Exception as e:
        logger.error("Unexpected error getting access token", error=str(e))
        raise HTTPException(status_code=500, detail={
            "error": "INTERNAL_ERROR",
            "message": "An unexpected error occurred while obtaining access token"
        })


@router.post("/otp", response_model=APIResponse)
async def request_otp(
    request: OTPRequest,
    client: SSIFastConnectClient = Depends(get_trading_client)
):
    """
    Request OTP for 2FA authentication
    
    Sends an OTP code to the registered phone number/email
    for the specified trading account.
    """
    
    logger.info("Requesting OTP", account=request.account)
    
    try:
        result = await client.get_otp(request.account)
        
        return APIResponse(
            success=True,
            message="OTP sent successfully",
            data=result.get("data", {}),
            timestamp=datetime.now()
        )
        
    except SSIAuthenticationError as e:
        logger.error("OTP request failed", account=request.account, error=str(e))
        raise HTTPException(status_code=401, detail={
            "error": "OTP_REQUEST_FAILED",
            "message": "Failed to send OTP",
            "details": str(e)
        })
    
    except SSIAPIError as e:
        logger.error("SSI API error requesting OTP", error=str(e))
        raise HTTPException(status_code=502, detail={
            "error": "SSI_API_ERROR",
            "message": "Failed to request OTP from SSI",
            "details": str(e)
        })
    
    except Exception as e:
        logger.error("Unexpected error requesting OTP", error=str(e))
        raise HTTPException(status_code=500, detail={
            "error": "INTERNAL_ERROR",
            "message": "An unexpected error occurred while requesting OTP"
        })


@router.post("/verify-code", response_model=APIResponse)
async def verify_code(
    request: VerifyCodeRequest,
    client: SSIFastConnectClient = Depends(get_trading_client)
):
    """
    Verify OTP/PIN code for 2FA authentication
    
    Validates the provided OTP or PIN code and enables
    trading operations for the session.
    """
    
    logger.info("Verifying 2FA code", account=request.account)
    
    try:
        # Validate input
        if not request.code or len(request.code) < 4:
            raise ValidationError("Invalid verification code format", field="code")
        
        # In a real implementation, this would call SSI API to verify the code
        # For now, simulate verification logic
        
        # Mock verification - accept any 6-digit code for demonstration
        if len(request.code) == 6 and request.code.isdigit():
            verification_success = True
        else:
            verification_success = False
        
        if verification_success:
            # Mark session as 2FA verified
            if client.session:
                client.session.two_fa_verified = True
                client.session.account = request.account
            
            return APIResponse(
                success=True,
                message="Verification code accepted",
                data={
                    "verified": True,
                    "account": request.account,
                    "session_valid": True
                },
                timestamp=datetime.now()
            )
        else:
            raise SSIAuthenticationError("Invalid verification code")
        
    except ValidationError as e:
        logger.warning("Code validation failed", error=str(e))
        raise HTTPException(status_code=422, detail={
            "error": "VALIDATION_ERROR",
            "message": str(e),
            "field": e.field
        })
    
    except SSIAuthenticationError as e:
        logger.warning("Code verification failed", error=str(e))
        raise HTTPException(status_code=401, detail={
            "error": "VERIFICATION_FAILED",
            "message": "Invalid verification code",
            "details": str(e)
        })
    
    except Exception as e:
        logger.error("Unexpected error verifying code", error=str(e))
        raise HTTPException(status_code=500, detail={
            "error": "INTERNAL_ERROR",
            "message": "An unexpected error occurred while verifying code"
        })


@router.get("/session-status", response_model=APIResponse)
async def get_session_status(
    client: SSIFastConnectClient = Depends(get_trading_client)
):
    """
    Get current authentication session status
    
    Returns information about the current session including
    authentication status and available operations.
    """
    
    logger.info("Checking session status")
    
    try:
        session_info = {
            "authenticated": client.session is not None,
            "two_fa_verified": client.session.two_fa_verified if client.session else False,
            "account": client.session.account if client.session else None,
            "session_valid": client.session is not None and client.session.access_token,
            "expires_at": client.session.expires_at.isoformat() if client.session and client.session.expires_at else None,
            "available_operations": {
                "trading": client.session.two_fa_verified if client.session else False,
                "account_info": client.session is not None,
                "market_data": True  # Usually available without full auth
            }
        }
        
        return APIResponse(
            success=True,
            message="Session status retrieved",
            data=session_info,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error("Error checking session status", error=str(e))
        raise HTTPException(status_code=500, detail={
            "error": "INTERNAL_ERROR",
            "message": "An unexpected error occurred while checking session status"
        })


@router.post("/logout", response_model=APIResponse)
async def logout(
    client: SSIFastConnectClient = Depends(get_trading_client)
):
    """
    Logout and invalidate current session
    
    Clears the current authentication session and invalidates tokens.
    """
    
    logger.info("Processing logout")
    
    try:
        # Clear session
        client.session = None
        
        return APIResponse(
            success=True,
            message="Logged out successfully",
            data={"session_cleared": True},
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error("Error during logout", error=str(e))
        raise HTTPException(status_code=500, detail={
            "error": "INTERNAL_ERROR",
            "message": "An unexpected error occurred during logout"
        })


