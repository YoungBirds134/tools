"""
Order Management Service - Services Package
"""

try:
    from .order_service import OrderService
    from .portfolio_service import PortfolioService
    from .trading_session_service import TradingSessionService
    
    __all__ = ["OrderService", "PortfolioService", "TradingSessionService"]
except ImportError:
    # Fallback for development environment
    __all__ = []
    FCTradingClient = None
    fcmodel_requests = None
    SSI_AVAILABLE = False

from ..config import settings
from typing import Optional
import random
import logging
import json

logger = logging.getLogger(__name__)


class FCTradingService:
    def __init__(self):
        self.client = None
        
        if not SSI_AVAILABLE:
            logger.warning("SSI FC Trading library not available. Service will run in mock mode.")
            return
        
        # Check if private key is valid before initializing client
        # if not settings.is_private_key_valid:
        #     logger.warning("Invalid or missing private key. FCTradingClient will not be initialized.")
        #     logger.warning("Please update your .env file with a valid PRIVATE_KEY")
        #     return
            
        try:
            self.client = FCTradingClient(
                settings.url,
                settings.consumer_id,
                settings.consumer_secret,
                settings.private_key,
                settings.two_fa_type
            )
            logger.info("FCTradingClient initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize FCTradingClient: {str(e)}")
            self.client = None
    
    def _ensure_client(self):
        """Ensure client is available before making requests"""
        if not SSI_AVAILABLE:
            logger.warning("SSI FC Trading library not available. Using mock mode.")
            return False
        if self.client is None:
            logger.warning("FCTradingClient is not initialized. Using mock mode.")
            return False
        return True
    
    def get_access_token(self) -> str:
        """Get current access token"""
        self._ensure_client()
        try:
            token = self.client.get_access_token()
            logger.info("Access token retrieved successfully")
            return token
        except Exception as e:
            logger.error(f"Error getting access token: {str(e)}")
            raise
    
    def get_otp(self) -> str:
        """Get OTP for 2FA"""
        if not self._ensure_client():
            # Mock OTP response
            return json.dumps({
                "success": True,
                "message": "OTP sent successfully (mock)",
                "data": {"mock": True}
            })
        
        try:
            fc_req = fcmodel_requests.GetOTP(settings.consumer_id, settings.consumer_secret)
            result = self.client.get_otp(fc_req)
            logger.info("OTP request sent successfully")
            return result
        except Exception as e:
            logger.error(f"Error getting OTP: {str(e)}")
            # Return mock response on error
            return json.dumps({
                "success": False,
                "message": f"Error getting OTP: {str(e)}",
                "mock": True
            })
    
    def verify_code(self, code: str) -> str:
        """Verify OTP or PIN code"""
        if not self._ensure_client():
            # Mock verification response
            return json.dumps({
                "success": True,
                "message": "Code verified successfully (mock)",
                "data": {
                    "accessToken": "mock_access_token",
                    "mock": True
                }
            })
        
        try:
            result = self.client.verifyCode(code)
            logger.info("Code verification completed")
            return result
        except Exception as e:
            logger.error(f"Error verifying code: {str(e)}")
            return json.dumps({
                "success": False,
                "message": f"Error verifying code: {str(e)}",
                "mock": True
            })
    
    def place_new_order(self, order_data: dict) -> str:
        """Place a new order"""
        if not self._ensure_client():
            # Mock order placement
            from datetime import datetime
            mock_result = {
                "success": True,
                "message": "Order placed successfully (mock)",
                "data": {
                    "order_id": f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "status": "PENDING",
                    "instrument_id": order_data.get("instrument_id"),
                    "price": order_data.get("price"),
                    "quantity": order_data.get("quantity"),
                    "buy_sell": order_data.get("buy_sell"),
                    "order_type": order_data.get("order_type"),
                    "timestamp": datetime.now().isoformat(),
                    "mock": True
                }
            }
            return json.dumps(mock_result)
        
        try:
            fc_req = fcmodel_requests.NewOrder(
                str(order_data["account"]).upper(),
                str(random.randint(0, 99999999)),
                str(order_data["instrument_id"]).upper(),
                str(order_data["market"]).upper(),
                str(order_data["buy_sell"]).upper(),
                str(order_data["order_type"]).upper(),
                float(order_data["price"]),
                int(order_data["quantity"]),
                bool(order_data.get("stop_order", False)),
                float(order_data.get("stop_price", 0)),
                str(order_data.get("stop_type", "")),
                float(order_data.get("stop_step", 0)),
                float(order_data.get("loss_step", 0)),
                float(order_data.get("profit_step", 0)),
                deviceId=str(order_data.get("device_id", FCTradingClient.get_deviceid())),
                userAgent=str(order_data.get("user_agent", FCTradingClient.get_user_agent()))
            )
            
            result = self.client.new_order(fc_req)
            logger.info(f"New order placed for {order_data['instrument_id']}")
            return result
        except Exception as e:
            logger.error(f"Error placing new order: {str(e)}")
            return json.dumps({
                "success": False,
                "message": f"Error placing order: {str(e)}",
                "mock": True
            })
    
    def place_derivative_order(self, order_data: dict) -> str:
        """Place a new derivative order"""
        self._ensure_client()
        try:
            fc_req = fcmodel_requests.NewOrder(
                str(order_data["account"]).upper(),
                str(random.randint(0, 99999999)),
                str(order_data["instrument_id"]).upper(),
                str(order_data["market"]).upper(),
                str(order_data["buy_sell"]).upper(),
                str(order_data["order_type"]).upper(),
                float(order_data["price"]),
                int(order_data["quantity"]),
                bool(order_data.get("stop_order", False)),
                float(order_data.get("stop_price", 0)),
                str(order_data.get("stop_type", "")),
                float(order_data.get("stop_step", 0)),
                float(order_data.get("loss_step", 0)),
                float(order_data.get("profit_step", 0)),
                deviceId=str(order_data.get("device_id", FCTradingClient.get_deviceid())),
                userAgent=str(order_data.get("user_agent", FCTradingClient.get_user_agent()))
            )
            
            result = self.client.der_new_order(fc_req)
            logger.info(f"New derivative order placed for {order_data['instrument_id']}")
            return result
        except Exception as e:
            logger.error(f"Error placing derivative order: {str(e)}")
            raise
    
    def modify_order(self, order_data: dict) -> str:
        """Modify an existing order"""
        try:
            fc_rq = fcmodel_requests.ModifyOrder(
                str(order_data["account"]),
                str(random.randint(0, 99999999)),
                str(order_data["order_id"]),
                str(order_data["market_id"]),
                str(order_data["instrument_id"]),
                float(order_data["price"]),
                int(order_data["quantity"]),
                str(order_data["buy_sell"]),
                str(order_data["order_type"]),
                deviceId=str(order_data.get("device_id", FCTradingClient.get_deviceid())),
                userAgent=str(order_data.get("user_agent", FCTradingClient.get_user_agent()))
            )
            
            result = self.client.modify_order(fc_rq)
            logger.info(f"Order {order_data['order_id']} modified")
            return result
        except Exception as e:
            logger.error(f"Error modifying order: {str(e)}")
            raise
    
    def modify_derivative_order(self, order_data: dict) -> str:
        """Modify an existing derivative order"""
        try:
            fc_rq = fcmodel_requests.ModifyOrder(
                str(order_data["account"]),
                str(random.randint(0, 99999999)),
                str(order_data["order_id"]),
                str(order_data["market_id"]),
                str(order_data["instrument_id"]),
                float(order_data["price"]),
                int(order_data["quantity"]),
                str(order_data["buy_sell"]),
                str(order_data["order_type"]),
                deviceId=str(order_data.get("device_id", FCTradingClient.get_deviceid())),
                userAgent=str(order_data.get("user_agent", FCTradingClient.get_user_agent()))
            )
            
            result = self.client.der_modify_order(fc_rq)
            logger.info(f"Derivative order {order_data['order_id']} modified")
            return result
        except Exception as e:
            logger.error(f"Error modifying derivative order: {str(e)}")
            raise
    
    def cancel_order(self, order_data: dict) -> str:
        """Cancel an order"""
        try:
            fc_rq = fcmodel_requests.CancelOrder(
                str(order_data["account"]),
                str(random.randint(0, 99999999)),
                str(order_data["order_id"]),
                str(order_data["market_id"]),
                str(order_data["instrument_id"]),
                str(order_data["buy_sell"]),
                deviceId=str(order_data.get("device_id", FCTradingClient.get_deviceid())),
                userAgent=str(order_data.get("user_agent", FCTradingClient.get_user_agent()))
            )
            
            result = self.client.cancle_order(fc_rq)
            logger.info(f"Order {order_data['order_id']} cancelled")
            return result
        except Exception as e:
            logger.error(f"Error cancelling order: {str(e)}")
            raise
    
    def cancel_derivative_order(self, order_data: dict) -> str:
        """Cancel a derivative order"""
        try:
            fc_rq = fcmodel_requests.CancelOrder(
                str(order_data["account"]),
                str(random.randint(0, 99999999)),
                str(order_data["order_id"]),
                str(order_data["market_id"]),
                str(order_data["instrument_id"]),
                str(order_data["buy_sell"]),
                deviceId=str(order_data.get("device_id", FCTradingClient.get_deviceid())),
                userAgent=str(order_data.get("user_agent", FCTradingClient.get_user_agent()))
            )
            
            result = self.client.der_cancle_order(fc_rq)
            logger.info(f"Derivative order {order_data['order_id']} cancelled")
            return result
        except Exception as e:
            logger.error(f"Error cancelling derivative order: {str(e)}")
            raise
    
    def get_stock_account_balance(self, account: str) -> str:
        """Get stock account balance"""
        if not self._ensure_client():
            # Mock account balance
            mock_balance = {
                "success": True,
                "message": "Account balance retrieved (mock)",
                "data": {
                    "account": account,
                    "accountBalance": 10000000.0,
                    "purchasingPower": 8000000.0,
                    "totalAssets": 15000000.0,
                    "securitiesValue": 5000000.0,
                    "availableCash": 8000000.0,
                    "currency": "VND",
                    "mock": True
                }
            }
            return json.dumps(mock_balance)
        
        try:
            fc_rq = fcmodel_requests.StockAccountBalance(str(account))
            result = self.client.get_stock_account_balance(fc_rq)
            logger.info(f"Stock balance retrieved for account {account}")
            return result
        except Exception as e:
            logger.error(f"Error getting stock balance: {str(e)}")
            return json.dumps({
                "success": False,
                "message": f"Error getting stock balance: {str(e)}",
                "mock": True
            })
    
    def get_derivative_account_balance(self, account: str) -> str:
        """Get derivative account balance"""
        try:
            fc_rq = fcmodel_requests.DerivativeAccountBalance(str(account))
            result = self.client.get_derivative_account_balance(fc_rq)
            logger.info(f"Derivative balance retrieved for account {account}")
            return result
        except Exception as e:
            logger.error(f"Error getting derivative balance: {str(e)}")
            raise
    
    def get_pp_mmr_account(self, account: str) -> str:
        """Get PP and MMR of account"""
        try:
            fc_rq = fcmodel_requests.PPMMRAccount(str(account))
            result = self.client.get_pp_mmr_account(fc_rq)
            logger.info(f"PP/MMR retrieved for account {account}")
            return result
        except Exception as e:
            logger.error(f"Error getting PP/MMR: {str(e)}")
            raise
    
    def get_stock_position(self, account: str) -> str:
        """Get stock position"""
        if not self._ensure_client():
            # Mock stock positions
            mock_positions = {
                "success": True,
                "message": "Stock positions retrieved (mock)",
                "data": [
                    {
                        "instrumentId": "VIC",
                        "totalQty": 100,
                        "sellableQty": 100,
                        "avgPrice": 65000,
                        "currentPrice": 67000,
                        "marketValue": 6700000,
                        "unrealizedPnL": 200000,
                        "unrealizedPnLPct": 3.08
                    },
                    {
                        "instrumentId": "VCB",
                        "totalQty": 50,
                        "sellableQty": 50,
                        "avgPrice": 88000,
                        "currentPrice": 85000,
                        "marketValue": 4250000,
                        "unrealizedPnL": -150000,
                        "unrealizedPnLPct": -3.41
                    }
                ],
                "mock": True
            }
            return json.dumps(mock_positions)
        
        try:
            fc_rq = fcmodel_requests.StockPosition(str(account))
            result = self.client.get_stock_position(fc_rq)
            logger.info(f"Stock position retrieved for account {account}")
            return result
        except Exception as e:
            logger.error(f"Error getting stock position: {str(e)}")
            return json.dumps({
                "success": False,
                "message": f"Error getting stock position: {str(e)}",
                "mock": True
            })
    
    def get_derivative_position(self, account: str, query_summary: bool = True) -> str:
        """Get derivative position"""
        try:
            fc_rq = fcmodel_requests.DerivativePosition(str(account), query_summary)
            result = self.client.get_derivative_position(fc_rq)
            logger.info(f"Derivative position retrieved for account {account}")
            return result
        except Exception as e:
            logger.error(f"Error getting derivative position: {str(e)}")
            raise
    
    def get_max_buy_qty(self, account: str, instrument_id: str, price: float) -> str:
        """Get maximum buy quantity"""
        try:
            fc_rq = fcmodel_requests.MaxBuyQty(str(account), str(instrument_id), float(price))
            result = self.client.get_max_buy_qty(fc_rq)
            logger.info(f"Max buy qty retrieved for {instrument_id}")
            return result
        except Exception as e:
            logger.error(f"Error getting max buy qty: {str(e)}")
            raise
    
    def get_max_sell_qty(self, account: str, instrument_id: str, price: float = 0) -> str:
        """Get maximum sell quantity"""
        try:
            fc_rq = fcmodel_requests.MaxSellQty(str(account), str(instrument_id), float(price))
            result = self.client.get_max_sell_qty(fc_rq)
            logger.info(f"Max sell qty retrieved for {instrument_id}")
            return result
        except Exception as e:
            logger.error(f"Error getting max sell qty: {str(e)}")
            raise
    
    def get_order_history(self, account: str, start_date: str, end_date: str) -> str:
        """Get order history"""
        try:
            fc_rq = fcmodel_requests.OrderHistory(str(account), str(start_date), str(end_date))
            result = self.client.get_order_history(fc_rq)
            logger.info(f"Order history retrieved for account {account}")
            return result
        except Exception as e:
            logger.error(f"Error getting order history: {str(e)}")
            raise
    
    def get_order_book(self, account: str) -> str:
        """Get order book"""
        if not self._ensure_client():
            # Mock order book
            from datetime import datetime
            mock_orders = {
                "success": True,
                "message": "Order book retrieved (mock)",
                "data": [
                    {
                        "orderId": "ORD001",
                        "instrumentId": "VIC",
                        "price": 65000,
                        "quantity": 100,
                        "filledQty": 0,
                        "buySell": "B",
                        "orderType": "LO",
                        "status": "PENDING",
                        "orderTime": datetime.now().isoformat()
                    },
                    {
                        "orderId": "ORD002",
                        "instrumentId": "VCB",
                        "price": 85000,
                        "quantity": 50,
                        "filledQty": 50,
                        "buySell": "S",
                        "orderType": "LO",
                        "status": "FILLED",
                        "orderTime": datetime.now().isoformat()
                    }
                ],
                "mock": True
            }
            return json.dumps(mock_orders)
        
        try:
            fc_rq = fcmodel_requests.OrderBook(str(account))
            result = self.client.get_order_book(fc_rq)
            logger.info(f"Order book retrieved for account {account}")
            return result
        except Exception as e:
            logger.error(f"Error getting order book: {str(e)}")
            return json.dumps({
                "success": False,
                "message": f"Error getting order book: {str(e)}",
                "mock": True
            })
    
    def get_audit_order_book(self, account: str) -> str:
        """Get audit order book"""
        try:
            fc_rq = fcmodel_requests.AuditOrderBook(str(account))
            result = self.client.get_audit_order_book(fc_rq)
            logger.info(f"Audit order book retrieved for account {account}")
            return result
        except Exception as e:
            logger.error(f"Error getting audit order book: {str(e)}")
            raise
    
    def get_rate_limit(self) -> str:
        """Get rate limit information"""
        try:
            result = self.client.get_ratelimit()
            logger.info("Rate limit information retrieved")
            return result
        except Exception as e:
            logger.error(f"Error getting rate limit: {str(e)}")
            raise


# Singleton instance
fc_trading_service = FCTradingService()
