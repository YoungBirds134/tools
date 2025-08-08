"""
Trading Session Service - Manages trading session information and rules.
"""

from datetime import datetime, time, timedelta
from typing import Dict, Optional

from ..models import TradingSession, TradingSessionInfo, Market


class TradingSessionService:
    """Service for managing trading session information."""
    
    def __init__(self):
        """Initialize trading session service."""
        self.session_cache: Optional[TradingSessionInfo] = None
        self.cache_expiry: Optional[datetime] = None
        self.cache_duration = timedelta(minutes=1)  # Cache for 1 minute
    
    async def get_current_session(self) -> Dict[str, any]:
        """Get current trading session information."""
        
        # Check cache
        if (self.session_cache and 
            self.cache_expiry and 
            datetime.now() < self.cache_expiry):
            return self._session_to_dict(self.session_cache)
        
        # Calculate current session
        session_info = await self._calculate_current_session()
        
        # Update cache
        self.session_cache = session_info
        self.cache_expiry = datetime.now() + self.cache_duration
        
        return self._session_to_dict(session_info)
    
    async def _calculate_current_session(self) -> TradingSessionInfo:
        """Calculate current trading session based on Vietnam time."""
        
        now = datetime.now()
        current_time = now.time()
        
        # Check if it's a weekend
        if now.weekday() >= 5:  # Saturday (5) or Sunday (6)
            return TradingSessionInfo(
                current_session=TradingSession.CLOSED,
                next_session=TradingSession.MORNING_AUCTION,
                session_start_time=None,
                session_end_time=None,
                market_status="WEEKEND",
                can_place_orders=False,
                can_modify_orders=False,
                can_cancel_orders=False
            )
        
        # Define trading session times
        sessions = [
            {
                "session": TradingSession.MORNING_AUCTION,
                "start": time(9, 0),
                "end": time(9, 15),
                "next_session": TradingSession.CONTINUOUS_MORNING,
                "market_status": "AUCTION",
                "can_place_orders": True,
                "can_modify_orders": False,
                "can_cancel_orders": False
            },
            {
                "session": TradingSession.CONTINUOUS_MORNING,
                "start": time(9, 15),
                "end": time(11, 30),
                "next_session": TradingSession.LUNCH_BREAK,
                "market_status": "OPEN",
                "can_place_orders": True,
                "can_modify_orders": True,
                "can_cancel_orders": True
            },
            {
                "session": TradingSession.LUNCH_BREAK,
                "start": time(11, 30),
                "end": time(13, 0),
                "next_session": TradingSession.CONTINUOUS_AFTERNOON,
                "market_status": "BREAK",
                "can_place_orders": False,
                "can_modify_orders": False,
                "can_cancel_orders": False
            },
            {
                "session": TradingSession.CONTINUOUS_AFTERNOON,
                "start": time(13, 0),
                "end": time(14, 30),
                "next_session": TradingSession.CLOSING_AUCTION,
                "market_status": "OPEN",
                "can_place_orders": True,
                "can_modify_orders": True,
                "can_cancel_orders": True
            },
            {
                "session": TradingSession.CLOSING_AUCTION,
                "start": time(14, 30),
                "end": time(14, 45),
                "next_session": TradingSession.POST_MARKET,
                "market_status": "CLOSING",
                "can_place_orders": True,
                "can_modify_orders": False,
                "can_cancel_orders": False
            },
            {
                "session": TradingSession.POST_MARKET,
                "start": time(14, 45),
                "end": time(15, 0),
                "next_session": TradingSession.CLOSED,
                "market_status": "POST_TRADING",
                "can_place_orders": True,  # PLO orders only
                "can_modify_orders": False,
                "can_cancel_orders": False
            }
        ]
        
        # Find current session
        for session_info in sessions:
            start_time = session_info["start"]
            end_time = session_info["end"]
            
            if start_time <= current_time < end_time:
                return TradingSessionInfo(
                    current_session=session_info["session"],
                    next_session=session_info["next_session"],
                    session_start_time=now.replace(
                        hour=start_time.hour,
                        minute=start_time.minute,
                        second=0,
                        microsecond=0
                    ),
                    session_end_time=now.replace(
                        hour=end_time.hour,
                        minute=end_time.minute,
                        second=0,
                        microsecond=0
                    ),
                    market_status=session_info["market_status"],
                    can_place_orders=session_info["can_place_orders"],
                    can_modify_orders=session_info["can_modify_orders"],
                    can_cancel_orders=session_info["can_cancel_orders"]
                )
        
        # Outside trading hours
        return TradingSessionInfo(
            current_session=TradingSession.CLOSED,
            next_session=TradingSession.MORNING_AUCTION,
            session_start_time=None,
            session_end_time=None,
            market_status="CLOSED",
            can_place_orders=False,
            can_modify_orders=False,
            can_cancel_orders=False
        )
    
    def _session_to_dict(self, session_info: TradingSessionInfo) -> Dict[str, any]:
        """Convert TradingSessionInfo to dictionary."""
        return {
            "current_session": session_info.current_session.value,
            "next_session": session_info.next_session.value if session_info.next_session else None,
            "session_start_time": session_info.session_start_time.isoformat() if session_info.session_start_time else None,
            "session_end_time": session_info.session_end_time.isoformat() if session_info.session_end_time else None,
            "market_status": session_info.market_status,
            "can_place_orders": session_info.can_place_orders,
            "can_modify_orders": session_info.can_modify_orders,
            "can_cancel_orders": session_info.can_cancel_orders
        }
    
    async def get_market_schedule(self, date: Optional[datetime] = None) -> Dict[str, any]:
        """Get market schedule for a specific date."""
        
        if date is None:
            date = datetime.now()
        
        # Check if it's a weekend
        if date.weekday() >= 5:
            return {
                "date": date.strftime("%Y-%m-%d"),
                "is_trading_day": False,
                "reason": "Weekend",
                "sessions": []
            }
        
        # Check if it's a public holiday (simplified)
        holidays = await self._get_public_holidays(date.year)
        if date.date() in holidays:
            return {
                "date": date.strftime("%Y-%m-%d"),
                "is_trading_day": False,
                "reason": "Public Holiday",
                "sessions": []
            }
        
        # Return normal trading schedule
        sessions = [
            {
                "name": "Morning Auction",
                "type": "AUCTION",
                "start_time": "09:00:00",
                "end_time": "09:15:00",
                "can_place_orders": True,
                "can_modify_orders": False,
                "can_cancel_orders": False
            },
            {
                "name": "Continuous Morning",
                "type": "CONTINUOUS",
                "start_time": "09:15:00",
                "end_time": "11:30:00",
                "can_place_orders": True,
                "can_modify_orders": True,
                "can_cancel_orders": True
            },
            {
                "name": "Lunch Break",
                "type": "BREAK",
                "start_time": "11:30:00",
                "end_time": "13:00:00",
                "can_place_orders": False,
                "can_modify_orders": False,
                "can_cancel_orders": False
            },
            {
                "name": "Continuous Afternoon",
                "type": "CONTINUOUS",
                "start_time": "13:00:00",
                "end_time": "14:30:00",
                "can_place_orders": True,
                "can_modify_orders": True,
                "can_cancel_orders": True
            },
            {
                "name": "Closing Auction",
                "type": "AUCTION",
                "start_time": "14:30:00",
                "end_time": "14:45:00",
                "can_place_orders": True,
                "can_modify_orders": False,
                "can_cancel_orders": False
            },
            {
                "name": "Post Market",
                "type": "POST_MARKET",
                "start_time": "14:45:00",
                "end_time": "15:00:00",
                "can_place_orders": True,  # PLO only
                "can_modify_orders": False,
                "can_cancel_orders": False
            }
        ]
        
        return {
            "date": date.strftime("%Y-%m-%d"),
            "is_trading_day": True,
            "timezone": "Asia/Ho_Chi_Minh",
            "sessions": sessions
        }
    
    async def _get_public_holidays(self, year: int) -> set:
        """Get public holidays for Vietnam (simplified)."""
        
        # This is a simplified list - in production, this should be
        # fetched from a holiday calendar service or database
        holidays = set()
        
        # New Year's Day
        holidays.add(datetime(year, 1, 1).date())
        
        # Vietnamese New Year (Tet) - approximate dates
        # This should be calculated properly based on lunar calendar
        if year == 2025:
            # Tet 2025: January 28 - February 3
            for day in range(28, 32):
                holidays.add(datetime(year, 1, day).date())
            for day in range(1, 4):
                holidays.add(datetime(year, 2, day).date())
        
        # Hung Kings' Day (10th day of 3rd lunar month)
        # Liberation Day (April 30)
        holidays.add(datetime(year, 4, 30).date())
        
        # International Workers' Day (May 1)
        holidays.add(datetime(year, 5, 1).date())
        
        # National Day (September 2)
        holidays.add(datetime(year, 9, 2).date())
        
        return holidays
    
    async def is_trading_allowed(
        self, 
        market: Market, 
        order_type: str,
        action: str = "place"  # place, modify, cancel
    ) -> Dict[str, any]:
        """Check if trading action is allowed for specific market and order type."""
        
        session_info = await self.get_current_session()
        current_session = session_info["current_session"]
        
        # Base permissions from session
        base_permissions = {
            "place": session_info["can_place_orders"],
            "modify": session_info["can_modify_orders"],
            "cancel": session_info["can_cancel_orders"]
        }
        
        # Market-specific rules
        market_rules = await self._get_market_specific_rules(market, current_session, order_type)
        
        # Combine base permissions with market-specific rules
        allowed = base_permissions.get(action, False) and market_rules.get(action, False)
        
        return {
            "allowed": allowed,
            "session": current_session,
            "market": market.value,
            "order_type": order_type,
            "action": action,
            "reason": market_rules.get("reason") if not allowed else None
        }
    
    async def _get_market_specific_rules(
        self, 
        market: Market, 
        session: str, 
        order_type: str
    ) -> Dict[str, any]:
        """Get market-specific trading rules."""
        
        rules = {
            "place": True,
            "modify": True,
            "cancel": True,
            "reason": None
        }
        
        # HOSE-specific rules
        if market == Market.HOSE:
            if session == "MORNING_AUCTION":
                if order_type not in ["ATO", "LO"]:
                    rules.update({
                        "place": False,
                        "reason": "Only ATO and LO orders allowed during morning auction on HOSE"
                    })
                rules.update({"modify": False, "cancel": False})
            
            elif session == "CLOSING_AUCTION":
                if order_type not in ["ATC", "LO"]:
                    rules.update({
                        "place": False,
                        "reason": "Only ATC and LO orders allowed during closing auction on HOSE"
                    })
                rules.update({"modify": False, "cancel": False})
        
        # HNX-specific rules
        elif market == Market.HNX:
            if session == "CLOSING_AUCTION":
                if order_type not in ["ATC", "LO"]:
                    rules.update({
                        "place": False,
                        "reason": "Only ATC and LO orders allowed during closing auction on HNX"
                    })
                rules.update({"modify": False, "cancel": False})
            
            elif session == "POST_MARKET":
                if order_type != "PLO":
                    rules.update({
                        "place": False,
                        "reason": "Only PLO orders allowed during post-market session on HNX"
                    })
                rules.update({"modify": False, "cancel": False})
        
        # UPCOM-specific rules
        elif market == Market.UPCOM:
            if order_type not in ["LO", "MTL"]:
                rules.update({
                    "place": False,
                    "reason": f"Order type {order_type} not supported on UPCOM"
                })
        
        return rules
    
    async def get_next_trading_session(self) -> Dict[str, any]:
        """Get information about the next trading session."""
        
        current_session = await self.get_current_session()
        
        if current_session["next_session"]:
            return {
                "next_session": current_session["next_session"],
                "estimated_start_time": self._get_next_session_start_time(current_session["next_session"]),
                "current_session_ends_at": current_session["session_end_time"]
            }
        
        # If no next session today, return next trading day
        next_trading_day = await self._get_next_trading_day()
        
        return {
            "next_session": "MORNING_AUCTION",
            "estimated_start_time": f"{next_trading_day}T09:00:00",
            "next_trading_date": next_trading_day
        }
    
    def _get_next_session_start_time(self, next_session: str) -> str:
        """Get estimated start time for next session."""
        
        session_times = {
            "MORNING_AUCTION": "09:00:00",
            "CONTINUOUS_MORNING": "09:15:00",
            "LUNCH_BREAK": "11:30:00",
            "CONTINUOUS_AFTERNOON": "13:00:00",
            "CLOSING_AUCTION": "14:30:00",
            "POST_MARKET": "14:45:00",
            "CLOSED": None
        }
        
        today = datetime.now().strftime("%Y-%m-%d")
        time_str = session_times.get(next_session)
        
        if time_str:
            return f"{today}T{time_str}"
        
        return None
    
    async def _get_next_trading_day(self) -> str:
        """Get next trading day (skipping weekends and holidays)."""
        
        current_date = datetime.now().date()
        next_date = current_date + timedelta(days=1)
        
        # Skip weekends
        while next_date.weekday() >= 5:  # Saturday or Sunday
            next_date += timedelta(days=1)
        
        # Skip holidays (simplified check)
        holidays = await self._get_public_holidays(next_date.year)
        while next_date in holidays:
            next_date += timedelta(days=1)
            # Skip weekends again if holiday skip leads to weekend
            while next_date.weekday() >= 5:
                next_date += timedelta(days=1)
        
        return next_date.strftime("%Y-%m-%d")
