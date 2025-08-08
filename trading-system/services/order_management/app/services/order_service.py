"""
Order Service - Core business logic for order management.
"""

import asyncio
import uuid
from datetime import datetime, time
from typing import Any, Dict, List, Optional

from ..models import (
    OrderCreateRequest, OrderModifyRequest, OrderCancelRequest,
    OrderResponse, OrderStatus, OrderSide, OrderType, Market,
    TradingSession, TradingSessionInfo
)


class OrderService:
    """Service for order management operations."""
    
    def __init__(self):
        """Initialize order service."""
        self.orders: Dict[str, Dict] = {}  # In-memory storage for demo
    
    async def create_order(
        self, 
        order_request: OrderCreateRequest, 
        user_id: str
    ) -> OrderResponse:
        """Create a new order."""
        
        # Generate order ID
        order_id = f"ORD_{int(datetime.now().timestamp())}_{uuid.uuid4().hex[:8]}"
        
        # Validate trading session
        session_info = await self._get_current_session()
        if not session_info.can_place_orders:
            raise ValueError(f"Cannot place orders during {session_info.current_session}")
        
        # Validate order request
        await self._validate_order_request(order_request)
        
        # Create order object
        order_data = {
            "id": str(uuid.uuid4()),
            "order_id": order_id,
            "client_order_id": order_request.client_order_id,
            "instrument_id": order_request.instrument_id,
            "symbol": order_request.symbol,
            "market": order_request.market,
            "side": order_request.side,
            "order_type": order_request.order_type,
            "quantity": order_request.quantity,
            "price": order_request.price,
            "filled_quantity": 0,
            "remaining_quantity": order_request.quantity,
            "average_price": None,
            "status": OrderStatus.PENDING,
            "order_time": datetime.utcnow(),
            "sent_time": None,
            "acknowledged_time": None,
            "last_updated": datetime.utcnow(),
            "account_id": order_request.account_id,
            "user_id": user_id,
            "ssi_order_id": None,
            "request_id": None,
            "notes": order_request.notes,
            "error_message": None,
            "trading_session": session_info.current_session,
            "strategy_id": order_request.strategy_id
        }
        
        # Store order
        self.orders[order_id] = order_data
        
        # Send to SSI FastConnect (simulation)
        await self._send_order_to_ssi(order_data)
        
        return OrderResponse(**order_data)
    
    async def modify_order(
        self, 
        modify_request: OrderModifyRequest, 
        user_id: str
    ) -> OrderResponse:
        """Modify an existing order."""
        
        order_id = modify_request.order_id
        
        # Check if order exists
        if order_id not in self.orders:
            raise ValueError(f"Order {order_id} not found")
        
        order_data = self.orders[order_id]
        
        # Validate user ownership
        if order_data["user_id"] != user_id:
            raise ValueError("Access denied: Order belongs to different user")
        
        # Validate order status
        if order_data["status"] not in [OrderStatus.PENDING, OrderStatus.ACKNOWLEDGED]:
            raise ValueError(f"Cannot modify order in {order_data['status']} status")
        
        # Validate trading session
        session_info = await self._get_current_session()
        if not session_info.can_modify_orders:
            raise ValueError(f"Cannot modify orders during {session_info.current_session}")
        
        # Update order data
        if modify_request.price is not None:
            order_data["price"] = modify_request.price
        
        if modify_request.quantity is not None:
            old_quantity = order_data["quantity"]
            filled_quantity = order_data["filled_quantity"]
            
            if modify_request.quantity < filled_quantity:
                raise ValueError("New quantity cannot be less than filled quantity")
            
            order_data["quantity"] = modify_request.quantity
            order_data["remaining_quantity"] = modify_request.quantity - filled_quantity
        
        order_data["last_updated"] = datetime.utcnow()
        order_data["status"] = OrderStatus.PENDING  # Reset to pending for modification
        
        # Send modification to SSI FastConnect (simulation)
        await self._modify_order_at_ssi(order_data)
        
        return OrderResponse(**order_data)
    
    async def cancel_order(
        self, 
        cancel_request: OrderCancelRequest, 
        user_id: str
    ) -> OrderResponse:
        """Cancel an existing order."""
        
        order_id = cancel_request.order_id
        
        # Check if order exists
        if order_id not in self.orders:
            raise ValueError(f"Order {order_id} not found")
        
        order_data = self.orders[order_id]
        
        # Validate user ownership
        if order_data["user_id"] != user_id:
            raise ValueError("Access denied: Order belongs to different user")
        
        # Validate order status
        if order_data["status"] in [OrderStatus.FILLED, OrderStatus.CANCELLED, OrderStatus.REJECTED]:
            raise ValueError(f"Cannot cancel order in {order_data['status']} status")
        
        # Validate trading session
        session_info = await self._get_current_session()
        if not session_info.can_cancel_orders:
            raise ValueError(f"Cannot cancel orders during {session_info.current_session}")
        
        # Update order status
        order_data["status"] = OrderStatus.CANCELLED
        order_data["last_updated"] = datetime.utcnow()
        if cancel_request.reason:
            order_data["notes"] = f"{order_data.get('notes', '')} | Cancelled: {cancel_request.reason}"
        
        # Send cancellation to SSI FastConnect (simulation)
        await self._cancel_order_at_ssi(order_data)
        
        return OrderResponse(**order_data)
    
    async def get_order(self, order_id: str, user_id: str) -> Optional[OrderResponse]:
        """Get order by ID."""
        
        if order_id not in self.orders:
            return None
        
        order_data = self.orders[order_id]
        
        # Validate user ownership
        if order_data["user_id"] != user_id:
            raise ValueError("Access denied: Order belongs to different user")
        
        return OrderResponse(**order_data)
    
    async def get_orders(
        self, 
        user_id: str,
        account_id: Optional[str] = None,
        symbol: Optional[str] = None,
        status: Optional[OrderStatus] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[OrderResponse]:
        """Get orders with filtering."""
        
        filtered_orders = []
        
        for order_data in self.orders.values():
            # Filter by user
            if order_data["user_id"] != user_id:
                continue
            
            # Filter by account
            if account_id and order_data["account_id"] != account_id:
                continue
            
            # Filter by symbol
            if symbol and order_data["symbol"] != symbol:
                continue
            
            # Filter by status
            if status and order_data["status"] != status:
                continue
            
            filtered_orders.append(OrderResponse(**order_data))
        
        # Sort by order time (newest first)
        filtered_orders.sort(key=lambda x: x.order_time, reverse=True)
        
        # Apply pagination
        return filtered_orders[offset:offset + limit]
    
    async def get_order_history(
        self,
        user_id: str,
        account_id: Optional[str] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[OrderResponse]:
        """Get order history with date filtering."""
        
        filtered_orders = []
        
        for order_data in self.orders.values():
            # Filter by user
            if order_data["user_id"] != user_id:
                continue
            
            # Filter by account
            if account_id and order_data["account_id"] != account_id:
                continue
            
            # Filter by date range
            order_time = order_data["order_time"]
            if from_date and order_time < from_date:
                continue
            if to_date and order_time > to_date:
                continue
            
            # Only include completed orders in history
            if order_data["status"] in [
                OrderStatus.FILLED, 
                OrderStatus.CANCELLED, 
                OrderStatus.REJECTED,
                OrderStatus.EXPIRED
            ]:
                filtered_orders.append(OrderResponse(**order_data))
        
        # Sort by order time (newest first)
        filtered_orders.sort(key=lambda x: x.order_time, reverse=True)
        
        # Apply pagination
        return filtered_orders[offset:offset + limit]
    
    async def _validate_order_request(self, order_request: OrderCreateRequest) -> None:
        """Validate order request."""
        
        # Validate quantity
        if order_request.quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        # Validate price for limit orders
        if order_request.order_type in [OrderType.LIMIT, OrderType.AT_THE_CLOSE]:
            if order_request.price is None or order_request.price <= 0:
                raise ValueError("Price is required and must be positive for limit orders")
        
        # Validate market-specific rules
        if order_request.market == Market.HOSE:
            await self._validate_hose_rules(order_request)
        elif order_request.market == Market.HNX:
            await self._validate_hnx_rules(order_request)
        elif order_request.market == Market.UPCOM:
            await self._validate_upcom_rules(order_request)
    
    async def _validate_hose_rules(self, order_request: OrderCreateRequest) -> None:
        """Validate HOSE-specific trading rules."""
        
        # Validate lot size (usually 100 shares)
        if order_request.quantity % 100 != 0:
            raise ValueError("HOSE requires quantity to be in lots of 100 shares")
        
        # Validate order types
        session_info = await self._get_current_session()
        
        if session_info.current_session == TradingSession.MORNING_AUCTION:
            if order_request.order_type not in [OrderType.AT_THE_OPEN, OrderType.LIMIT]:
                raise ValueError("Only ATO and LO orders allowed during morning auction")
        
        elif session_info.current_session == TradingSession.CLOSING_AUCTION:
            if order_request.order_type not in [OrderType.AT_THE_CLOSE, OrderType.LIMIT]:
                raise ValueError("Only ATC and LO orders allowed during closing auction")
        
        elif session_info.current_session in [
            TradingSession.CONTINUOUS_MORNING, 
            TradingSession.CONTINUOUS_AFTERNOON
        ]:
            if order_request.order_type not in [OrderType.LIMIT, OrderType.MARKET_TO_LIMIT]:
                raise ValueError("Only LO and MTL orders allowed during continuous sessions")
    
    async def _validate_hnx_rules(self, order_request: OrderCreateRequest) -> None:
        """Validate HNX-specific trading rules."""
        
        # Validate lot size (usually 100 shares)
        if order_request.quantity % 100 != 0:
            raise ValueError("HNX requires quantity to be in lots of 100 shares")
        
        # HNX allows more order types
        valid_order_types = [
            OrderType.LIMIT, 
            OrderType.MARKET_TO_LIMIT,
            OrderType.MATCH_OR_KILL,
            OrderType.MATCH_AND_KILL
        ]
        
        session_info = await self._get_current_session()
        
        if session_info.current_session == TradingSession.CLOSING_AUCTION:
            if order_request.order_type not in [OrderType.AT_THE_CLOSE, OrderType.LIMIT]:
                raise ValueError("Only ATC and LO orders allowed during closing auction")
        
        elif session_info.current_session == TradingSession.POST_MARKET:
            if order_request.order_type != OrderType.POST_LIMIT:
                raise ValueError("Only PLO orders allowed during post-market session")
    
    async def _validate_upcom_rules(self, order_request: OrderCreateRequest) -> None:
        """Validate UPCOM-specific trading rules."""
        
        # UPCOM allows odd lots
        if order_request.quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        # Simpler order type validation for UPCOM
        valid_order_types = [OrderType.LIMIT, OrderType.MARKET_TO_LIMIT]
        
        if order_request.order_type not in valid_order_types:
            raise ValueError(f"Order type {order_request.order_type} not supported on UPCOM")
    
    async def _get_current_session(self) -> TradingSessionInfo:
        """Get current trading session information."""
        
        # Simple session determination based on current time
        now = datetime.now().time()
        
        if time(9, 0) <= now < time(9, 15):
            return TradingSessionInfo(
                current_session=TradingSession.MORNING_AUCTION,
                next_session=TradingSession.CONTINUOUS_MORNING,
                session_start_time=datetime.now().replace(hour=9, minute=0, second=0),
                session_end_time=datetime.now().replace(hour=9, minute=15, second=0),
                market_status="OPEN",
                can_place_orders=True,
                can_modify_orders=False,
                can_cancel_orders=False
            )
        
        elif time(9, 15) <= now < time(11, 30):
            return TradingSessionInfo(
                current_session=TradingSession.CONTINUOUS_MORNING,
                next_session=TradingSession.LUNCH_BREAK,
                session_start_time=datetime.now().replace(hour=9, minute=15, second=0),
                session_end_time=datetime.now().replace(hour=11, minute=30, second=0),
                market_status="OPEN",
                can_place_orders=True,
                can_modify_orders=True,
                can_cancel_orders=True
            )
        
        elif time(11, 30) <= now < time(13, 0):
            return TradingSessionInfo(
                current_session=TradingSession.LUNCH_BREAK,
                next_session=TradingSession.CONTINUOUS_AFTERNOON,
                session_start_time=datetime.now().replace(hour=11, minute=30, second=0),
                session_end_time=datetime.now().replace(hour=13, minute=0, second=0),
                market_status="CLOSED",
                can_place_orders=False,
                can_modify_orders=False,
                can_cancel_orders=False
            )
        
        elif time(13, 0) <= now < time(14, 30):
            return TradingSessionInfo(
                current_session=TradingSession.CONTINUOUS_AFTERNOON,
                next_session=TradingSession.CLOSING_AUCTION,
                session_start_time=datetime.now().replace(hour=13, minute=0, second=0),
                session_end_time=datetime.now().replace(hour=14, minute=30, second=0),
                market_status="OPEN",
                can_place_orders=True,
                can_modify_orders=True,
                can_cancel_orders=True
            )
        
        elif time(14, 30) <= now < time(14, 45):
            return TradingSessionInfo(
                current_session=TradingSession.CLOSING_AUCTION,
                next_session=TradingSession.POST_MARKET,
                session_start_time=datetime.now().replace(hour=14, minute=30, second=0),
                session_end_time=datetime.now().replace(hour=14, minute=45, second=0),
                market_status="CLOSING",
                can_place_orders=True,
                can_modify_orders=False,
                can_cancel_orders=False
            )
        
        elif time(14, 45) <= now < time(15, 0):
            return TradingSessionInfo(
                current_session=TradingSession.POST_MARKET,
                next_session=TradingSession.CLOSED,
                session_start_time=datetime.now().replace(hour=14, minute=45, second=0),
                session_end_time=datetime.now().replace(hour=15, minute=0, second=0),
                market_status="POST_TRADING",
                can_place_orders=True,  # PLO orders only
                can_modify_orders=False,
                can_cancel_orders=False
            )
        
        else:
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
    
    async def _send_order_to_ssi(self, order_data: Dict[str, Any]) -> None:
        """Send order to SSI FastConnect (simulation)."""
        
        # Simulate API call delay
        await asyncio.sleep(0.1)
        
        # Simulate SSI response
        order_data["status"] = OrderStatus.SENT
        order_data["sent_time"] = datetime.utcnow()
        order_data["ssi_order_id"] = f"SSI_{order_data['order_id']}"
        order_data["request_id"] = f"REQ_{uuid.uuid4().hex[:8]}"
        
        # Simulate acknowledgment
        await asyncio.sleep(0.1)
        order_data["status"] = OrderStatus.ACKNOWLEDGED
        order_data["acknowledged_time"] = datetime.utcnow()
        
        print(f"Order {order_data['order_id']} sent to SSI FastConnect")
    
    async def _modify_order_at_ssi(self, order_data: Dict[str, Any]) -> None:
        """Modify order at SSI FastConnect (simulation)."""
        
        # Simulate API call delay
        await asyncio.sleep(0.1)
        
        # Update order status
        order_data["status"] = OrderStatus.ACKNOWLEDGED
        order_data["last_updated"] = datetime.utcnow()
        
        print(f"Order {order_data['order_id']} modified at SSI FastConnect")
    
    async def _cancel_order_at_ssi(self, order_data: Dict[str, Any]) -> None:
        """Cancel order at SSI FastConnect (simulation)."""
        
        # Simulate API call delay
        await asyncio.sleep(0.1)
        
        print(f"Order {order_data['order_id']} cancelled at SSI FastConnect")
