"""
FC Trading service layer
"""
from typing import List, Optional
from decimal import Decimal
from app.clients.fc_trading import FCTradingClient
from app.schemas.fc_trading import *
from app.core.logging_config import LoggerMixin
from app.core.exceptions import SSIIntegrationError, SSIValidationError
from app.core.auth_middleware import SSIServiceAuth


class FCTradingService(LoggerMixin):
    """FC Trading service with business logic"""
    
    def __init__(self, access_token: Optional[str] = None):
        self.client = FCTradingClient(access_token=access_token)
        self.access_token = access_token
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self.client.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.client.disconnect()
    
    async def authenticate(
        self, 
        request: AccessTokenRequest
    ) -> AccessTokenResponse:
        """Authenticate and get access token"""
        try:
            self.log_info(
                "Authenticating user",
                consumer_id=request.consumer_id,
                two_factor_type=request.two_factor_type,
                is_save=request.is_save
            )
            
            response = await self.client.get_access_token(request)
            
            if response.status == 200 or response.status == "Success":
                self.log_info("Authentication successful")
                
                # Cache the access token if successful
                if response.data and response.data.token:
                    await SSIServiceAuth.get_or_cache_token(
                        consumer_id=request.consumer_id,
                        consumer_secret=request.consumer_secret,
                        access_token=response.data.token,  # Use the property to get actual token
                        cache_duration_minutes=30  # SSI tokens typically last 30 minutes
                    )
                    self.log_info("Access token cached successfully")
            else:
                self.log_warning("Authentication failed", response=response)
            
            return response
            
        except Exception as e:
            self.log_error("Authentication failed", error=str(e))
            raise SSIIntegrationError(f"Authentication failed: {e}")
    
    async def request_otp(self, request: GetOTPRequest) -> GetOTPResponse:
        """Request OTP for 2FA"""
        try:
            self.log_info("Requesting OTP", consumer_id=request.consumer_id)
            
            response = await self.client.get_otp(request)
            
            self.log_info("OTP request processed", status=response.status)
            return response
            
        except Exception as e:
            self.log_error("OTP request failed", error=str(e))
            raise SSIIntegrationError(f"OTP request failed: {e}")
    
    async def place_order(self, request: NewOrderRequest) -> NewOrderResponse:
        """Place new order with validation"""
        try:
            # Validate order before placing
            self._validate_order_request(request)
            
            self.log_info(
                "Placing order",
                account=request.account,
                symbol=request.instrument_id,
                side=request.buy_sell.value,
                quantity=request.quantity,
                price=request.price,
                order_type=request.order_type.value
            )
            
            response = await self.client.new_order(request)
            
            if response.status == 200 or response.status == "Success":
                self.log_info(
                    "Order placed successfully",
                    order_id=response.data.order_id if response.data else None
                )
            else:
                self.log_warning("Order placement failed", response=response)
            
            return response
            
        except Exception as e:
            self.log_error("Order placement failed", error=str(e))
            raise SSIIntegrationError(f"Order placement failed: {e}")
    
    async def modify_order(self, request: ModifyOrderRequest) -> ModifyOrderResponse:
        """Modify existing order with validation"""
        try:
            # Validate modification request
            self._validate_modify_request(request)
            
            self.log_info(
                "Modifying order",
                account=request.account,
                order_id=request.order_id,
                symbol=request.instrument_id,
                new_price=request.price,
                new_quantity=request.quantity
            )
            
            response = await self.client.modify_order(request)
            
            if response.status == 200 or response.status == "Success":
                self.log_info("Order modified successfully")
            else:
                self.log_warning("Order modification failed", response=response)
            
            return response
            
        except Exception as e:
            self.log_error("Order modification failed", error=str(e))
            raise SSIIntegrationError(f"Order modification failed: {e}")
    
    async def cancel_order(self, request: CancelOrderRequest) -> CancelOrderResponse:
        """Cancel existing order"""
        try:
            self.log_info(
                "Cancelling order",
                account=request.account,
                order_id=request.order_id,
                symbol=request.instrument_id
            )
            
            response = await self.client.cancel_order(request)
            
            if response.status == 200 or response.status == "Success":
                self.log_info("Order cancelled successfully")
            else:
                self.log_warning("Order cancellation failed", response=response)
            
            return response
            
        except Exception as e:
            self.log_error("Order cancellation failed", error=str(e))
            raise SSIIntegrationError(f"Order cancellation failed: {e}")
    
    async def get_orders(self, request: OrderBookRequest) -> OrderBookResponse:
        """Get current orders"""
        try:
            self.log_info("Getting order book", account=request.account)
            
            response = await self.client.get_order_book(request)
            
            # Business logic: filter and sort orders
            if response.data:
                response.data = self._process_order_data(response.data)
            
            self.log_info(
                "Order book retrieved",
                count=len(response.data) if response.data else 0
            )
            
            return response
            
        except Exception as e:
            self.log_error("Failed to get order book", error=str(e))
            raise SSIIntegrationError(f"Order book retrieval failed: {e}")
    
    async def get_order_history(
        self, 
        request: OrderHistoryRequest
    ) -> OrderHistoryResponse:
        """Get order history"""
        try:
            # Validate date range
            self._validate_date_range(request.start_date, request.end_date)
            
            self.log_info(
                "Getting order history",
                account=request.account,
                start_date=request.start_date,
                end_date=request.end_date
            )
            
            response = await self.client.get_order_history(request)
            
            # Business logic: process historical data if exists
            # Note: SSI API returns data in different format, so we handle it as raw dict
            self.log_info(
                "Order history retrieved",
                has_data=bool(response.data)
            )
            
            return response
            
        except Exception as e:
            self.log_error("Failed to get order history", error=str(e))
            raise SSIIntegrationError(f"Order history retrieval failed: {e}")
    
    async def get_account_balance(
        self, 
        request: CashAccountBalanceRequest
    ) -> CashAccountBalanceResponse:
        """Get account cash balance"""
        try:
            self.log_info("Getting account balance", account=request.account)
            
            response = await self.client.get_cash_account_balance(request)
            
            # Business logic: validate balance data
            if response.data:
                self._validate_balance_data(response.data)
            
            self.log_info("Account balance retrieved")
            return response
            
        except Exception as e:
            self.log_error("Failed to get account balance", error=str(e))
            raise SSIIntegrationError(f"Account balance retrieval failed: {e}")
    
    async def get_positions(
        self, 
        request: StockPositionRequest
    ) -> StockPositionResponse:
        """Get stock positions"""
        try:
            self.log_info("Getting stock positions", account=request.account)
            
            response = await self.client.get_stock_position(request)
            
            # Business logic: calculate total portfolio value
            if response.data:
                response.data = self._enrich_position_data(response.data)
            
            self.log_info(
                "Stock positions retrieved",
                count=len(response.data) if response.data else 0
            )
            
            return response
            
        except Exception as e:
            self.log_error("Failed to get stock positions", error=str(e))
            raise SSIIntegrationError(f"Stock positions retrieval failed: {e}")
    
    async def get_buying_power(
        self, 
        request: MaxBuyQtyRequest
    ) -> MaxBuyQtyResponse:
        """Get maximum buying power"""
        try:
            # Validate price
            if request.price <= 0:
                raise SSIValidationError("Price must be greater than 0")
            
            self.log_info(
                "Getting max buy quantity",
                account=request.account,
                symbol=request.instrument_id,
                price=request.price
            )
            
            response = await self.client.get_max_buy_qty(request)
            
            self.log_info(
                "Max buy quantity retrieved",
                max_qty=response.data if response.data else 0
            )
            
            return response
            
        except Exception as e:
            self.log_error("Failed to get max buy quantity", error=str(e))
            raise SSIIntegrationError(f"Max buy quantity retrieval failed: {e}")
    
    async def get_selling_power(
        self, 
        request: MaxSellQtyRequest
    ) -> MaxSellQtyResponse:
        """Get maximum selling power"""
        try:
            self.log_info(
                "Getting max sell quantity",
                account=request.account,
                symbol=request.instrument_id
            )
            
            response = await self.client.get_max_sell_qty(request)
            
            self.log_info(
                "Max sell quantity retrieved",
                max_qty=response.data if response.data else 0
            )
            
            return response
            
        except Exception as e:
            self.log_error("Failed to get max sell quantity", error=str(e))
            raise SSIIntegrationError(f"Max sell quantity retrieval failed: {e}")
    
    def _validate_order_request(self, request: NewOrderRequest) -> None:
        """Validate order request"""
        # Price validation
        if request.price < 0:
            raise SSIValidationError("Price cannot be negative")
        
        # Quantity validation
        if request.quantity <= 0:
            raise SSIValidationError("Quantity must be greater than 0")
        
        # Market-specific validations
        if request.market == Market.VN:
            # Stock market validations
            if request.quantity % 100 != 0:
                raise SSIValidationError("Stock quantity must be in lots of 100")
        
        # Stop order validations
        if request.stop_order:
            if not request.stop_price or request.stop_price <= 0:
                raise SSIValidationError("Stop price required for stop orders")
    
    def _validate_modify_request(self, request: ModifyOrderRequest) -> None:
        """Validate order modification request"""
        if not request.order_id:
            raise SSIValidationError("Order ID is required for modification")
        
        if request.price < 0:
            raise SSIValidationError("Price cannot be negative")
        
        if request.quantity <= 0:
            raise SSIValidationError("Quantity must be greater than 0")
    
    def _validate_date_range(self, start_date: str, end_date: str) -> None:
        """Validate date range"""
        if not start_date or not end_date:
            raise SSIValidationError("Both start_date and end_date are required")
        
        # Add more sophisticated date validation here if needed
    
    def _process_order_data(self, orders: List[OrderData]) -> List[OrderData]:
        """Process and sort order data"""
        # Sort by input time descending (newest first)
        return sorted(
            orders, 
            key=lambda x: x.input_time or "", 
            reverse=True
        )
    
    def _process_historical_orders(self, orders: List[OrderData]) -> List[OrderData]:
        """Process historical order data"""
        # Sort by modified time descending
        return sorted(
            orders, 
            key=lambda x: x.modified_time or x.input_time or "", 
            reverse=True
        )
    
    def _validate_balance_data(self, balance: CashAccountBalance) -> None:
        """Validate balance data consistency"""
        # Add business logic to validate balance relationships
        if balance.cash_balance is not None and balance.available_cash is not None:
            if balance.available_cash > balance.cash_balance:
                self.log_warning(
                    "Available cash exceeds total cash balance",
                    account=balance.account,
                    cash_balance=balance.cash_balance,
                    available_cash=balance.available_cash
                )
    
    def _enrich_position_data(self, positions: List[StockPosition]) -> List[StockPosition]:
        """Enrich position data with calculations"""
        total_market_value = Decimal('0')
        
        for position in positions:
            if position.market_value:
                total_market_value += position.market_value
        
        self.log_info(
            "Portfolio summary calculated",
            total_positions=len(positions),
            total_market_value=total_market_value
        )
        
        return positions


    # Additional Account Information Methods
    async def get_audit_order_book(
        self, 
        request: AuditOrderBookRequest
    ) -> AuditOrderBookResponse:
        """Get audit order book"""
        try:
            self.log_info("Getting audit order book", account=request.account)
            
            response = await self.client.get_audit_order_book(request)
            
            if response.data:
                # Apply business logic and enrichment
                response.data = self._sort_orders_by_time(response.data)
            
            return response
            
        except Exception as e:
            self.log_error("Failed to get audit order book", error=str(e))
            raise SSIIntegrationError(f"Failed to get audit order book: {str(e)}")

    async def get_deriv_account_balance(
        self, 
        request: DerivAccountBalanceRequest
    ) -> DerivAccountBalanceResponse:
        """Get derivative account balance"""
        try:
            self.log_info("Getting derivative account balance", account=request.account)
            
            response = await self.client.get_deriv_account_balance(request)
            
            return response
            
        except Exception as e:
            self.log_error("Failed to get derivative account balance", error=str(e))
            raise SSIIntegrationError(f"Failed to get derivative account balance: {str(e)}")

    async def get_ppmmr_account(
        self, 
        request: PPMMRAccountRequest
    ) -> PPMMRAccountResponse:
        """Get PPMMR account information"""
        try:
            self.log_info("Getting PPMMR account info", account=request.account)
            
            response = await self.client.get_ppmmr_account(request)
            
            return response
            
        except Exception as e:
            self.log_error("Failed to get PPMMR account info", error=str(e))
            raise SSIIntegrationError(f"Failed to get PPMMR account info: {str(e)}")

    async def get_deriv_position(
        self, 
        request: DerivPositionRequest
    ) -> DerivPositionResponse:
        """Get derivative position"""
        try:
            self.log_info("Getting derivative position", account=request.account)
            
            response = await self.client.get_deriv_position(request)
            
            return response
            
        except Exception as e:
            self.log_error("Failed to get derivative position", error=str(e))
            raise SSIIntegrationError(f"Failed to get derivative position: {str(e)}")

    async def get_rate_limit(
        self, 
        request: RateLimitRequest
    ) -> RateLimitResponse:
        """Get rate limit information"""
        try:
            self.log_info("Getting rate limit info", account=request.account)
            
            response = await self.client.get_rate_limit(request)
            
            return response
            
        except Exception as e:
            self.log_error("Failed to get rate limit info", error=str(e))
            raise SSIIntegrationError(f"Failed to get rate limit info: {str(e)}")

    # Derivative Trading Methods
    async def place_deriv_order(
        self, 
        request: DerivNewOrderRequest
    ) -> DerivNewOrderResponse:
        """Place new derivative order"""
        try:
            self.log_info(
                "Placing derivative order",
                account=request.account,
                instrument_id=request.instrument_id,
                side=request.buy_sell,
                price=request.price,
                quantity=request.quantity
            )
            
            response_data = await self.client.place_deriv_order(request)
            
            # Create proper response object
            response = DerivNewOrderResponse(
                status=response_data.get('status', 200),
                message=response_data.get('message', 'Success'),
                data=response_data.get('data', {})
            )
            
            if response.status == 200 or response.status == "Success":
                self.log_info("Derivative order placed successfully", order_data=response.data)
            else:
                self.log_warning("Failed to place derivative order", response=response)
            
            return response
            
        except Exception as e:
            self.log_error("Failed to place derivative order", error=str(e))
            raise SSIIntegrationError(f"Failed to place derivative order: {str(e)}")

    async def cancel_deriv_order(
        self, 
        request: DerivCancelOrderRequest
    ) -> DerivCancelOrderResponse:
        """Cancel derivative order"""
        try:
            self.log_info(
                "Cancelling derivative order",
                account=request.account,
                order_id=request.order_id,
                instrument_id=request.instrument_id
            )
            
            response = await self.client.cancel_deriv_order(request)
            
            return response
            
        except Exception as e:
            self.log_error("Failed to cancel derivative order", error=str(e))
            raise SSIIntegrationError(f"Failed to cancel derivative order: {str(e)}")

    async def modify_deriv_order(
        self, 
        request: DerivModifyOrderRequest
    ) -> DerivModifyOrderResponse:
        """Modify derivative order"""
        try:
            self.log_info(
                "Modifying derivative order",
                account=request.account,
                order_id=request.order_id,
                new_price=request.price,
                new_quantity=request.quantity
            )
            
            response = await self.client.modify_deriv_order(request)
            
            return response
            
        except Exception as e:
            self.log_error("Failed to modify derivative order", error=str(e))
            raise SSIIntegrationError(f"Failed to modify derivative order: {str(e)}")

    async def get_portfolio(
        self, 
        request: StockPositionRequest
    ) -> StockPositionResponse:
        """Get portfolio (alias for get_positions)"""
        try:
            self.log_info("Getting portfolio", account=request.account)
            
            # Use existing get_positions method
            response = await self.get_positions(request)
            
            return response
            
        except Exception as e:
            self.log_error("Failed to get portfolio", error=str(e))
            raise SSIIntegrationError(f"Portfolio retrieval failed: {e}")

    # Helper methods
    def _sort_orders_by_time(self, orders):
        """Sort orders by time"""
        if not orders:
            return orders
        
        # Sort by input_time descending (newest first)  
        def get_time(order):
            if hasattr(order, 'input_time'):
                return order.input_time or ''
            elif isinstance(order, dict):
                return order.get('input_time', '') or order.get('modified_time', '')
            else:
                return ''
        
        return sorted(orders, key=get_time, reverse=True)
