"""
Portfolio Service - Manages portfolio positions and calculations.
"""

from decimal import Decimal
from typing import Dict, List, Optional
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_

from ..models import (
    Position, Order, OrderExecution, 
    OrderSide, OrderStatus, OrderType,
    PositionResponse, PortfolioSummary, PositionHistory
)
from ....common.logging import LoggerManager


class PortfolioService:
    """Service for managing portfolio positions and calculations."""
    
    def __init__(self, db: Session):
        """Initialize portfolio service."""
        self.db = db
        self.logger = LoggerManager.get_logger("portfolio_service")
    
    async def get_positions(
        self, 
        account_id: str,
        symbol: Optional[str] = None,
        include_zero_positions: bool = False
    ) -> List[PositionResponse]:
        """Get current positions for an account."""
        
        try:
            query = self.db.query(Position).filter(Position.account_id == account_id)
            
            if symbol:
                query = query.filter(Position.symbol == symbol)
            
            if not include_zero_positions:
                query = query.filter(Position.quantity > 0)
            
            positions = query.all()
            
            # Convert to response models
            position_responses = []
            for position in positions:
                # Calculate current market value and P&L
                current_price = await self._get_current_price(position.symbol)
                market_value = position.quantity * current_price
                unrealized_pnl = market_value - (position.quantity * position.average_price)
                
                position_response = PositionResponse(
                    id=position.id,
                    account_id=position.account_id,
                    symbol=position.symbol,
                    quantity=position.quantity,
                    available_quantity=position.available_quantity,
                    average_price=position.average_price,
                    market_value=market_value,
                    unrealized_pnl=unrealized_pnl,
                    cost_basis=position.quantity * position.average_price,
                    last_updated=position.updated_at
                )
                position_responses.append(position_response)
            
            self.logger.info(f"Retrieved {len(position_responses)} positions for account {account_id}")
            return position_responses
            
        except Exception as e:
            self.logger.error(f"Error getting positions for account {account_id}: {str(e)}")
            raise
    
    async def get_position(self, account_id: str, symbol: str) -> Optional[PositionResponse]:
        """Get specific position for an account and symbol."""
        
        try:
            position = self.db.query(Position).filter(
                and_(
                    Position.account_id == account_id,
                    Position.symbol == symbol
                )
            ).first()
            
            if not position:
                return None
            
            # Calculate current market value and P&L
            current_price = await self._get_current_price(symbol)
            market_value = position.quantity * current_price
            unrealized_pnl = market_value - (position.quantity * position.average_price)
            
            return PositionResponse(
                id=position.id,
                account_id=position.account_id,
                symbol=position.symbol,
                quantity=position.quantity,
                available_quantity=position.available_quantity,
                average_price=position.average_price,
                market_value=market_value,
                unrealized_pnl=unrealized_pnl,
                cost_basis=position.quantity * position.average_price,
                last_updated=position.updated_at
            )
            
        except Exception as e:
            self.logger.error(f"Error getting position for {account_id}/{symbol}: {str(e)}")
            raise
    
    async def update_position_from_execution(
        self, 
        account_id: str,
        symbol: str,
        side: OrderSide,
        quantity: Decimal,
        price: Decimal,
        execution_id: str
    ) -> Position:
        """Update position based on order execution."""
        
        try:
            # Get or create position
            position = self.db.query(Position).filter(
                and_(
                    Position.account_id == account_id,
                    Position.symbol == symbol
                )
            ).first()
            
            if not position:
                position = Position(
                    account_id=account_id,
                    symbol=symbol,
                    quantity=Decimal('0'),
                    available_quantity=Decimal('0'),
                    average_price=Decimal('0')
                )
                self.db.add(position)
            
            # Calculate new position
            if side == OrderSide.BUY:
                # Buying - increase position
                total_cost = (position.quantity * position.average_price) + (quantity * price)
                new_quantity = position.quantity + quantity
                
                if new_quantity > 0:
                    new_average_price = total_cost / new_quantity
                else:
                    new_average_price = Decimal('0')
                
                position.quantity = new_quantity
                position.available_quantity += quantity  # New shares are immediately available
                position.average_price = new_average_price
                
            else:  # SELL
                # Selling - decrease position
                if position.quantity >= quantity:
                    position.quantity -= quantity
                    position.available_quantity = min(position.available_quantity, position.quantity)
                    # Average price remains the same when selling
                else:
                    self.logger.warning(f"Overselling detected for {symbol}: trying to sell {quantity} but only have {position.quantity}")
                    # Handle overselling case
                    position.quantity = Decimal('0')
                    position.available_quantity = Decimal('0')
            
            position.updated_at = datetime.utcnow()
            
            # Create position history record
            await self._create_position_history(
                position=position,
                execution_id=execution_id,
                change_type="EXECUTION",
                quantity_change=quantity if side == OrderSide.BUY else -quantity,
                price=price
            )
            
            self.db.commit()
            self.logger.info(f"Updated position for {account_id}/{symbol}: {position.quantity} @ {position.average_price}")
            
            return position
            
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Error updating position from execution: {str(e)}")
            raise
    
    async def reserve_quantity(
        self, 
        account_id: str, 
        symbol: str, 
        quantity: Decimal,
        order_id: str
    ) -> bool:
        """Reserve quantity for a sell order."""
        
        try:
            position = self.db.query(Position).filter(
                and_(
                    Position.account_id == account_id,
                    Position.symbol == symbol
                )
            ).first()
            
            if not position or position.available_quantity < quantity:
                self.logger.warning(f"Insufficient available quantity for {symbol}: need {quantity}, have {position.available_quantity if position else 0}")
                return False
            
            # Reserve the quantity
            position.available_quantity -= quantity
            position.updated_at = datetime.utcnow()
            
            # Create position history record
            await self._create_position_history(
                position=position,
                execution_id=order_id,
                change_type="RESERVE",
                quantity_change=-quantity,
                price=Decimal('0')
            )
            
            self.db.commit()
            self.logger.info(f"Reserved {quantity} of {symbol} for order {order_id}")
            
            return True
            
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Error reserving quantity: {str(e)}")
            raise
    
    async def release_quantity(
        self, 
        account_id: str, 
        symbol: str, 
        quantity: Decimal,
        order_id: str
    ) -> bool:
        """Release reserved quantity (e.g., when order is cancelled)."""
        
        try:
            position = self.db.query(Position).filter(
                and_(
                    Position.account_id == account_id,
                    Position.symbol == symbol
                )
            ).first()
            
            if not position:
                self.logger.warning(f"No position found for {account_id}/{symbol} when releasing quantity")
                return False
            
            # Release the quantity
            position.available_quantity += quantity
            # Make sure available quantity doesn't exceed total quantity
            position.available_quantity = min(position.available_quantity, position.quantity)
            position.updated_at = datetime.utcnow()
            
            # Create position history record
            await self._create_position_history(
                position=position,
                execution_id=order_id,
                change_type="RELEASE",
                quantity_change=quantity,
                price=Decimal('0')
            )
            
            self.db.commit()
            self.logger.info(f"Released {quantity} of {symbol} for order {order_id}")
            
            return True
            
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Error releasing quantity: {str(e)}")
            raise
    
    async def get_portfolio_summary(self, account_id: str) -> PortfolioSummary:
        """Get portfolio summary with totals and performance metrics."""
        
        try:
            positions = await self.get_positions(account_id, include_zero_positions=False)
            
            total_market_value = Decimal('0')
            total_cost_basis = Decimal('0')
            total_unrealized_pnl = Decimal('0')
            
            for position in positions:
                total_market_value += position.market_value
                total_cost_basis += position.cost_basis
                total_unrealized_pnl += position.unrealized_pnl
            
            # Calculate daily P&L
            daily_pnl = await self._calculate_daily_pnl(account_id)
            
            # Calculate cash balance (simplified - should integrate with cash management)
            cash_balance = await self._get_cash_balance(account_id)
            
            # Calculate portfolio performance
            total_return_percent = Decimal('0')
            if total_cost_basis > 0:
                total_return_percent = (total_unrealized_pnl / total_cost_basis) * 100
            
            return PortfolioSummary(
                account_id=account_id,
                total_market_value=total_market_value,
                total_cost_basis=total_cost_basis,
                cash_balance=cash_balance,
                total_portfolio_value=total_market_value + cash_balance,
                unrealized_pnl=total_unrealized_pnl,
                daily_pnl=daily_pnl,
                total_return_percent=total_return_percent,
                position_count=len(positions),
                last_updated=datetime.utcnow()
            )
            
        except Exception as e:
            self.logger.error(f"Error calculating portfolio summary for {account_id}: {str(e)}")
            raise
    
    async def get_position_history(
        self, 
        account_id: str,
        symbol: Optional[str] = None,
        days: int = 30
    ) -> List[PositionHistory]:
        """Get position history for the last N days."""
        
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            query = self.db.query(PositionHistory).filter(
                and_(
                    PositionHistory.account_id == account_id,
                    PositionHistory.timestamp >= cutoff_date
                )
            )
            
            if symbol:
                query = query.filter(PositionHistory.symbol == symbol)
            
            history = query.order_by(PositionHistory.timestamp.desc()).all()
            
            return history
            
        except Exception as e:
            self.logger.error(f"Error getting position history: {str(e)}")
            raise
    
    async def _create_position_history(
        self,
        position: Position,
        execution_id: str,
        change_type: str,
        quantity_change: Decimal,
        price: Decimal
    ):
        """Create a position history record."""
        
        try:
            history = PositionHistory(
                account_id=position.account_id,
                symbol=position.symbol,
                timestamp=datetime.utcnow(),
                change_type=change_type,
                quantity_before=position.quantity - quantity_change if change_type == "EXECUTION" and quantity_change > 0 else position.quantity + abs(quantity_change),
                quantity_after=position.quantity,
                quantity_change=quantity_change,
                price=price,
                average_price_before=position.average_price,
                average_price_after=position.average_price,
                execution_id=execution_id
            )
            
            self.db.add(history)
            
        except Exception as e:
            self.logger.error(f"Error creating position history: {str(e)}")
            raise
    
    async def _get_current_price(self, symbol: str) -> Decimal:
        """Get current market price for a symbol."""
        
        # This is a placeholder - in production, this should fetch from
        # market data service or SSI API
        try:
            # For now, return a mock price
            # In production, integrate with market data service
            mock_prices = {
                "VIC": Decimal("85.5"),
                "VHM": Decimal("72.3"),
                "VCB": Decimal("92.8"),
                "TCB": Decimal("26.4"),
                "FPT": Decimal("125.2"),
                "MSN": Decimal("68.9"),
                "HPG": Decimal("25.7"),
                "GAS": Decimal("75.2"),
                "SAB": Decimal("165.8"),
                "CTG": Decimal("34.1")
            }
            
            return mock_prices.get(symbol, Decimal("50.0"))
            
        except Exception as e:
            self.logger.error(f"Error getting current price for {symbol}: {str(e)}")
            return Decimal("0")
    
    async def _calculate_daily_pnl(self, account_id: str) -> Decimal:
        """Calculate daily P&L for the account."""
        
        try:
            # This is a simplified calculation
            # In production, this should track actual daily changes
            today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            
            # Get executions from today
            today_executions = self.db.query(OrderExecution).join(Order).filter(
                and_(
                    Order.account_id == account_id,
                    OrderExecution.execution_time >= today_start,
                    Order.status == OrderStatus.FILLED
                )
            ).all()
            
            daily_pnl = Decimal('0')
            for execution in today_executions:
                # Simplified calculation - should be more sophisticated
                if execution.order.side == OrderSide.SELL:
                    # For sells, calculate realized P&L
                    # This is simplified - should track cost basis properly
                    current_price = await self._get_current_price(execution.order.symbol)
                    daily_pnl += (execution.price - current_price) * execution.quantity
            
            return daily_pnl
            
        except Exception as e:
            self.logger.error(f"Error calculating daily P&L for {account_id}: {str(e)}")
            return Decimal('0')
    
    async def _get_cash_balance(self, account_id: str) -> Decimal:
        """Get cash balance for the account."""
        
        # This is a placeholder - in production, this should integrate
        # with cash management service or account service
        try:
            # Mock cash balance
            return Decimal("1000000.0")  # 1M VND
            
        except Exception as e:
            self.logger.error(f"Error getting cash balance for {account_id}: {str(e)}")
            return Decimal('0')
    
    async def calculate_buying_power(self, account_id: str) -> Dict[str, Decimal]:
        """Calculate available buying power."""
        
        try:
            cash_balance = await self._get_cash_balance(account_id)
            
            # Get margin requirements (simplified)
            # In production, this should consider:
            # - Margin requirements per stock
            # - Account type (margin vs cash)
            # - Risk limits
            
            # For now, assume 100% cash buying power
            return {
                "cash_balance": cash_balance,
                "buying_power": cash_balance,
                "margin_used": Decimal('0'),
                "margin_available": Decimal('0')
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating buying power for {account_id}: {str(e)}")
            raise
