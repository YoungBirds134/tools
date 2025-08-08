"""
SSI FastConnect API router for Config Service
"""

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional
import logging

from ..models import OTPRequest, VerifyCodeRequest, SSIResponse
from ..services.ssi_service import SSIService
from ..config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


def get_ssi_service() -> SSIService:
    """Get SSI service instance"""
    # This would be injected from the main app
    # For now, we'll create a new instance
    return SSIService(settings)


@router.get("/access-token")
async def get_access_token(ssi_service: SSIService = Depends(get_ssi_service)):
    """Get SSI FastConnect Data API access token"""
    try:
        token = await ssi_service.get_access_token()
        return SSIResponse(
            success=True,
            message="Access token retrieved successfully",
            data={
                "access_token": token,
                "expires_in": ssi_service.token_expires_in
            }
        )
    except Exception as e:
        logger.error(f"Failed to get access token: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get access token: {str(e)}")


@router.get("/trading-access-token")
async def get_trading_access_token(ssi_service: SSIService = Depends(get_ssi_service)):
    """Get SSI FastConnect Trading API access token"""
    try:
        token = await ssi_service.get_trading_access_token()
        return SSIResponse(
            success=True,
            message="Trading access token retrieved successfully",
            data={
                "access_token": token,
                "expires_in": ssi_service.trading_token_expires_in
            }
        )
    except Exception as e:
        logger.error(f"Failed to get trading access token: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get trading access token: {str(e)}")


@router.post("/get-otp")
async def get_otp(request: OTPRequest, ssi_service: SSIService = Depends(get_ssi_service)):
    """Get OTP for 2FA authentication"""
    try:
        result = await ssi_service.get_otp()
        return SSIResponse(
            success=True,
            message="OTP request successful",
            data=result
        )
    except Exception as e:
        logger.error(f"Failed to get OTP: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get OTP: {str(e)}")


@router.post("/verify-code")
async def verify_code(request: VerifyCodeRequest, ssi_service: SSIService = Depends(get_ssi_service)):
    """Verify OTP/PIN code for 2FA"""
    try:
        # This would typically involve verifying the code with SSI
        # For now, we'll return a mock response
        return SSIResponse(
            success=True,
            message="Code verified successfully",
            data={
                "verified": True,
                "account": request.account
            }
        )
    except Exception as e:
        logger.error(f"Failed to verify code: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to verify code: {str(e)}")


@router.get("/health")
async def ssi_health_check(ssi_service: SSIService = Depends(get_ssi_service)):
    """Check SSI service health"""
    try:
        is_healthy = ssi_service.is_healthy()
        return SSIResponse(
            success=True,
            message="SSI service health check",
            data={
                "healthy": is_healthy,
                "initialized": ssi_service.is_initialized,
                "circuit_open": ssi_service.circuit_open
            }
        )
    except Exception as e:
        logger.error(f"SSI health check failed: {str(e)}")
        return SSIResponse(
            success=False,
            message="SSI service health check failed",
            data={
                "healthy": False,
                "error": str(e)
            }
        )


@router.post("/refresh-tokens")
async def refresh_tokens(ssi_service: SSIService = Depends(get_ssi_service)):
    """Manually refresh SSI tokens"""
    try:
        await ssi_service._refresh_tokens()
        return SSIResponse(
            success=True,
            message="Tokens refreshed successfully",
            data={
                "data_token_valid": ssi_service.access_token is not None,
                "trading_token_valid": ssi_service.trading_access_token is not None
            }
        )
    except Exception as e:
        logger.error(f"Failed to refresh tokens: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to refresh tokens: {str(e)}")


@router.get("/config")
async def get_ssi_config(ssi_service: SSIService = Depends(get_ssi_service)):
    """Get SSI configuration (without sensitive data)"""
    try:
        return SSIResponse(
            success=True,
            message="SSI configuration retrieved",
            data={
                "consumer_id_configured": bool(ssi_service.consumer_id),
                "consumer_secret_configured": bool(ssi_service.consumer_secret),
                "private_key_configured": bool(ssi_service.private_key),
                "fc_trading_url": ssi_service.fc_trading_url,
                "fc_data_url": ssi_service.fc_data_url,
                "two_fa_type": ssi_service.two_fa_type,
                "notify_id": ssi_service.notify_id
            }
        )
    except Exception as e:
        logger.error(f"Failed to get SSI config: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get SSI config: {str(e)}") 