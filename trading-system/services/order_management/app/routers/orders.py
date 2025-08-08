"""
Orders API Router
Enhanced order management endpoints with comprehensive validation,
error handling, and logging.
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import Dict, Any
import structlog
from datetime import datetime

from ..models import (
    NewOrderRequest,
    ModifyOrderRequest, 
    CancelOrderRequest,
    OrderHistoryRequest,
    OrderResponse,
    APIResponse,
    OrderBookResponse
)
from ..services.ssi_client import get_ssi_client, SSIFastConnectClient
from ..utils.trading_validator import validate_trading_request, get_trading_session_info
from ..utils.exceptions import (
    TradingSessionError,
    ValidationError,
    OrderError,
    SSIAPIError
)

logger = structlog.get_logger(__name__)
router = APIRouter()


async def get_trading_client() -> SSIFastConnectClient:
    """Dependency to get SSI trading client"""
    return await get_ssi_client()


def validate_order_request(request: NewOrderRequest) -> None:
    """Validate order request against trading rules"""
    
    # Validate trading session and order type
    is_valid, message = validate_trading_request(
        market=request.market,
        order_type=request.order_type,
        action="place"
    )
    
    if not is_valid:
        raise TradingSessionError(message)
    
    # Additional business logic validations
    if request.quantity <= 0:
        raise ValidationError("Quantity must be positive", field="quantity")
    
    if request.price < 0:
        raise ValidationError("Price cannot be negative", field="price")
    
    # Validate special order type requirements
    if request.order_type.value in ["ATO", "ATC"] and request.price > 0:
        raise ValidationError("ATO/ATC orders should have price = 0", field="price")


@router.post("/new-order", response_model=OrderResponse, status_code=201)
async def place_new_order(
    request: NewOrderRequest,
    background_tasks: BackgroundTasks,
    client: SSIFastConnectClient = Depends(get_trading_client)
):
    """
    Place a new stock order
    
    This endpoint validates the order against trading session rules,
    submits to SSI FastConnect API, and returns the order result.
    """
    
    logger.info("Processing new order request", 
                instrument=request.instrument_id,
                quantity=request.quantity,
                price=request.price,
                order_type=request.order_type.value)
    
    try:
        # Validate order request
        validate_order_request(request)
        
        # Prepare order data for SSI API
        order_data = {
            "instrumentID": request.instrument_id,
            "market": request.market.value,
            "buySell": request.buy_sell.value,
            "orderType": request.order_type.value,
            "price": request.price,
            "quantity": request.quantity,
            "account": request.account,
            "requestID": request.request_id,
            "stopOrder": request.stop_order,
            "stopPrice": request.stop_price,
            "stopType": request.stop_type,
            "stopStep": request.stop_step,
            "lossStep": request.loss_step,
            "profitStep": request.profit_step,
            "deviceID": request.device_id or "",
            "userAgent": request.user_agent or ""
        }
        
        # Submit order to SSI
        result = await client.place_order(order_data)
        
        # Log successful order
        logger.info("Order placed successfully",
                   instrument=request.instrument_id,
                   request_id=request.request_id,
                   order_id=result.get("data", {}).get("orderID"))
        
        # Background task for order tracking
        background_tasks.add_task(
            track_order_status, 
            request.request_id, 
            result.get("data", {}).get("orderID")
        )
        
        return OrderResponse(
            success=True,
            message="Order placed successfully",
            data=result.get("data", {}),
            order_id=result.get("data", {}).get("orderID"),
            request_id=request.request_id,
            timestamp=datetime.now()
        )
        
    except TradingSessionError as e:
        logger.warning("Trading session validation failed", error=str(e))
        raise HTTPException(status_code=400, detail={
            "error": "TRADING_SESSION_ERROR",
            "message": str(e),
            "session_info": get_trading_session_info(request.market)
        })
    
    except ValidationError as e:
        logger.warning("Order validation failed", error=str(e), field=e.field)
        raise HTTPException(status_code=422, detail={
            "error": "VALIDATION_ERROR",
            "message": str(e),
            "field": e.field
        })
    
    except SSIAPIError as e:
        logger.error("SSI API error", error=str(e))
        raise HTTPException(status_code=502, detail={
            "error": "SSI_API_ERROR",
            "message": "Failed to submit order to exchange",
            "details": str(e)
        })
    
    except Exception as e:
        logger.error("Unexpected error placing order", error=str(e))
        raise HTTPException(status_code=500, detail={
            "error": "INTERNAL_ERROR",
            "message": "An unexpected error occurred while placing the order"
        })


@router.post("/modify-order", response_model=OrderResponse)
async def modify_order(
    request: ModifyOrderRequest,
    client: SSIFastConnectClient = Depends(get_trading_client)
):
    """
    Modify an existing order
    
    Validates modification against current trading session rules
    and submits to SSI FastConnect API.
    """
    
    logger.info("Processing order modification", 
                order_id=request.order_id,
                new_price=request.price,
                new_quantity=request.quantity)
    
    try:
        # Validate modification is allowed in current session
        is_valid, message = validate_trading_request(
            market=request.market,
            order_type=request.order_type,
            action="modify"
        )
        
        if not is_valid:
            raise TradingSessionError(message)
        
        # Prepare modification data
        order_data = {
            "orderID": request.order_id,
            "instrumentID": request.instrument_id,
            "market": request.market.value,
            "buySell": request.buy_sell.value,
            "orderType": request.order_type.value,
            "price": request.price,
            "quantity": request.quantity,
            "account": request.account,
            "deviceID": request.device_id or "",
            "userAgent": request.user_agent or ""
        }
        
        # Submit modification to SSI
        result = await client.modify_order(order_data)
        
        logger.info("Order modified successfully", order_id=request.order_id)
        
        return OrderResponse(
            success=True,
            message="Order modified successfully",
            data=result.get("data", {}),
            order_id=request.order_id,
            timestamp=datetime.now()
        )
        
    except TradingSessionError as e:
        logger.warning("Order modification not allowed", error=str(e))
        raise HTTPException(status_code=400, detail={
            "error": "TRADING_SESSION_ERROR",
            "message": str(e),
            "session_info": get_trading_session_info(request.market)
        })
    
    except SSIAPIError as e:
        logger.error("SSI API error modifying order", error=str(e))
        raise HTTPException(status_code=502, detail={
            "error": "SSI_API_ERROR",
            "message": "Failed to modify order",
            "details": str(e)
        })
    
    except Exception as e:
        logger.error("Unexpected error modifying order", error=str(e))
        raise HTTPException(status_code=500, detail={
            "error": "INTERNAL_ERROR",
            "message": "An unexpected error occurred while modifying the order"
        })


@router.post("/cancel-order", response_model=OrderResponse)
async def cancel_order(
    request: CancelOrderRequest,
    client: SSIFastConnectClient = Depends(get_trading_client)
):
    """
    Cancel an existing order
    
    Validates cancellation against current trading session rules
    and submits to SSI FastConnect API.
    """
    
    logger.info("Processing order cancellation", order_id=request.order_id)
    
    try:
        # Validate cancellation is allowed in current session  
        is_valid, message = validate_trading_request(
            market=request.market,
            order_type=None,  # Not needed for cancellation
            action="cancel"
        )
        
        if not is_valid:
            raise TradingSessionError(message)
        
        # Prepare cancellation data
        order_data = {
            "orderID": request.order_id,
            "instrumentID": request.instrument_id,
            "market": request.market.value,
            "buySell": request.buy_sell.value,
            "account": request.account,
            "deviceID": request.device_id or "",
            "userAgent": request.user_agent or ""
        }
        
        # Submit cancellation to SSI
        result = await client.cancel_order(order_data)
        
        logger.info("Order cancelled successfully", order_id=request.order_id)
        
        return OrderResponse(
            success=True,
            message="Order cancelled successfully",
            data=result.get("data", {}),
            order_id=request.order_id,
            timestamp=datetime.now()
        )
        
    except TradingSessionError as e:
        logger.warning("Order cancellation not allowed", error=str(e))
        raise HTTPException(status_code=400, detail={
            "error": "TRADING_SESSION_ERROR",
            "message": str(e)
        })
    
    except SSIAPIError as e:
        logger.error("SSI API error cancelling order", error=str(e))
        raise HTTPException(status_code=502, detail={
            "error": "SSI_API_ERROR",
            "message": "Failed to cancel order",
            "details": str(e)
        })
    
    except Exception as e:
        logger.error("Unexpected error cancelling order", error=str(e))
        raise HTTPException(status_code=500, detail={
            "error": "INTERNAL_ERROR",
            "message": "An unexpected error occurred while cancelling the order"
        })


@router.get("/order-history", response_model=OrderBookResponse)
async def get_order_history(
    request: OrderHistoryRequest,
    client: SSIFastConnectClient = Depends(get_trading_client)
):
    """
    Get order history for specified date range
    """
    
    logger.info("Retrieving order history", 
                account=request.account,
                start_date=request.start_date,
                end_date=request.end_date)
    
    try:
        result = await client.get_order_history(
            request.account,
            request.start_date,
            request.end_date
        )
        
        return OrderBookResponse(
            success=True,
            message="Order history retrieved successfully",
            account=request.account,
            orders=result.get("data", []),
            timestamp=datetime.now()
        )
        
    except SSIAPIError as e:
        logger.error("SSI API error retrieving order history", error=str(e))
        raise HTTPException(status_code=502, detail={
            "error": "SSI_API_ERROR",
            "message": "Failed to retrieve order history",
            "details": str(e)
        })
    
    except Exception as e:
        logger.error("Unexpected error retrieving order history", error=str(e))
        raise HTTPException(status_code=500, detail={
            "error": "INTERNAL_ERROR",
            "message": "An unexpected error occurred while retrieving order history"
        })


@router.get("/trading-session-info", response_model=APIResponse)
async def get_trading_session_info(market: str):
    """
    Get current trading session information for specified market
    """
    
    try:
        # Convert market string to enum
        from ..models import MarketEnum
        market_enum = MarketEnum(market.upper())
        
        session_info = get_trading_session_info(market_enum)
        
        return APIResponse(
            success=True,
            message="Trading session info retrieved successfully",
            data=session_info,
            timestamp=datetime.now()
        )
        
    except ValueError:
        raise HTTPException(status_code=400, detail={
            "error": "INVALID_MARKET",
            "message": f"Invalid market: {market}. Valid markets: VN, HN, UP, VNFE"
        })
    
    except Exception as e:
        logger.error("Error retrieving trading session info", error=str(e))
        raise HTTPException(status_code=500, detail={
            "error": "INTERNAL_ERROR",
            "message": "An unexpected error occurred"
        })


async def track_order_status(request_id: str, order_id: str):
    """
    Background task to track order status updates
    This could publish to Kafka for other services to consume
    """
    
    logger.info("Starting order status tracking", 
                request_id=request_id,
                order_id=order_id)
    
    # In a real implementation, this would:
    # 1. Subscribe to order status updates from SSI
    # 2. Update local database
    # 3. Publish updates to Kafka topics
    # 4. Send notifications if needed
    
    # For now, just log the tracking initiation
    logger.info("Order tracking initiated", 
                request_id=request_id,
                order_id=order_id)
