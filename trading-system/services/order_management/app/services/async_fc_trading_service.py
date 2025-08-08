"""
Async wrapper for FC Trading Service
Provides async interface for web API integration
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List
import json

from .fc_trading_service import FCTradingService

logger = logging.getLogger(__name__)


class AsyncFCTradingService:
    """Async wrapper for FC Trading Service"""
    
    def __init__(self):
        self.fc_service = FCTradingService()
        self._authenticated_users = set()  # Track authenticated users
        
    def _run_in_executor(self, func, *args, **kwargs):
        """Run sync function in executor"""
        loop = asyncio.get_event_loop()
        return loop.run_in_executor(None, func, *args, **kwargs)
    
    def _parse_response(self, response_str: str) -> Dict[str, Any]:
        """Parse JSON response string"""
        try:
            return json.loads(response_str)
        except (json.JSONDecodeError, TypeError):
            return {
                'success': False,
                'message': 'Invalid response format',
                'data': None
            }
    
    async def is_available(self) -> bool:
        """Check if FC Trading Service is available"""
        try:
            return await self._run_in_executor(self.fc_service.is_available)
        except Exception as e:
            logger.error(f"Error checking FC Trading availability: {e}")
            return False
    
    async def get_otp(self, user_id: str) -> Dict[str, Any]:
        """Request OTP for authentication"""
        try:
            response = await self._run_in_executor(self.fc_service.get_otp)
            result = self._parse_response(response)
            
            if result.get('success'):
                # Mark OTP as requested for this user
                logger.info(f"OTP requested for user {user_id}")
                
            return result
        except Exception as e:
            logger.error(f"Error requesting OTP for user {user_id}: {e}")
            return {
                'success': False,
                'message': f'Error requesting OTP: {str(e)}',
                'data': None
            }
    
    async def verify_otp(self, user_id: str, otp_code: str) -> Dict[str, Any]:
        """Verify OTP code"""
        try:
            response = await self._run_in_executor(self.fc_service.verify_code, otp_code)
            result = self._parse_response(response)
            
            if result.get('success'):
                # Mark user as authenticated
                self._authenticated_users.add(user_id)
                logger.info(f"User {user_id} authenticated successfully")
            
            return result
        except Exception as e:
            logger.error(f"Error verifying OTP for user {user_id}: {e}")
            return {
                'success': False,
                'message': f'Error verifying OTP: {str(e)}',
                'data': None
            }
    
    async def get_account_balance(self, user_id: str) -> Dict[str, Any]:
        """Get account balance information"""
        try:
            if not self._is_user_authenticated(user_id):
                return {
                    'success': False,
                    'message': 'User not authenticated',
                    'data': None
                }
            
            response = await self._run_in_executor(self.fc_service.get_account_info)
            result = self._parse_response(response)
            
            # Extract balance information from account info
            if result.get('success') and result.get('data'):
                account_data = result['data']
                balance_data = {
                    'cash': account_data.get('cash', 0),
                    'market_value': account_data.get('asset_value', 0),
                    'total_value': account_data.get('nav', 0),
                    'buying_power': account_data.get('max_buy_power', 0)
                }
                return {
                    'success': True,
                    'message': 'Balance retrieved successfully',
                    'data': balance_data
                }
            
            return result
        except Exception as e:
            logger.error(f"Error getting balance for user {user_id}: {e}")
            return {
                'success': False,
                'message': f'Error getting balance: {str(e)}',
                'data': None
            }
    
    async def get_positions(self, user_id: str) -> Dict[str, Any]:
        """Get account positions"""
        try:
            if not self._is_user_authenticated(user_id):
                return {
                    'success': False,
                    'message': 'User not authenticated',
                    'data': None
                }
            
            response = await self._run_in_executor(self.fc_service.get_positions)
            return self._parse_response(response)
        except Exception as e:
            logger.error(f"Error getting positions for user {user_id}: {e}")
            return {
                'success': False,
                'message': f'Error getting positions: {str(e)}',
                'data': None
            }
    
    async def get_orders(self, user_id: str) -> Dict[str, Any]:
        """Get pending orders"""
        try:
            if not self._is_user_authenticated(user_id):
                return {
                    'success': False,
                    'message': 'User not authenticated',
                    'data': None
                }
            
            response = await self._run_in_executor(self.fc_service.get_orders)
            return self._parse_response(response)
        except Exception as e:
            logger.error(f"Error getting orders for user {user_id}: {e}")
            return {
                'success': False,
                'message': f'Error getting orders: {str(e)}',
                'data': None
            }
    
    async def get_order_history(self, user_id: str) -> Dict[str, Any]:
        """Get order history"""
        try:
            if not self._is_user_authenticated(user_id):
                return {
                    'success': False,
                    'message': 'User not authenticated',
                    'data': None
                }
            
            # FC Trading Service doesn't have specific order history method
            # Use get_orders and filter for historical data
            response = await self._run_in_executor(self.fc_service.get_orders)
            result = self._parse_response(response)
            
            if result.get('success'):
                # Filter for completed orders (history)
                orders = result.get('data', [])
                history = [order for order in orders if order.get('status') in ['FILLED', 'CANCELLED', 'REJECTED']]
                return {
                    'success': True,
                    'message': 'Order history retrieved successfully',
                    'data': history
                }
            
            return result
        except Exception as e:
            logger.error(f"Error getting order history for user {user_id}: {e}")
            return {
                'success': False,
                'message': f'Error getting order history: {str(e)}',
                'data': None
            }
    
    async def get_symbols(self) -> Dict[str, Any]:
        """Get available trading symbols"""
        try:
            # Use search_symbols to get available symbols
            response = await self._run_in_executor(self.fc_service.search_symbols, "")
            result = self._parse_response(response)
            
            if result.get('success'):
                return result
            else:
                # Return mock data if service not available
                return {
                    'success': True,
                    'message': 'Mock symbols data',
                    'data': [
                        {'symbol': 'VN30F2412', 'name': 'VN30 Future Dec 2024'},
                        {'symbol': 'VIC', 'name': 'Vingroup JSC'},
                        {'symbol': 'VHM', 'name': 'Vinhomes JSC'},
                        {'symbol': 'HPG', 'name': 'Hoa Phat Group JSC'},
                        {'symbol': 'TCB', 'name': 'Techcombank'},
                        {'symbol': 'VCB', 'name': 'Vietcombank'},
                        {'symbol': 'BID', 'name': 'BIDV'},
                        {'symbol': 'CTG', 'name': 'VietinBank'},
                        {'symbol': 'MSN', 'name': 'Masan Group'},
                        {'symbol': 'GAS', 'name': 'PetroVietnam Gas JSC'}
                    ]
                }
        except Exception as e:
            logger.error(f"Error getting symbols: {e}")
            return {
                'success': True,
                'message': 'Mock symbols data (error fallback)',
                'data': [
                    {'symbol': 'VN30F2412', 'name': 'VN30 Future Dec 2024'},
                    {'symbol': 'VIC', 'name': 'Vingroup JSC'},
                    {'symbol': 'VHM', 'name': 'Vinhomes JSC'}
                ]
            }
    
    async def get_stock_price(self, symbol: str) -> Dict[str, Any]:
        """Get current stock price"""
        try:
            response = await self._run_in_executor(self.fc_service.get_market_data, symbol)
            result = self._parse_response(response)
            
            if result.get('success') and result.get('data'):
                market_data = result['data']
                price_data = {
                    'symbol': symbol,
                    'current_price': market_data.get('last_price', 0),
                    'bid_price': market_data.get('bid_price', 0),
                    'ask_price': market_data.get('ask_price', 0),
                    'change': market_data.get('change', 0),
                    'change_percent': market_data.get('change_percent', 0)
                }
                return {
                    'success': True,
                    'message': 'Price data retrieved successfully',
                    'data': price_data
                }
            
            return result
        except Exception as e:
            logger.error(f"Error getting price for {symbol}: {e}")
            return {
                'success': False,
                'message': f'Error getting price: {str(e)}',
                'data': None
            }
    
    async def place_order(self, user_id: str, symbol: str, side: str, volume: int, 
                         price: float, order_type: str = 'LO') -> Dict[str, Any]:
        """Place a trading order"""
        try:
            if not self._is_user_authenticated(user_id):
                return {
                    'success': False,
                    'message': 'User not authenticated',
                    'data': None
                }
            
            # Prepare order data
            order_data = {
                'instrument_id': symbol,
                'price': price,
                'quantity': volume,
                'buy_sell': 'B' if side.upper() == 'BUY' else 'S',
                'order_type': order_type.upper(),
                'account_id': ''  # Will be filled by FC service
            }
            
            response = await self._run_in_executor(self.fc_service.place_order, order_data)
            result = self._parse_response(response)
            
            if result.get('success'):
                logger.info(f"Order placed successfully for user {user_id}: {symbol} {side} {volume}@{price}")
            
            return result
        except Exception as e:
            logger.error(f"Error placing order for user {user_id}: {e}")
            return {
                'success': False,
                'message': f'Error placing order: {str(e)}',
                'data': None
            }
    
    async def cancel_order(self, user_id: str, order_id: str) -> Dict[str, Any]:
        """Cancel an order"""
        try:
            if not self._is_user_authenticated(user_id):
                return {
                    'success': False,
                    'message': 'User not authenticated',
                    'data': None
                }
            
            response = await self._run_in_executor(self.fc_service.cancel_order, order_id)
            return self._parse_response(response)
        except Exception as e:
            logger.error(f"Error cancelling order {order_id} for user {user_id}: {e}")
            return {
                'success': False,
                'message': f'Error cancelling order: {str(e)}',
                'data': None
            }
    
    def _is_user_authenticated(self, user_id: str) -> bool:
        """Check if user is authenticated"""
        return user_id in self._authenticated_users
    
    def logout_user(self, user_id: str):
        """Logout user (remove from authenticated users)"""
        self._authenticated_users.discard(user_id)
        logger.info(f"User {user_id} logged out")


# Global instance
async_fc_trading_service = AsyncFCTradingService()
