"""
FC Trading API routes
"""
from fastapi import APIRouter, Depends, HTTPException, Query, Body, status, Header
from typing import Optional
from decimal import Decimal
from app.services.fc_trading_service import FCTradingService
from app.schemas.fc_trading import *
from app.schemas.base import ErrorResponse
from app.core.exceptions import (
    SSIIntegrationError, ssi_integration_error_to_http_exception,
    SSIAPIError, ssi_api_error_to_http_exception
)

router = APIRouter(prefix="/fc-trading", tags=["FC Trading"])


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


# Authentication endpoints
@router.post(
    "/auth/token",
    response_model=AccessTokenResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Get Access Token",
    description="Authenticate and get access token for trading operations"
)
async def get_access_token(
    request: AccessTokenRequest = Body(..., 
        example={
            "consumer_id": "your_consumer_id",
            "consumer_secret": "your_consumer_secret",
            "code": "123456",
            "two_factor_type": 1,
            "is_save": True
        }
    ),
    service: FCTradingService = Depends(get_fc_trading_service)
) -> AccessTokenResponse:
    """Get access token"""
    try:
        return await service.authenticate(request)
    
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
    "/auth/otp",
    response_model=GetOTPResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Request OTP",
    description="Request One-Time Password for 2FA authentication"
)
async def request_otp(
    request: GetOTPRequest = Body(...,
        example={
            "consumer_id": "your_consumer_id",
            "consumer_secret": "your_consumer_secret"
        }
    ),
    service: FCTradingService = Depends(get_fc_trading_service)
) -> GetOTPResponse:
    """Request OTP"""
    try:
        return await service.request_otp(request)
    
    except SSIAPIError as e:
        raise ssi_api_error_to_http_exception(e)
    except SSIIntegrationError as e:
        raise ssi_integration_error_to_http_exception(e)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal server error", "error": str(e)}
        )


# Order Management endpoints
@router.post(
    "/orders",
    response_model=NewOrderResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        422: {"model": ErrorResponse, "description": "Validation Error"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Place New Order",
    description="Place a new buy/sell order"
)
async def place_order(
    request: NewOrderRequest = Body(...,
        example={
            "account": "Q023951",
            "instrument_id": "SSI",
            "market": "VN",
            "buy_sell": "B",
            "order_type": "LO",
            "price": 25000,
            "quantity": 100,
            "stop_order": False
        }
    ),
    service: FCTradingService = Depends(get_fc_trading_service)
) -> NewOrderResponse:
    """Place new order"""
    try:
        return await service.place_order(request)
    
    except SSIAPIError as e:
        raise ssi_api_error_to_http_exception(e)
    except SSIIntegrationError as e:
        raise ssi_integration_error_to_http_exception(e)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal server error", "error": str(e)}
        )


@router.put(
    "/orders/{order_id}",
    response_model=ModifyOrderResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "Order Not Found"},
        422: {"model": ErrorResponse, "description": "Validation Error"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Modify Order",
    description="Modify an existing order"
)
async def modify_order(
    order_id: str,
    request: ModifyOrderRequest = Body(...,
        example={
            "account": "Q023951",
            "order_id": "12345678",
            "instrument_id": "SSI",
            "market_id": "VN",
            "buy_sell": "B",
            "order_type": "LO",
            "price": 26000,
            "quantity": 200
        }
    ),
    service: FCTradingService = Depends(get_fc_trading_service)
) -> ModifyOrderResponse:
    """Modify existing order"""
    try:
        # Ensure order_id in request matches path parameter
        request.order_id = order_id
        return await service.modify_order(request)
    
    except SSIAPIError as e:
        raise ssi_api_error_to_http_exception(e)
    except SSIIntegrationError as e:
        raise ssi_integration_error_to_http_exception(e)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal server error", "error": str(e)}
        )


@router.delete(
    "/orders/{order_id}",
    response_model=CancelOrderResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "Order Not Found"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Cancel Order",
    description="Cancel an existing order"
)
async def cancel_order(
    order_id: str,
    request: CancelOrderRequest = Body(...,
        example={
            "account": "Q023951",
            "order_id": "12345678",
            "instrument_id": "SSI",
            "market_id": "VN",
            "buy_sell": "B"
        }
    ),
    service: FCTradingService = Depends(get_fc_trading_service)
) -> CancelOrderResponse:
    """Cancel existing order"""
    try:
        # Ensure order_id in request matches path parameter
        request.order_id = order_id
        return await service.cancel_order(request)
    
    except SSIAPIError as e:
        raise ssi_api_error_to_http_exception(e)
    except SSIIntegrationError as e:
        raise ssi_integration_error_to_http_exception(e)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal server error", "error": str(e)}
        )


# Query endpoints
@router.get(
    "/orders",
    response_model=OrderBookResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Get Current Orders",
    description="Get current active orders (order book)"
)
async def get_orders(
    account: str = Query(..., description="Trading account"),
    service: FCTradingService = Depends(get_fc_trading_service)
) -> OrderBookResponse:
    """Get current orders"""
    try:
        request = OrderBookRequest(account=account)
        return await service.get_orders(request)
    
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
    "/orders/history",
    response_model=OrderHistoryResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Get Order History",
    description="Get historical orders within date range"
)
async def get_order_history(
    account: str = Query(..., description="Trading account"),
    start_date: str = Query(..., description="Start date (dd/mm/yyyy)"),
    end_date: str = Query(..., description="End date (dd/mm/yyyy)"),
    service: FCTradingService = Depends(get_fc_trading_service)
) -> OrderHistoryResponse:
    """Get order history"""
    try:
        request = OrderHistoryRequest(
            account=account,
            start_date=start_date,
            end_date=end_date
        )
        return await service.get_order_history(request)
    
    except SSIAPIError as e:
        raise ssi_api_error_to_http_exception(e)
    except SSIIntegrationError as e:
        raise ssi_integration_error_to_http_exception(e)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal server error", "error": str(e)}
        )


# Account Information endpoints
@router.get(
    "/account/balance",
    response_model=CashAccountBalanceResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Get Account Balance",
    description="Get cash account balance information"
)
async def get_account_balance(
    account: str = Query(..., description="Trading account"),
    service: FCTradingService = Depends(get_fc_trading_service)
) -> CashAccountBalanceResponse:
    """Get account balance"""
    try:
        request = CashAccountBalanceRequest(account=account)
        return await service.get_account_balance(request)
    
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
    "/account/positions",
    response_model=StockPositionResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Get Stock Positions",
    description="Get current stock positions"
)
async def get_positions(
    account: str = Query(..., description="Trading account"),
    service: FCTradingService = Depends(get_fc_trading_service)
) -> StockPositionResponse:
    """Get stock positions"""
    try:
        request = StockPositionRequest(account=account)
        return await service.get_positions(request)
    
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
    "/account/portfolio",
    response_model=PortfolioResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Get Portfolio",
    description="Get portfolio summary with P&L information"
)
async def get_portfolio(
    account: str = Query(..., description="Trading account"),
    service: FCTradingService = Depends(get_fc_trading_service)
) -> PortfolioResponse:
    """Get portfolio"""
    try:
        request = PortfolioRequest(account=account)
        return await service.get_portfolio(request)
    
    except SSIAPIError as e:
        raise ssi_api_error_to_http_exception(e)
    except SSIIntegrationError as e:
        raise ssi_integration_error_to_http_exception(e)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal server error", "error": str(e)}
        )


# Trading Power endpoints
@router.get(
    "/account/max-buy-qty",
    response_model=MaxBuyQtyResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Get Maximum Buy Quantity",
    description="Get maximum quantity that can be bought for a specific stock at given price"
)
async def get_max_buy_qty(
    account: str = Query(..., description="Trading account"),
    instrument_id: str = Query(..., max_length=10, description="Stock symbol"),
    price: Decimal = Query(..., gt=0, description="Order price"),
    service: FCTradingService = Depends(get_fc_trading_service)
) -> MaxBuyQtyResponse:
    """Get maximum buy quantity"""
    try:
        request = MaxBuyQtyRequest(
            account=account,
            instrument_id=instrument_id,
            price=price
        )
        return await service.get_buying_power(request)
    
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
    "/account/max-sell-qty",
    response_model=MaxSellQtyResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Get Maximum Sell Quantity",
    description="Get maximum quantity that can be sold for a specific stock"
)
async def get_max_sell_qty(
    account: str = Query(..., description="Trading account"),
    instrument_id: str = Query(..., max_length=10, description="Stock symbol"),
    service: FCTradingService = Depends(get_fc_trading_service)
) -> MaxSellQtyResponse:
    """Get maximum sell quantity"""
    try:
        request = MaxSellQtyRequest(
            account=account,
            instrument_id=instrument_id
        )
        return await service.get_selling_power(request)
    
    except SSIAPIError as e:
        raise ssi_api_error_to_http_exception(e)
    except SSIIntegrationError as e:
        raise ssi_integration_error_to_http_exception(e)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal server error", "error": str(e)}
        )


# Derivative Trading endpoints
@router.post(
    "/deriv/orders",
    response_model=NewOrderResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        422: {"model": ErrorResponse, "description": "Validation Error"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Place New Derivative Order",
    description="Place a new derivative buy/sell order"
)
async def place_deriv_order(
    request: DerivNewOrderRequest = Body(...,
        example={
            "account": "Q023951",
            "instrument_id": "VN30F2501",
            "market": "VNFE",
            "buy_sell": "B",
            "order_type": "LO",
            "price": 1300,
            "quantity": 1
        }
    ),
    service: FCTradingService = Depends(get_fc_trading_service)
) -> NewOrderResponse:
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


@router.put(
    "/deriv/orders/{order_id}",
    response_model=ModifyOrderResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "Order Not Found"},
        422: {"model": ErrorResponse, "description": "Validation Error"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Modify Derivative Order",
    description="Modify an existing derivative order"
)
async def modify_deriv_order(
    order_id: str,
    request: DerivModifyOrderRequest = Body(...,
        example={
            "account": "Q023951",
            "order_id": "12345678",
            "instrument_id": "VN30F2501",
            "market_id": "VNFE",
            "buy_sell": "B",
            "order_type": "LO",
            "price": 1310,
            "quantity": 2
        }
    ),
    service: FCTradingService = Depends(get_fc_trading_service)
) -> ModifyOrderResponse:
    """Modify existing derivative order"""
    try:
        # Ensure order_id in request matches path parameter
        request.order_id = order_id
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
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal server error", "error": str(e)}
        )


@router.delete(
    "/deriv/orders/{order_id}",
    response_model=CancelOrderResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "Order Not Found"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Cancel Derivative Order",
    description="Cancel an existing derivative order"
)
async def cancel_deriv_order(
    order_id: str,
    request: DerivCancelOrderRequest = Body(...,
        example={
            "account": "Q023951",
            "order_id": "12345678",
            "instrument_id": "VN30F2501",
            "market_id": "VNFE",
            "buy_sell": "B"
        }
    ),
    service: FCTradingService = Depends(get_fc_trading_service)
) -> CancelOrderResponse:
    """Cancel existing derivative order"""
    try:
        # Ensure order_id in request matches path parameter
        request.order_id = order_id
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


@router.get(
    "/deriv/account/balance",
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
    "/deriv/account/positions",
    response_model=DerivPositionResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Get Derivative Positions",
    description="Get current derivative positions"
)
async def get_deriv_positions(
    account: str = Query(..., description="Derivative trading account"),
    service: FCTradingService = Depends(get_fc_trading_service)
) -> DerivPositionResponse:
    """Get derivative positions"""
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
