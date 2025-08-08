"""
Trading validation utilities for Vietnamese stock exchanges
Implements HOSE and HNX trading rules and session validations
"""

from datetime import datetime, time
from typing import Dict, List, Tuple, Optional
from enum import Enum

from ..models import (
    OrderTypeEnum, 
    MarketEnum, 
    TradingSessionEnum,
    BuySellEnum
)
from ..utils.exceptions import TradingSessionError, ValidationError


class TradingRules:
    """Trading rules for Vietnamese exchanges"""
    
    # HOSE Trading Sessions
    HOSE_SESSIONS = {
        TradingSessionEnum.OPENING_AUCTION: {
            "start": time(9, 0),
            "end": time(9, 15),
            "allowed_orders": [OrderTypeEnum.ATO, OrderTypeEnum.LIMIT],
            "can_cancel": False,
            "can_modify": False,
            "description": "Opening auction (ATO/LO only, no cancel/modify)"
        },
        TradingSessionEnum.CONTINUOUS_1: {
            "start": time(9, 15),
            "end": time(11, 30),
            "allowed_orders": [OrderTypeEnum.LIMIT, OrderTypeEnum.MARKET_TO_LIMIT],
            "can_cancel": True,
            "can_modify": True,
            "description": "Continuous trading I (LO/MTL, can cancel/modify)"
        },
        TradingSessionEnum.LUNCH_BREAK: {
            "start": time(11, 30),
            "end": time(13, 0),
            "allowed_orders": [],
            "can_cancel": False,
            "can_modify": False,
            "description": "Lunch break (no trading activity)"
        },
        TradingSessionEnum.CONTINUOUS_2: {
            "start": time(13, 0),
            "end": time(14, 30),
            "allowed_orders": [OrderTypeEnum.LIMIT, OrderTypeEnum.MARKET_TO_LIMIT],
            "can_cancel": True,
            "can_modify": True,
            "description": "Continuous trading II (LO/MTL, can cancel/modify)"
        },
        TradingSessionEnum.CLOSING_AUCTION: {
            "start": time(14, 30),
            "end": time(14, 45),
            "allowed_orders": [OrderTypeEnum.ATC, OrderTypeEnum.LIMIT],
            "can_cancel": False,
            "can_modify": False,
            "description": "Closing auction (ATC/LO only, no cancel/modify)"
        },
        TradingSessionEnum.PUT_THROUGH: {
            "start": time(9, 0),
            "end": time(15, 0),
            "allowed_orders": [],  # Special block trading
            "can_cancel": False,
            "can_modify": False,
            "description": "Put-through trading (block trades)"
        }
    }
    
    # HNX Trading Sessions
    HNX_SESSIONS = {
        TradingSessionEnum.CONTINUOUS_1: {
            "start": time(9, 0),
            "end": time(11, 30),
            "allowed_orders": [
                OrderTypeEnum.LIMIT, 
                OrderTypeEnum.MARKET_TO_LIMIT,
                OrderTypeEnum.MATCH_OR_KILL,
                OrderTypeEnum.MATCH_AND_KILL
            ],
            "can_cancel": True,
            "can_modify": True,
            "description": "Continuous trading I (LO/MTL/MOK/MAK, can cancel/modify)"
        },
        TradingSessionEnum.LUNCH_BREAK: {
            "start": time(11, 30),
            "end": time(13, 0),
            "allowed_orders": [],
            "can_cancel": False,
            "can_modify": False,
            "description": "Lunch break (no trading activity)"
        },
        TradingSessionEnum.CONTINUOUS_2: {
            "start": time(13, 0),
            "end": time(14, 30),
            "allowed_orders": [
                OrderTypeEnum.LIMIT, 
                OrderTypeEnum.MARKET_TO_LIMIT,
                OrderTypeEnum.MATCH_OR_KILL,
                OrderTypeEnum.MATCH_AND_KILL
            ],
            "can_cancel": True,
            "can_modify": True,
            "description": "Continuous trading II (LO/MTL/MOK/MAK, can cancel/modify)"
        },
        TradingSessionEnum.CLOSING_AUCTION: {
            "start": time(14, 30),
            "end": time(14, 45),
            "allowed_orders": [OrderTypeEnum.ATC, OrderTypeEnum.LIMIT],
            "can_cancel": False,
            "can_modify": False,
            "description": "Closing auction (ATC/LO only, no cancel/modify)"
        },
        TradingSessionEnum.AFTER_HOURS: {
            "start": time(14, 45),
            "end": time(15, 0),
            "allowed_orders": [OrderTypeEnum.POST_LIMIT],
            "can_cancel": False,
            "can_modify": False,
            "description": "After hours (PLO only, no cancel/modify)"
        },
        TradingSessionEnum.PUT_THROUGH: {
            "start": time(9, 0),
            "end": time(15, 0),
            "allowed_orders": [],  # Special block trading
            "can_cancel": False,
            "can_modify": False,
            "description": "Put-through trading (block trades)"
        }
    }
    
    # Price limits (daily volatility limits)
    PRICE_LIMITS = {
        MarketEnum.HOSE: {
            "normal_stocks": 0.07,  # ±7%
            "new_listing": 0.20     # ±20%
        },
        MarketEnum.HNX: {
            "normal_stocks": 0.10,  # ±10%
            "new_listing": 0.30     # ±30%
        },
        MarketEnum.UPCOM: {
            "normal_stocks": 0.15,  # ±15%
            "new_listing": 0.40     # ±40%
        }
    }


class TradingSessionValidator:
    """Validates trading operations based on current session and market rules"""
    
    def __init__(self):
        self.rules = TradingRules()
    
    def get_current_session(self, market: MarketEnum, current_time: datetime = None) -> Tuple[TradingSessionEnum, Dict]:
        """Get current trading session for the specified market"""
        if current_time is None:
            current_time = datetime.now()
        
        current_time_only = current_time.time()
        
        # Select appropriate sessions based on market
        if market == MarketEnum.HOSE:
            sessions = self.rules.HOSE_SESSIONS
        elif market == MarketEnum.HNX:
            sessions = self.rules.HNX_SESSIONS
        else:
            # Default to HOSE rules for other markets
            sessions = self.rules.HOSE_SESSIONS
        
        # Find current session
        for session_type, session_info in sessions.items():
            if session_info["start"] <= current_time_only <= session_info["end"]:
                return session_type, session_info
        
        # If no session found, market is closed
        return None, {"description": "Market closed", "allowed_orders": [], "can_cancel": False, "can_modify": False}
    
    def validate_order_placement(
        self, 
        market: MarketEnum, 
        order_type: OrderTypeEnum,
        current_time: datetime = None
    ) -> Tuple[bool, str]:
        """Validate if order can be placed in current session"""
        
        session_type, session_info = self.get_current_session(market, current_time)
        
        if session_type is None:
            return False, "Market is currently closed"
        
        if session_type == TradingSessionEnum.LUNCH_BREAK:
            return False, "No trading allowed during lunch break"
        
        if order_type not in session_info["allowed_orders"]:
            allowed_types = [ot.value for ot in session_info["allowed_orders"]]
            return False, f"Order type {order_type.value} not allowed in {session_type.value}. Allowed: {allowed_types}"
        
        return True, f"Order placement allowed in {session_type.value}"
    
    def validate_order_modification(
        self, 
        market: MarketEnum,
        current_time: datetime = None
    ) -> Tuple[bool, str]:
        """Validate if order can be modified in current session"""
        
        session_type, session_info = self.get_current_session(market, current_time)
        
        if session_type is None:
            return False, "Market is currently closed"
        
        if not session_info["can_modify"]:
            return False, f"Order modification not allowed in {session_type.value}"
        
        return True, f"Order modification allowed in {session_type.value}"
    
    def validate_order_cancellation(
        self, 
        market: MarketEnum,
        current_time: datetime = None
    ) -> Tuple[bool, str]:
        """Validate if order can be cancelled in current session"""
        
        session_type, session_info = self.get_current_session(market, current_time)
        
        if session_type is None:
            return False, "Market is currently closed"
        
        if not session_info["can_cancel"]:
            return False, f"Order cancellation not allowed in {session_type.value}"
        
        return True, f"Order cancellation allowed in {session_type.value}"
    
    def validate_price_limit(
        self, 
        market: MarketEnum, 
        instrument_id: str,
        price: float, 
        reference_price: float,
        is_new_listing: bool = False
    ) -> Tuple[bool, str, float, float]:
        """Validate if price is within daily limit"""
        
        if market not in self.rules.PRICE_LIMITS:
            return True, "No price limit validation for this market", 0, float('inf')
        
        limits = self.rules.PRICE_LIMITS[market]
        limit_pct = limits["new_listing"] if is_new_listing else limits["normal_stocks"]
        
        price_limit_up = reference_price * (1 + limit_pct)
        price_limit_down = reference_price * (1 - limit_pct)
        
        if price > price_limit_up:
            return False, f"Price {price} exceeds upper limit {price_limit_up:.0f}", price_limit_down, price_limit_up
        
        if price < price_limit_down:
            return False, f"Price {price} below lower limit {price_limit_down:.0f}", price_limit_down, price_limit_up
        
        return True, "Price within daily limits", price_limit_down, price_limit_up
    
    def get_market_status(self, market: MarketEnum, current_time: datetime = None) -> Dict:
        """Get comprehensive market status information"""
        
        session_type, session_info = self.get_current_session(market, current_time)
        
        if current_time is None:
            current_time = datetime.now()
        
        return {
            "market": market.value,
            "current_time": current_time.isoformat(),
            "session": session_type.value if session_type else "CLOSED",
            "session_info": session_info,
            "is_open": session_type is not None and session_type != TradingSessionEnum.LUNCH_BREAK,
            "can_place_orders": len(session_info["allowed_orders"]) > 0,
            "can_modify_orders": session_info["can_modify"],
            "can_cancel_orders": session_info["can_cancel"],
            "allowed_order_types": [ot.value for ot in session_info["allowed_orders"]]
        }


# Global validator instance
trading_validator = TradingSessionValidator()


def validate_trading_request(
    market: MarketEnum,
    order_type: OrderTypeEnum,
    action: str = "place",  # "place", "modify", "cancel"
    current_time: datetime = None
) -> Tuple[bool, str]:
    """
    Comprehensive trading request validation
    
    Args:
        market: Target market (HOSE, HNX, etc.)
        order_type: Type of order
        action: Trading action (place, modify, cancel)
        current_time: Time to validate against (defaults to now)
    
    Returns:
        Tuple of (is_valid, message)
    """
    
    try:
        if action == "place":
            return trading_validator.validate_order_placement(market, order_type, current_time)
        elif action == "modify":
            return trading_validator.validate_order_modification(market, current_time)
        elif action == "cancel":
            return trading_validator.validate_order_cancellation(market, current_time)
        else:
            return False, f"Unknown action: {action}"
            
    except Exception as e:
        return False, f"Validation error: {str(e)}"


def get_trading_session_info(market: MarketEnum, current_time: datetime = None) -> Dict:
    """Get current trading session information"""
    return trading_validator.get_market_status(market, current_time)
