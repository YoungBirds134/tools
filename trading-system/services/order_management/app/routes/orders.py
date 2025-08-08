"""
Order Management Service API Routes - Orders endpoint.
"""

from typing import List, Optional
from decimal import Decimal
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

try:
    from ..database import get_db
    from ..models import (
        NewOrderRequest as OrderCreateRequest, 
        ModifyOrderRequest as OrderModifyRequest, 
        OrderResponse,
        OrderStatus, OrderSide, OrderType, Market
    )
    from ..services.order_service import OrderService
    from ..services.trading_session_service import TradingSessionService
    from ....common.logging import LoggerManager
    from ....common.security import SecurityManager
except ImportError:
    # Fallback for development environment
    pass

# Initialize security
security = HTTPBearer()
try:
    security_manager = SecurityManager()
    logger = LoggerManager.get_logger("order_routes")
except:
    security_manager = None
    logger = None

# Router
router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    responses={404: {"description": "Not found"}}
)


@router.post("/", response_model=OrderResponse)
async def create_order(
    order_request: OrderCreateRequest,
    db: Session = Depends(get_db),
    token: str = Depends(security)
):
    """Create a new order."""
    
    try:
        # Extract account_id from token
        if security_manager:
            user_info = security_manager.decode_token(token.credentials)
            account_id = user_info.get("account_id")
            if not account_id:
                raise HTTPException(status_code=401, detail="Invalid token: missing account_id")
        else:
            # Fallback for development
            account_id = "DEV_ACCOUNT_001"
        
        # Initialize services
        order_service = OrderService(db)
        
        # Validate trading session
        trading_session_service = TradingSessionService()
        trading_allowed = await trading_session_service.is_trading_allowed(
            market=order_request.market,
            order_type=order_request.order_type.value,
            action="place"
        )
        
        if not trading_allowed["allowed"]:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Trading not allowed",
                    "reason": trading_allowed["reason"],
                    "session": trading_allowed["session"],
                    "market": trading_allowed["market"]
                }
            )
        
        # Create order
        order = await order_service.create_order(
            account_id=account_id,
            symbol=order_request.symbol,
            side=order_request.side,
            order_type=order_request.order_type,
            quantity=order_request.quantity,
            price=order_request.price,
            market=order_request.market,
            time_in_force=order_request.time_in_force,
            order_conditions=order_request.order_conditions
        )
        
        if logger:
            logger.info(f"Order created: {order.id} for account {account_id}")
        
        return order
        
    except HTTPException:
        raise
    except Exception as e:
        if logger:
            logger.error(f"Error creating order: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/", response_model=List[OrderResponse])
async def get_orders(
    db: Session = Depends(get_db),
    token: str = Depends(security),
    status: Optional[OrderStatus] = Query(None, description="Filter by order status"),
    symbol: Optional[str] = Query(None, description="Filter by symbol"),
    side: Optional[OrderSide] = Query(None, description="Filter by order side"),
    order_type: Optional[OrderType] = Query(None, description="Filter by order type"),
    market: Optional[Market] = Query(None, description="Filter by market"),
    from_date: Optional[datetime] = Query(None, description="Filter orders from this date"),
    to_date: Optional[datetime] = Query(None, description="Filter orders to this date"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of orders to return"),
    offset: int = Query(0, ge=0, description="Number of orders to skip")
):
    """Get orders for the authenticated account."""
    
    try:
        # Extract account_id from token
        if security_manager:
            user_info = security_manager.decode_token(token.credentials)
            account_id = user_info.get("account_id")
            if not account_id:
                raise HTTPException(status_code=401, detail="Invalid token: missing account_id")
        else:
            # Fallback for development
            account_id = "DEV_ACCOUNT_001"
        
        # Initialize service
        order_service = OrderService(db)
        
        # Build filters
        filters = {}
        if status:
            filters["status"] = status
        if symbol:
            filters["symbol"] = symbol
        if side:
            filters["side"] = side
        if order_type:
            filters["order_type"] = order_type
        if market:
            filters["market"] = market
        if from_date:
            filters["from_date"] = from_date
        if to_date:
            filters["to_date"] = to_date
        
        # Get orders
        orders = await order_service.get_orders(
            account_id=account_id,
            filters=filters,
            limit=limit,
            offset=offset
        )
        
        if logger:
            logger.info(f"Retrieved {len(orders)} orders for account {account_id}")
        
        return orders
        
    except HTTPException:
        raise
    except Exception as e:
        if logger:
            logger.error(f"Error getting orders: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: str = Path(..., description="Order ID"),
    db: Session = Depends(get_db),
    token: str = Depends(security)
):
    """Get a specific order by ID."""
    
    try:
        # Extract account_id from token
        if security_manager:
            user_info = security_manager.decode_token(token.credentials)
            account_id = user_info.get("account_id")
            if not account_id:
                raise HTTPException(status_code=401, detail="Invalid token: missing account_id")
        else:
            # Fallback for development
            account_id = "DEV_ACCOUNT_001"
        
        # Initialize service
        order_service = OrderService(db)
        
        # Get order
        order = await order_service.get_order(order_id, account_id)
        
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        if logger:
            logger.info(f"Retrieved order {order_id} for account {account_id}")
        
        return order
        
    except HTTPException:
        raise
    except Exception as e:
        if logger:
            logger.error(f"Error getting order {order_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.put("/{order_id}", response_model=OrderResponse)
async def modify_order(
    order_id: str = Path(..., description="Order ID"),
    modify_request: OrderModifyRequest = ...,
    db: Session = Depends(get_db),
    token: str = Depends(security)
):
    """Modify an existing order."""
    
    try:
        # Extract account_id from token
        if security_manager:
            user_info = security_manager.decode_token(token.credentials)
            account_id = user_info.get("account_id")
            if not account_id:
                raise HTTPException(status_code=401, detail="Invalid token: missing account_id")
        else:
            # Fallback for development
            account_id = "DEV_ACCOUNT_001"
        
        # Initialize services
        order_service = OrderService(db)
        
        # Get existing order to check market
        existing_order = await order_service.get_order(order_id, account_id)
        if not existing_order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        # Validate trading session
        trading_session_service = TradingSessionService()
        trading_allowed = await trading_session_service.is_trading_allowed(
            market=existing_order.market,
            order_type=existing_order.order_type.value,
            action="modify"
        )
        
        if not trading_allowed["allowed"]:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Order modification not allowed",
                    "reason": trading_allowed["reason"],
                    "session": trading_allowed["session"],
                    "market": trading_allowed["market"]
                }
            )
        
        # Modify order
        modified_order = await order_service.modify_order(
            order_id=order_id,
            account_id=account_id,
            new_quantity=modify_request.quantity,
            new_price=modify_request.price
        )
        
        if logger:
            logger.info(f"Order modified: {order_id} for account {account_id}")
        
        return modified_order
        
    except HTTPException:
        raise
    except Exception as e:
        if logger:
            logger.error(f"Error modifying order {order_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.delete("/{order_id}")
async def cancel_order(
    order_id: str = Path(..., description="Order ID"),
    db: Session = Depends(get_db),
    token: str = Depends(security)
):
    """Cancel an existing order."""
    
    try:
        # Extract account_id from token
        if security_manager:
            user_info = security_manager.decode_token(token.credentials)
            account_id = user_info.get("account_id")
            if not account_id:
                raise HTTPException(status_code=401, detail="Invalid token: missing account_id")
        else:
            # Fallback for development
            account_id = "DEV_ACCOUNT_001"
        
        # Initialize services
        order_service = OrderService(db)
        
        # Get existing order to check market
        existing_order = await order_service.get_order(order_id, account_id)
        if not existing_order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        # Validate trading session
        trading_session_service = TradingSessionService()
        trading_allowed = await trading_session_service.is_trading_allowed(
            market=existing_order.market,
            order_type=existing_order.order_type.value,
            action="cancel"
        )
        
        if not trading_allowed["allowed"]:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Order cancellation not allowed",
                    "reason": trading_allowed["reason"],
                    "session": trading_allowed["session"],
                    "market": trading_allowed["market"]
                }
            )
        
        # Cancel order
        success = await order_service.cancel_order(order_id, account_id)
        
        if not success:
            raise HTTPException(status_code=400, detail="Order could not be cancelled")
        
        if logger:
            logger.info(f"Order cancelled: {order_id} for account {account_id}")
        
        return {"message": "Order cancelled successfully", "order_id": order_id}
        
    except HTTPException:
        raise
    except Exception as e:
        if logger:
            logger.error(f"Error cancelling order {order_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/{order_id}/executions")
async def get_order_executions(
    order_id: str = Path(..., description="Order ID"),
    db: Session = Depends(get_db),
    token: str = Depends(security)
):
    """Get executions for a specific order."""
    
    try:
        # Extract account_id from token
        if security_manager:
            user_info = security_manager.decode_token(token.credentials)
            account_id = user_info.get("account_id")
            if not account_id:
                raise HTTPException(status_code=401, detail="Invalid token: missing account_id")
        else:
            # Fallback for development
            account_id = "DEV_ACCOUNT_001"
        
        # Initialize service
        order_service = OrderService(db)
        
        # Verify order belongs to account
        order = await order_service.get_order(order_id, account_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        # Get executions
        executions = await order_service.get_order_executions(order_id)
        
        if logger:
            logger.info(f"Retrieved {len(executions)} executions for order {order_id}")
        
        return executions
        
    except HTTPException:
        raise
    except Exception as e:
        if logger:
            logger.error(f"Error getting executions for order {order_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/{order_id}/simulate")
async def simulate_order_execution(
    order_id: str = Path(..., description="Order ID"),
    execution_price: Decimal = Query(..., description="Simulated execution price"),
    execution_quantity: Optional[Decimal] = Query(None, description="Simulated execution quantity (defaults to remaining quantity)"),
    db: Session = Depends(get_db),
    token: str = Depends(security)
):
    """Simulate order execution (for testing purposes)."""
    
    try:
        # Extract account_id from token
        if security_manager:
            user_info = security_manager.decode_token(token.credentials)
            account_id = user_info.get("account_id")
            if not account_id:
                raise HTTPException(status_code=401, detail="Invalid token: missing account_id")
        else:
            # Fallback for development
            account_id = "DEV_ACCOUNT_001"
        
        # Initialize service
        order_service = OrderService(db)
        
        # Verify order belongs to account
        order = await order_service.get_order(order_id, account_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        # Simulate execution
        success = await order_service.simulate_execution(
            order_id=order_id,
            execution_price=execution_price,
            execution_quantity=execution_quantity
        )
        
        if not success:
            raise HTTPException(status_code=400, detail="Order execution simulation failed")
        
        if logger:
            logger.info(f"Simulated execution for order {order_id}: price={execution_price}, quantity={execution_quantity}")
        
        return {
            "message": "Order execution simulated successfully",
            "order_id": order_id,
            "execution_price": execution_price,
            "execution_quantity": execution_quantity
        }
        
    except HTTPException:
        raise
    except Exception as e:
        if logger:
            logger.error(f"Error simulating execution for order {order_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/statistics/summary")
async def get_order_statistics(
    db: Session = Depends(get_db),
    token: str = Depends(security),
    from_date: Optional[datetime] = Query(None, description="Statistics from this date"),
    to_date: Optional[datetime] = Query(None, description="Statistics to this date")
):
    """Get order statistics summary."""
    
    try:
        # Extract account_id from token
        if security_manager:
            user_info = security_manager.decode_token(token.credentials)
            account_id = user_info.get("account_id")
            if not account_id:
                raise HTTPException(status_code=401, detail="Invalid token: missing account_id")
        else:
            # Fallback for development
            account_id = "DEV_ACCOUNT_001"
        
        # Initialize service
        order_service = OrderService(db)
        
        # Get statistics
        stats = await order_service.get_order_statistics(
            account_id=account_id,
            from_date=from_date,
            to_date=to_date
        )
        
        if logger:
            logger.info(f"Retrieved order statistics for account {account_id}")
        
        return stats
        
    except HTTPException:
        raise
    except Exception as e:
        if logger:
            logger.error(f"Error getting order statistics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
