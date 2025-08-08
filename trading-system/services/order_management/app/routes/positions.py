"""
Order Management Service API Routes - Positions endpoint.
"""

from typing import List, Optional
from decimal import Decimal
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

try:
    from ..database import get_db
    from ..models import PositionResponse
    from ..services.portfolio_service import PortfolioService
    from ....common.logging import LoggerManager
    from ....common.security import SecurityManager
except ImportError:
    # Fallback for development environment
    PositionResponse = None
    PortfolioService = None
    LoggerManager = None
    SecurityManager = None
    get_db = None

# Create fallback models for missing classes
if PositionResponse:
    PortfolioSummary = PositionResponse
    PositionHistory = PositionResponse
else:
    # Simple fallback classes
    from pydantic import BaseModel
    class PortfolioSummary(BaseModel):
        message: str = "Fallback model"
    class PositionHistory(BaseModel):
        message: str = "Fallback model"
    pass

# Initialize security
security = HTTPBearer()
try:
    security_manager = SecurityManager()
    logger = LoggerManager.get_logger("position_routes")
except:
    security_manager = None
    logger = None

# Router
router = APIRouter(
    prefix="/positions",
    tags=["positions"],
    responses={404: {"description": "Not found"}}
)


@router.get("/", response_model=List[PositionResponse])
async def get_positions(
    db: Session = Depends(get_db),
    token: str = Depends(security),
    symbol: Optional[str] = Query(None, description="Filter by symbol"),
    include_zero: bool = Query(False, description="Include positions with zero quantity")
):
    """Get current positions for the authenticated account."""
    
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
        portfolio_service = PortfolioService(db)
        
        # Get positions
        positions = await portfolio_service.get_positions(
            account_id=account_id,
            symbol=symbol,
            include_zero_positions=include_zero
        )
        
        if logger:
            logger.info(f"Retrieved {len(positions)} positions for account {account_id}")
        
        return positions
        
    except HTTPException:
        raise
    except Exception as e:
        if logger:
            logger.error(f"Error getting positions: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/{symbol}", response_model=PositionResponse)
async def get_position(
    symbol: str = Path(..., description="Stock symbol"),
    db: Session = Depends(get_db),
    token: str = Depends(security)
):
    """Get specific position for a symbol."""
    
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
        portfolio_service = PortfolioService(db)
        
        # Get position
        position = await portfolio_service.get_position(account_id, symbol.upper())
        
        if not position:
            raise HTTPException(status_code=404, detail=f"Position not found for symbol {symbol}")
        
        if logger:
            logger.info(f"Retrieved position for {symbol} in account {account_id}")
        
        return position
        
    except HTTPException:
        raise
    except Exception as e:
        if logger:
            logger.error(f"Error getting position for {symbol}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/summary/portfolio", response_model=PortfolioSummary)
async def get_portfolio_summary(
    db: Session = Depends(get_db),
    token: str = Depends(security)
):
    """Get portfolio summary with totals and performance metrics."""
    
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
        portfolio_service = PortfolioService(db)
        
        # Get portfolio summary
        summary = await portfolio_service.get_portfolio_summary(account_id)
        
        if logger:
            logger.info(f"Retrieved portfolio summary for account {account_id}")
        
        return summary
        
    except HTTPException:
        raise
    except Exception as e:
        if logger:
            logger.error(f"Error getting portfolio summary: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/history/changes", response_model=List[PositionHistory])
async def get_position_history(
    db: Session = Depends(get_db),
    token: str = Depends(security),
    symbol: Optional[str] = Query(None, description="Filter by symbol"),
    days: int = Query(30, ge=1, le=365, description="Number of days to look back")
):
    """Get position history for the last N days."""
    
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
        portfolio_service = PortfolioService(db)
        
        # Get position history
        history = await portfolio_service.get_position_history(
            account_id=account_id,
            symbol=symbol.upper() if symbol else None,
            days=days
        )
        
        if logger:
            logger.info(f"Retrieved {len(history)} position history records for account {account_id}")
        
        return history
        
    except HTTPException:
        raise
    except Exception as e:
        if logger:
            logger.error(f"Error getting position history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/buying-power/available")
async def get_buying_power(
    db: Session = Depends(get_db),
    token: str = Depends(security)
):
    """Get available buying power for the account."""
    
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
        portfolio_service = PortfolioService(db)
        
        # Calculate buying power
        buying_power = await portfolio_service.calculate_buying_power(account_id)
        
        if logger:
            logger.info(f"Retrieved buying power for account {account_id}")
        
        return buying_power
        
    except HTTPException:
        raise
    except Exception as e:
        if logger:
            logger.error(f"Error getting buying power: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/{symbol}/reserve")
async def reserve_position_quantity(
    symbol: str = Path(..., description="Stock symbol"),
    quantity: Decimal = Query(..., description="Quantity to reserve"),
    order_id: str = Query(..., description="Order ID for the reservation"),
    db: Session = Depends(get_db),
    token: str = Depends(security)
):
    """Reserve quantity for a sell order (for internal use)."""
    
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
        portfolio_service = PortfolioService(db)
        
        # Reserve quantity
        success = await portfolio_service.reserve_quantity(
            account_id=account_id,
            symbol=symbol.upper(),
            quantity=quantity,
            order_id=order_id
        )
        
        if not success:
            raise HTTPException(status_code=400, detail="Insufficient quantity available for reservation")
        
        if logger:
            logger.info(f"Reserved {quantity} of {symbol} for order {order_id}")
        
        return {
            "message": "Quantity reserved successfully",
            "symbol": symbol,
            "quantity": quantity,
            "order_id": order_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        if logger:
            logger.error(f"Error reserving quantity: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/{symbol}/release")
async def release_position_quantity(
    symbol: str = Path(..., description="Stock symbol"),
    quantity: Decimal = Query(..., description="Quantity to release"),
    order_id: str = Query(..., description="Order ID for the release"),
    db: Session = Depends(get_db),
    token: str = Depends(security)
):
    """Release reserved quantity (e.g., when order is cancelled)."""
    
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
        portfolio_service = PortfolioService(db)
        
        # Release quantity
        success = await portfolio_service.release_quantity(
            account_id=account_id,
            symbol=symbol.upper(),
            quantity=quantity,
            order_id=order_id
        )
        
        if not success:
            raise HTTPException(status_code=400, detail="Failed to release quantity")
        
        if logger:
            logger.info(f"Released {quantity} of {symbol} for order {order_id}")
        
        return {
            "message": "Quantity released successfully",
            "symbol": symbol,
            "quantity": quantity,
            "order_id": order_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        if logger:
            logger.error(f"Error releasing quantity: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/analytics/performance")
async def get_position_performance(
    db: Session = Depends(get_db),
    token: str = Depends(security),
    symbol: Optional[str] = Query(None, description="Filter by symbol"),
    period: str = Query("1M", description="Performance period (1D, 1W, 1M, 3M, 6M, 1Y)")
):
    """Get position performance analytics."""
    
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
        
        # Parse period
        period_days = {
            "1D": 1,
            "1W": 7,
            "1M": 30,
            "3M": 90,
            "6M": 180,
            "1Y": 365
        }
        
        days = period_days.get(period, 30)
        
        # Initialize service
        portfolio_service = PortfolioService(db)
        
        # Get positions for performance calculation
        positions = await portfolio_service.get_positions(
            account_id=account_id,
            symbol=symbol,
            include_zero_positions=False
        )
        
        # Calculate performance metrics (simplified)
        total_market_value = sum(pos.market_value for pos in positions)
        total_cost_basis = sum(pos.cost_basis for pos in positions)
        total_unrealized_pnl = sum(pos.unrealized_pnl for pos in positions)
        
        performance_percent = Decimal('0')
        if total_cost_basis > 0:
            performance_percent = (total_unrealized_pnl / total_cost_basis) * 100
        
        performance_data = {
            "account_id": account_id,
            "period": period,
            "symbol": symbol,
            "total_positions": len(positions),
            "total_market_value": total_market_value,
            "total_cost_basis": total_cost_basis,
            "total_unrealized_pnl": total_unrealized_pnl,
            "performance_percent": performance_percent,
            "best_performer": None,
            "worst_performer": None,
            "calculation_date": datetime.utcnow()
        }
        
        # Find best and worst performers
        if positions:
            best_pos = max(positions, key=lambda p: (p.unrealized_pnl / p.cost_basis) if p.cost_basis > 0 else 0)
            worst_pos = min(positions, key=lambda p: (p.unrealized_pnl / p.cost_basis) if p.cost_basis > 0 else 0)
            
            performance_data["best_performer"] = {
                "symbol": best_pos.symbol,
                "unrealized_pnl": best_pos.unrealized_pnl,
                "performance_percent": (best_pos.unrealized_pnl / best_pos.cost_basis * 100) if best_pos.cost_basis > 0 else 0
            }
            
            performance_data["worst_performer"] = {
                "symbol": worst_pos.symbol,
                "unrealized_pnl": worst_pos.unrealized_pnl,
                "performance_percent": (worst_pos.unrealized_pnl / worst_pos.cost_basis * 100) if worst_pos.cost_basis > 0 else 0
            }
        
        if logger:
            logger.info(f"Retrieved performance analytics for account {account_id}, period {period}")
        
        return performance_data
        
    except HTTPException:
        raise
    except Exception as e:
        if logger:
            logger.error(f"Error getting position performance: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
