"""
Order Management Service API Routes - Accounts endpoint.
"""

from typing import Dict, List, Optional
from decimal import Decimal
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

try:
    from ..database import get_db
    from ..services.portfolio_service import PortfolioService
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
    logger = LoggerManager.get_logger("account_routes")
except:
    security_manager = None
    logger = None

# Router
router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
    responses={404: {"description": "Not found"}}
)


@router.get("/profile")
async def get_account_profile(
    db: Session = Depends(get_db),
    token: str = Depends(security)
):
    """Get account profile information."""
    
    try:
        # Extract account_id from token
        if security_manager:
            user_info = security_manager.decode_token(token.credentials)
            account_id = user_info.get("account_id")
            user_id = user_info.get("user_id")
            if not account_id:
                raise HTTPException(status_code=401, detail="Invalid token: missing account_id")
        else:
            # Fallback for development
            account_id = "DEV_ACCOUNT_001"
            user_id = "DEV_USER_001"
        
        # Get account information (simplified)
        account_profile = {
            "account_id": account_id,
            "user_id": user_id,
            "account_type": "TRADING",
            "account_status": "ACTIVE",
            "account_name": f"Trading Account {account_id}",
            "created_date": "2024-01-01T00:00:00Z",
            "last_login": datetime.utcnow().isoformat(),
            "permissions": [
                "TRADE_STOCKS",
                "VIEW_PORTFOLIO",
                "VIEW_ORDERS",
                "MODIFY_ORDERS",
                "CANCEL_ORDERS"
            ],
            "trading_limits": {
                "daily_trading_limit": Decimal("10000000"),  # 10M VND
                "single_order_limit": Decimal("1000000"),    # 1M VND
                "max_positions": 50
            }
        }
        
        if logger:
            logger.info(f"Retrieved account profile for {account_id}")
        
        return account_profile
        
    except HTTPException:
        raise
    except Exception as e:
        if logger:
            logger.error(f"Error getting account profile: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/balance")
async def get_account_balance(
    db: Session = Depends(get_db),
    token: str = Depends(security)
):
    """Get account balance and cash information."""
    
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
        
        # Get portfolio summary and buying power
        portfolio_summary = await portfolio_service.get_portfolio_summary(account_id)
        buying_power = await portfolio_service.calculate_buying_power(account_id)
        
        balance_info = {
            "account_id": account_id,
            "cash_balance": buying_power["cash_balance"],
            "buying_power": buying_power["buying_power"],
            "total_portfolio_value": portfolio_summary.total_portfolio_value,
            "market_value": portfolio_summary.total_market_value,
            "unrealized_pnl": portfolio_summary.unrealized_pnl,
            "daily_pnl": portfolio_summary.daily_pnl,
            "margin_used": buying_power.get("margin_used", Decimal('0')),
            "margin_available": buying_power.get("margin_available", Decimal('0')),
            "last_updated": portfolio_summary.last_updated
        }
        
        if logger:
            logger.info(f"Retrieved account balance for {account_id}")
        
        return balance_info
        
    except HTTPException:
        raise
    except Exception as e:
        if logger:
            logger.error(f"Error getting account balance: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/trading-limits")
async def get_trading_limits(
    db: Session = Depends(get_db),
    token: str = Depends(security)
):
    """Get trading limits and restrictions for the account."""
    
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
        
        # Get current usage (simplified)
        # In production, this should track actual daily usage
        
        trading_limits = {
            "account_id": account_id,
            "daily_limits": {
                "max_daily_volume": Decimal("10000000"),  # 10M VND
                "used_daily_volume": Decimal("2500000"),   # 2.5M VND
                "remaining_daily_volume": Decimal("7500000"),  # 7.5M VND
                "max_daily_orders": 100,
                "used_daily_orders": 15,
                "remaining_daily_orders": 85
            },
            "order_limits": {
                "max_single_order_value": Decimal("1000000"),  # 1M VND
                "max_order_quantity": 10000,
                "min_order_value": Decimal("10000")  # 10K VND
            },
            "position_limits": {
                "max_positions": 50,
                "current_positions": 8,
                "max_concentration_per_stock": Decimal("20.0"),  # 20%
                "max_sector_concentration": Decimal("30.0")       # 30%
            },
            "restrictions": {
                "day_trading_enabled": True,
                "margin_trading_enabled": False,
                "options_trading_enabled": False,
                "foreign_stock_trading_enabled": False
            },
            "reset_time": "00:00:00 ICT",
            "last_updated": datetime.utcnow().isoformat()
        }
        
        if logger:
            logger.info(f"Retrieved trading limits for {account_id}")
        
        return trading_limits
        
    except HTTPException:
        raise
    except Exception as e:
        if logger:
            logger.error(f"Error getting trading limits: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/trading-session")
async def get_current_trading_session(
    token: str = Depends(security)
):
    """Get current trading session information."""
    
    try:
        # Extract account_id from token (for logging purposes)
        if security_manager:
            user_info = security_manager.decode_token(token.credentials)
            account_id = user_info.get("account_id")
        else:
            account_id = "DEV_ACCOUNT_001"
        
        # Initialize service
        trading_session_service = TradingSessionService()
        
        # Get current session
        session_info = await trading_session_service.get_current_session()
        
        # Get next session info
        next_session_info = await trading_session_service.get_next_trading_session()
        
        result = {
            **session_info,
            "next_session_info": next_session_info
        }
        
        if logger:
            logger.info(f"Retrieved trading session info for account {account_id}")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        if logger:
            logger.error(f"Error getting trading session: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/market-schedule")
async def get_market_schedule(
    date: Optional[str] = Query(None, description="Date in YYYY-MM-DD format (defaults to today)"),
    token: str = Depends(security)
):
    """Get market schedule for a specific date."""
    
    try:
        # Extract account_id from token (for logging purposes)
        if security_manager:
            user_info = security_manager.decode_token(token.credentials)
            account_id = user_info.get("account_id")
        else:
            account_id = "DEV_ACCOUNT_001"
        
        # Parse date
        target_date = None
        if date:
            try:
                target_date = datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
        
        # Initialize service
        trading_session_service = TradingSessionService()
        
        # Get market schedule
        schedule = await trading_session_service.get_market_schedule(target_date)
        
        if logger:
            logger.info(f"Retrieved market schedule for {date or 'today'} for account {account_id}")
        
        return schedule
        
    except HTTPException:
        raise
    except Exception as e:
        if logger:
            logger.error(f"Error getting market schedule: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/permissions")
async def get_account_permissions(
    db: Session = Depends(get_db),
    token: str = Depends(security)
):
    """Get account permissions and capabilities."""
    
    try:
        # Extract account_id from token
        if security_manager:
            user_info = security_manager.decode_token(token.credentials)
            account_id = user_info.get("account_id")
            user_role = user_info.get("role", "USER")
            if not account_id:
                raise HTTPException(status_code=401, detail="Invalid token: missing account_id")
        else:
            # Fallback for development
            account_id = "DEV_ACCOUNT_001"
            user_role = "USER"
        
        # Define permissions based on role and account status
        base_permissions = {
            "trading": {
                "can_place_orders": True,
                "can_modify_orders": True,
                "can_cancel_orders": True,
                "can_view_orders": True,
                "can_view_executions": True
            },
            "portfolio": {
                "can_view_positions": True,
                "can_view_portfolio_summary": True,
                "can_view_position_history": True,
                "can_view_performance": True
            },
            "account": {
                "can_view_profile": True,
                "can_view_balance": True,
                "can_view_trading_limits": True,
                "can_modify_profile": False
            },
            "market_data": {
                "can_view_real_time_prices": True,
                "can_view_level2_data": False,
                "can_view_historical_data": True
            },
            "advanced": {
                "can_use_margin": False,
                "can_trade_options": False,
                "can_trade_foreign_stocks": False,
                "can_use_algorithms": False
            }
        }
        
        # Admin users get additional permissions
        if user_role == "ADMIN":
            base_permissions["account"]["can_modify_profile"] = True
            base_permissions["advanced"]["can_use_algorithms"] = True
        
        permissions_info = {
            "account_id": account_id,
            "user_role": user_role,
            "permissions": base_permissions,
            "restrictions": [
                "Day trading only during market hours",
                "Maximum 50 positions",
                "No short selling",
                "No margin trading"
            ],
            "last_updated": datetime.utcnow().isoformat()
        }
        
        if logger:
            logger.info(f"Retrieved permissions for account {account_id}")
        
        return permissions_info
        
    except HTTPException:
        raise
    except Exception as e:
        if logger:
            logger.error(f"Error getting account permissions: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/activity-summary")
async def get_account_activity_summary(
    db: Session = Depends(get_db),
    token: str = Depends(security),
    days: int = Query(30, ge=1, le=365, description="Number of days to look back")
):
    """Get account activity summary for the specified period."""
    
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
        
        # Calculate period
        from_date = datetime.utcnow() - timedelta(days=days)
        
        # Get activity summary (simplified)
        # In production, this should aggregate actual data from orders and executions
        
        activity_summary = {
            "account_id": account_id,
            "period": {
                "from_date": from_date.isoformat(),
                "to_date": datetime.utcnow().isoformat(),
                "days": days
            },
            "trading_activity": {
                "total_orders": 45,
                "filled_orders": 38,
                "cancelled_orders": 7,
                "pending_orders": 2,
                "total_volume": Decimal("15750000"),  # 15.75M VND
                "buy_volume": Decimal("8250000"),     # 8.25M VND
                "sell_volume": Decimal("7500000"),    # 7.5M VND
                "average_order_size": Decimal("350000")  # 350K VND
            },
            "portfolio_activity": {
                "positions_opened": 12,
                "positions_closed": 8,
                "net_position_change": 4,
                "realized_pnl": Decimal("125000"),    # 125K VND profit
                "largest_gain": Decimal("85000"),     # 85K VND
                "largest_loss": Decimal("-35000")     # 35K VND loss
            },
            "market_participation": {
                "most_traded_symbol": "VIC",
                "most_traded_volume": Decimal("2500000"),
                "unique_symbols_traded": 15,
                "average_daily_trades": 1.5
            },
            "risk_metrics": {
                "max_daily_loss": Decimal("-125000"),
                "max_daily_gain": Decimal("275000"),
                "win_rate": Decimal("65.8"),  # 65.8%
                "sharpe_ratio": Decimal("1.25")
            }
        }
        
        if logger:
            logger.info(f"Retrieved activity summary for account {account_id}, period {days} days")
        
        return activity_summary
        
    except HTTPException:
        raise
    except Exception as e:
        if logger:
            logger.error(f"Error getting activity summary: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
