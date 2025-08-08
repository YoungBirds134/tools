"""
Accounts API Router
Account management endpoints for balance, portfolio, and trading capabilities.
"""

from fastapi import APIRouter, HTTPException, Depends
import structlog
from datetime import datetime

from ..models import (
    AccountBalanceRequest,
    PositionRequest,
    MaxQuantityRequest,
    BalanceResponse,
    PositionResponse,
    MaxQuantityResponse,
    APIResponse
)
from ..services.ssi_client import get_ssi_client, SSIFastConnectClient
from ..utils.exceptions import SSIAPIError

logger = structlog.get_logger(__name__)
router = APIRouter()


async def get_trading_client() -> SSIFastConnectClient:
    """Dependency to get SSI trading client"""
    return await get_ssi_client()


@router.get("/balance/{account}", response_model=BalanceResponse)
async def get_account_balance(
    account: str,
    client: SSIFastConnectClient = Depends(get_trading_client)
):
    """
    Get account balance information
    
    Returns available cash balance for trading.
    """
    
    logger.info("Retrieving account balance", account=account)
    
    try:
        result = await client.get_account_balance(account)
        
        balance_data = result.get("data", {})
        balance = balance_data.get("balance", 0.0)
        
        return BalanceResponse(
            success=True,
            message="Balance retrieved successfully",
            account=account,
            balance=balance,
            currency="VND",
            data=balance_data,
            timestamp=datetime.now()
        )
        
    except SSIAPIError as e:
        logger.error("SSI API error retrieving balance", account=account, error=str(e))
        raise HTTPException(status_code=502, detail={
            "error": "SSI_API_ERROR",
            "message": "Failed to retrieve account balance",
            "details": str(e)
        })
    
    except Exception as e:
        logger.error("Unexpected error retrieving balance", account=account, error=str(e))
        raise HTTPException(status_code=500, detail={
            "error": "INTERNAL_ERROR",
            "message": "An unexpected error occurred while retrieving balance"
        })


@router.get("/portfolio/{account}", response_model=PositionResponse)
async def get_portfolio(
    account: str,
    query_summary: bool = True,
    client: SSIFastConnectClient = Depends(get_trading_client)
):
    """
    Get portfolio positions for account
    
    Returns detailed position information including holdings and P&L.
    """
    
    logger.info("Retrieving portfolio", account=account)
    
    try:
        result = await client.get_portfolio(account)
        
        positions_data = result.get("data", [])
        
        return PositionResponse(
            success=True,
            message="Portfolio retrieved successfully",
            account=account,
            positions=positions_data,
            data=result,
            timestamp=datetime.now()
        )
        
    except SSIAPIError as e:
        logger.error("SSI API error retrieving portfolio", account=account, error=str(e))
        raise HTTPException(status_code=502, detail={
            "error": "SSI_API_ERROR",
            "message": "Failed to retrieve portfolio",
            "details": str(e)
        })
    
    except Exception as e:
        logger.error("Unexpected error retrieving portfolio", account=account, error=str(e))
        raise HTTPException(status_code=500, detail={
            "error": "INTERNAL_ERROR",
            "message": "An unexpected error occurred while retrieving portfolio"
        })


@router.get("/max-quantity", response_model=MaxQuantityResponse)
async def get_max_quantity(
    account: str,
    instrument_id: str,
    price: float = 0,
    client: SSIFastConnectClient = Depends(get_trading_client)
):
    """
    Get maximum tradeable quantity for specified instrument
    
    Calculates maximum buy/sell quantities based on:
    - Available balance (for buy orders)
    - Current holdings (for sell orders)
    - Market rules and position limits
    """
    
    logger.info("Calculating max quantities", 
                account=account,
                instrument=instrument_id,
                price=price)
    
    try:
        result = await client.get_max_quantity(account, instrument_id, price)
        
        data = result.get("data", {})
        max_buy = data.get("maxBuyQuantity", 0)
        max_sell = data.get("maxSellQuantity", 0)
        
        return MaxQuantityResponse(
            success=True,
            message="Max quantities calculated successfully",
            account=account,
            instrument_id=instrument_id,
            max_buy_quantity=max_buy,
            max_sell_quantity=max_sell,
            data=data,
            timestamp=datetime.now()
        )
        
    except SSIAPIError as e:
        logger.error("SSI API error calculating max quantities", 
                    account=account, 
                    instrument=instrument_id,
                    error=str(e))
        raise HTTPException(status_code=502, detail={
            "error": "SSI_API_ERROR",
            "message": "Failed to calculate maximum quantities",
            "details": str(e)
        })
    
    except Exception as e:
        logger.error("Unexpected error calculating max quantities", 
                    account=account,
                    instrument=instrument_id,
                    error=str(e))
        raise HTTPException(status_code=500, detail={
            "error": "INTERNAL_ERROR",
            "message": "An unexpected error occurred while calculating maximum quantities"
        })


@router.get("/account-info/{account}", response_model=APIResponse)
async def get_account_info(
    account: str,
    client: SSIFastConnectClient = Depends(get_trading_client)
):
    """
    Get comprehensive account information
    
    Returns account details, status, and trading permissions.
    """
    
    logger.info("Retrieving account info", account=account)
    
    try:
        # In a real implementation, this would call SSI API for account details
        # For now, return basic account info structure
        
        account_info = {
            "account_id": account,
            "account_type": "VNDS",  # Vietnam Dong Securities
            "status": "ACTIVE",
            "trading_permissions": {
                "stocks": True,
                "derivatives": False,  # Would be determined by actual account
                "margin_trading": False,
                "short_selling": False
            },
            "risk_limits": {
                "daily_loss_limit": 0,
                "position_limit": 0,
                "leverage_limit": 1.0
            }
        }
        
        return APIResponse(
            success=True,
            message="Account info retrieved successfully",
            data=account_info,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error("Error retrieving account info", account=account, error=str(e))
        raise HTTPException(status_code=500, detail={
            "error": "INTERNAL_ERROR",
            "message": "An unexpected error occurred while retrieving account information"
        })
        handle_fc_trading_error(e, "Get stock balance")


