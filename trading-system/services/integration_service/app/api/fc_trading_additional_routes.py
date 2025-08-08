"""
Essential FC Trading API routes for core functionality
"""
from fastapi import APIRouter, Depends, HTTPException, Query, Body, status, Header
from typing import Optional
from decimal import Decimal
from app.services.fc_trading_service import FCTradingService
from app.schemas.fc_trading import (
    # Account Management
    AuditOrderBookRequest, AuditOrderBookResponse,
    DerivAccountBalanceRequest, DerivAccountBalanceResponse,
    PPMMRAccountRequest, PPMMRAccountResponse,
    DerivPositionRequest, DerivPositionResponse,
    RateLimitRequest, RateLimitResponse,
    
    # Derivative Trading
    DerivNewOrderRequest, DerivNewOrderResponse,
    DerivCancelOrderRequest, DerivCancelOrderResponse,
    DerivModifyOrderRequest, DerivModifyOrderResponse
)
from app.schemas.base import ErrorResponse
from app.core.exceptions import (
    SSIIntegrationError, ssi_integration_error_to_http_exception,
    SSIAPIError, ssi_api_error_to_http_exception
)

router = APIRouter(prefix="/fc-trading", tags=["FC Trading Additional"])


def extract_bearer_token(authorization: Optional[str] = Header(None)) -> Optional[str]:
    """Extract bearer token from Authorization header"""
    if authorization and authorization.startswith("Bearer "):
        return authorization[7:]  # Remove "Bearer " prefix
    return None


async def get_fc_trading_service(token: Optional[str] = Depends(extract_bearer_token)):
    """Dependency to get FC Trading service with token"""
    # Use Bearer token if provided, otherwise service will get token from Redis cache
    from config import settings
    effective_token = token  # Don't fall back to config token - let service handle Redis cache
    service = FCTradingService(access_token=effective_token)
    try:
        await service.__aenter__()
        yield service
    finally:
        await service.__aexit__(None, None, None)


# Essential Account Information endpoints only
@router.get(
    "/account/audit-order-book",
    response_model=AuditOrderBookResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Get Audit Order Book",
    description="Get audit order book for the account"
)
async def get_audit_order_book(
    account: str = Query(..., description="Trading account"),
    service: FCTradingService = Depends(get_fc_trading_service)
) -> AuditOrderBookResponse:
    """Get audit order book"""
    try:
        request = AuditOrderBookRequest(account=account)
        return await service.get_audit_order_book(request)
    
    except SSIAPIError as e:
        raise ssi_api_error_to_http_exception(e)
    except SSIIntegrationError as e:
        raise ssi_integration_error_to_http_exception(e)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal server error", "error": str(e)}
        )

@router.get(
    "/account/deriv-balance",
    response_model=DerivAccountBalanceResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Get Derivative Account Balance",
    description="Get derivative account balance information"
)
async def get_deriv_account_balance(
    account: str = Query(..., description="Derivative trading account"),
    service: FCTradingService = Depends(get_fc_trading_service)
) -> DerivAccountBalanceResponse:
    """Get derivative account balance"""
    try:
        request = DerivAccountBalanceRequest(account=account)
        return await service.get_deriv_account_balance(request)
    
    except SSIAPIError as e:
        raise ssi_api_error_to_http_exception(e)
    except SSIIntegrationError as e:
        raise ssi_integration_error_to_http_exception(e)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal server error", "error": str(e)}
        )


@router.get(
    "/account/ppmmr-account",
    response_model=PPMMRAccountResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Get PPMMR Account Information",
    description="Get PPMMR (Price-to-Margin Ratio) account information"
)
async def get_ppmmr_account(
    account: str = Query(..., description="Trading account"),
    service: FCTradingService = Depends(get_fc_trading_service)
) -> PPMMRAccountResponse:
    """Get PPMMR account information"""
    try:
        request = PPMMRAccountRequest(account=account)
        return await service.get_ppmmr_account(request)
    
    except SSIAPIError as e:
        raise ssi_api_error_to_http_exception(e)
    except SSIIntegrationError as e:
        raise ssi_integration_error_to_http_exception(e)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal server error", "error": str(e)}
        )


@router.get(
    "/account/deriv-position",
    response_model=DerivPositionResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Get Derivative Position",
    description="Get derivative trading positions"
)
async def get_deriv_position(
    account: str = Query(..., description="Derivative trading account"),
    service: FCTradingService = Depends(get_fc_trading_service)
) -> DerivPositionResponse:
    """Get derivative position"""
    try:
        request = DerivPositionRequest(account=account)
        return await service.get_deriv_position(request)
    
    except SSIAPIError as e:
        raise ssi_api_error_to_http_exception(e)
    except SSIIntegrationError as e:
        raise ssi_integration_error_to_http_exception(e)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal server error", "error": str(e)}
        )


@router.get(
    "/account/rate-limit",
    response_model=RateLimitResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Get Rate Limit Information",
    description="Get API rate limit information for the account"
)
async def get_rate_limit(
    account: str = Query(..., description="Trading account"),
    service: FCTradingService = Depends(get_fc_trading_service)
) -> RateLimitResponse:
    """Get rate limit information"""
    try:
        request = RateLimitRequest(account=account)
        return await service.get_rate_limit(request)
    
    except SSIAPIError as e:
        raise ssi_api_error_to_http_exception(e)
    except SSIIntegrationError as e:
        raise ssi_integration_error_to_http_exception(e)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal server error", "error": str(e)}
        )


# Essential Derivative Trading endpoints
@router.post(
    "/deriv/new-order",
    response_model=DerivNewOrderResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Place New Derivative Order",
    description="Place a new derivative trading order"
)
async def place_deriv_new_order(
    request: DerivNewOrderRequest = Body(...,
        example={
            "account": "1234567",
            "instrument_id": "VN30F2411",
            "market": "VNFE",
            "buy_sell": "B",
            "order_type": "LO",
            "price": 1280.0,
            "quantity": 1
        }
    ),
    service: FCTradingService = Depends(get_fc_trading_service)
) -> DerivNewOrderResponse:
    """Place new derivative order"""
    try:
        return await service.place_deriv_order(request)
    
    except SSIAPIError as e:
        raise ssi_api_error_to_http_exception(e)
    except SSIIntegrationError as e:
        raise ssi_integration_error_to_http_exception(e)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal server error", "error": str(e)}
        )


@router.post(
    "/deriv/cancel-order",
    response_model=DerivCancelOrderResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Cancel Derivative Order",
    description="Cancel an existing derivative order"
)
async def cancel_deriv_order(
    request: DerivCancelOrderRequest = Body(...,
        example={
            "account": "1234567",
            "order_id": "12345",
            "instrument_id": "VN30F2411",
            "market_id": "VNFE",
            "buy_sell": "B"
        }
    ),
    service: FCTradingService = Depends(get_fc_trading_service)
) -> DerivCancelOrderResponse:
    """Cancel derivative order"""
    try:
        return await service.cancel_deriv_order(request)
    
    except SSIAPIError as e:
        raise ssi_api_error_to_http_exception(e)
    except SSIIntegrationError as e:
        raise ssi_integration_error_to_http_exception(e)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal server error", "error": str(e)}
        )


@router.post(
    "/deriv/modify-order",
    response_model=DerivModifyOrderResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Modify Derivative Order",
    description="Modify an existing derivative order"
)
async def modify_deriv_order(
    request: DerivModifyOrderRequest = Body(...,
        example={
            "account": "1234567",
            "order_id": "12345",
            "instrument_id": "VN30F2411",
            "market_id": "VNFE",
            "buy_sell": "B",
            "order_type": "LO",
            "price": 1285.0,
            "quantity": 2
        }
    ),
    service: FCTradingService = Depends(get_fc_trading_service)
) -> DerivModifyOrderResponse:
    """Modify derivative order"""
    try:
        return await service.modify_deriv_order(request)
    
    except SSIAPIError as e:
        raise ssi_api_error_to_http_exception(e)
    except SSIIntegrationError as e:
        raise ssi_integration_error_to_http_exception(e)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal server error", "error": str(e)}
        )
