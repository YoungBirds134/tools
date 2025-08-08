"""
FC Data service layer
"""
from typing import List, Optional
from app.clients.fc_data import FCDataClient
from app.schemas.fc_data import *
from app.core.logging_config import LoggerMixin
from app.core.exceptions import SSIIntegrationError


class FCDataService(LoggerMixin):
    """FC Data service with business logic"""
    
    def __init__(self):
        self.client = FCDataClient()
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self.client.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.client.disconnect()
    
    async def get_access_token(
        self, 
        request: FCDataAccessTokenRequest
    ) -> FCDataAccessTokenResponse:
        """Get FC Data access token"""
        try:
            self.log_info("Getting FC Data access token", consumer_id=request.consumer_id)
            
            response = await self.client.get_access_token(request)
            
            self.log_info("FC Data access token obtained successfully")
            return response
            
        except Exception as e:
            self.log_error("Failed to get FC Data access token", error=str(e))
            raise SSIIntegrationError(f"FC Data authentication failed: {e}")

    async def get_securities_info(
        self, 
        request: GetSecuritiesInfoRequest
    ) -> GetSecuritiesInfoResponse:
        """Get securities information with business logic"""
        try:
            self.log_info(
                "Getting securities info",
                market=request.market,
                symbol=request.symbol,
                page=request.page_index,
                size=request.page_size
            )
            
            response = await self.client.get_securities_info(request)
            
            # Business logic: validate and enrich data
            if response.data:
                response.data = self._validate_securities_data(response.data)
            
            self.log_info(
                "Securities info retrieved",
                count=len(response.data) if response.data else 0,
                total_records=response.total_record
            )
            
            return response
            
        except Exception as e:
            self.log_error("Failed to get securities info", error=str(e))
            raise SSIIntegrationError(f"Securities info retrieval failed: {e}")
    
    async def get_daily_ohlc(
        self, 
        request: GetDailyOhlcRequest
    ) -> GetDailyOhlcResponse:
        """Get daily OHLC data with validation"""
        try:
            # Validate date range
            self._validate_date_range(request.from_date, request.to_date)
            
            self.log_info(
                "Getting daily OHLC",
                symbol=request.symbol,
                market=request.market,
                from_date=request.from_date,
                to_date=request.to_date
            )
            
            response = await self.client.get_daily_ohlc(request)
            
            # Business logic: validate OHLC data
            if response.data:
                response.data = self._validate_ohlc_data(response.data)
            
            self.log_info(
                "Daily OHLC retrieved",
                count=len(response.data) if response.data else 0
            )
            
            return response
            
        except Exception as e:
            self.log_error("Failed to get daily OHLC", error=str(e))
            raise SSIIntegrationError(f"Daily OHLC retrieval failed: {e}")
    
    async def get_intraday_ohlc(
        self, 
        request: GetIntradayOhlcRequest
    ) -> GetIntradayOhlcResponse:
        """Get intraday OHLC data"""
        try:
            # Validate date range
            self._validate_date_range(request.from_date, request.to_date)
            
            self.log_info(
                "Getting intraday OHLC",
                symbol=request.symbol,
                from_date=request.from_date,
                to_date=request.to_date,
                resolution=request.resolution
            )
            
            response = await self.client.get_intraday_ohlc(request)
            
            # Business logic: validate and sort data by time
            if response.data:
                response.data = self._validate_and_sort_intraday_data(response.data)
            
            self.log_info(
                "Intraday OHLC retrieved",
                count=len(response.data) if response.data else 0
            )
            
            return response
            
        except Exception as e:
            self.log_error("Failed to get intraday OHLC", error=str(e))
            raise SSIIntegrationError(f"Intraday OHLC retrieval failed: {e}")
    
    async def get_daily_index(
        self, 
        request: GetDailyIndexRequest
    ) -> GetDailyIndexResponse:
        """Get daily index data"""
        try:
            # Validate date range
            self._validate_date_range(request.from_date, request.to_date)
            
            self.log_info(
                "Getting daily index",
                index_id=request.index_id,
                from_date=request.from_date,
                to_date=request.to_date
            )
            
            response = await self.client.get_daily_index(request)
            
            # Business logic: validate index data
            if response.data:
                response.data = self._validate_index_data(response.data)
            
            self.log_info(
                "Daily index retrieved",
                count=len(response.data) if response.data else 0
            )
            
            return response
            
        except Exception as e:
            self.log_error("Failed to get daily index", error=str(e))
            raise SSIIntegrationError(f"Daily index retrieval failed: {e}")
    
    async def get_daily_stock_price(
        self, 
        request: GetDailyStockPriceRequest
    ) -> GetDailyStockPriceResponse:
        """Get daily stock price data"""
        try:
            # Validate date range
            self._validate_date_range(request.from_date, request.to_date)
            
            self.log_info(
                "Getting daily stock price",
                symbol=request.symbol,
                market=request.market,
                from_date=request.from_date,
                to_date=request.to_date
            )
            
            response = await self.client.get_daily_stock_price(request)
            
            # Business logic: validate and enrich stock price data
            if response.data:
                response.data = self._validate_stock_price_data(response.data)
            
            self.log_info(
                "Daily stock price retrieved",
                count=len(response.data) if response.data else 0
            )
            
            return response
            
        except Exception as e:
            self.log_error("Failed to get daily stock price", error=str(e))
            raise SSIIntegrationError(f"Daily stock price retrieval failed: {e}")
    
    def _validate_date_range(self, from_date: str, to_date: str) -> None:
        """Validate date range"""
        # Add date validation logic here
        # For now, just basic check
        if not from_date or not to_date:
            raise ValueError("Both from_date and to_date are required")
    
    def _validate_securities_data(self, data: List[SecurityInfo]) -> List[SecurityInfo]:
        """Validate and clean securities data"""
        validated_data = []
        for item in data:
            # Add validation logic here
            # For example, ensure symbol is uppercase
            if item.Symbol:
                item.Symbol = item.Symbol.upper()
            validated_data.append(item)
        return validated_data
    
    def _validate_ohlc_data(self, data: List[OhlcData]) -> List[OhlcData]:
        """Validate OHLC data"""
        validated_data = []
        for item in data:
            # Validate OHLC relationships
            if (item.open is not None and item.high is not None and 
                item.low is not None and item.close is not None):
                
                # Basic OHLC validation: High >= Open,Close and Low <= Open,Close
                if (item.high >= max(item.open, item.close) and 
                    item.low <= min(item.open, item.close)):
                    validated_data.append(item)
                else:
                    self.log_warning(
                        "Invalid OHLC data detected",
                        symbol=item.symbol,
                        date=item.trading_date,
                        ohlc=(item.open, item.high, item.low, item.close)
                    )
            else:
                validated_data.append(item)  # Keep data with null values
        
        return validated_data
    
    def _validate_and_sort_intraday_data(self, data: List[OhlcData]) -> List[OhlcData]:
        """Validate and sort intraday data by time"""
        validated_data = self._validate_ohlc_data(data)
        
        # Sort by trading date and time
        validated_data.sort(key=lambda x: (x.trading_date, x.time or ""))
        
        return validated_data
    
    def _validate_index_data(self, data: List[IndexData]) -> List[IndexData]:
        """Validate index data"""
        validated_data = []
        for item in data:
            # Validate index calculations
            if item.index_value is not None and item.index_value > 0:
                validated_data.append(item)
            elif item.index_value is None:
                validated_data.append(item)  # Keep null values
            else:
                self.log_warning(
                    "Invalid index value detected",
                    index_code=item.index_code,
                    date=item.trading_date,
                    value=item.index_value
                )
        
        return validated_data
    
    def _validate_stock_price_data(self, data: List[StockPriceData]) -> List[StockPriceData]:
        """Validate stock price data"""
        validated_data = []
        for item in data:
            # Validate price relationships
            if (item.close_price is not None and item.ref_price is not None and
                item.ceiling_price is not None and item.floor_price is not None):
                
                # Check if close price is within ceiling/floor range
                if item.floor_price <= item.close_price <= item.ceiling_price:
                    validated_data.append(item)
                else:
                    self.log_warning(
                        "Price out of range detected",
                        symbol=item.symbol,
                        date=item.trading_date,
                        close=item.close_price,
                        floor=item.floor_price,
                        ceiling=item.ceiling_price
                    )
            else:
                validated_data.append(item)  # Keep data with null values
        
        return validated_data

    # Additional methods for comprehensive FC Data API support
    
    async def get_securities_details(
        self, 
        request: GetSecuritiesDetailsRequest
    ) -> GetSecuritiesDetailsResponse:
        """Get securities details"""
        try:
            self.log_info(
                "Getting securities details",
                symbol=request.symbol,
                market=request.market
            )
            
            response = await self.client.get_securities_details(request)
            
            self.log_info("Securities details retrieved")
            return response
            
        except Exception as e:
            self.log_error("Failed to get securities details", error=str(e))
            raise SSIIntegrationError(f"Securities details retrieval failed: {e}")

    async def get_index_components(
        self, 
        request: GetIndexComponentsRequest
    ) -> GetIndexComponentsResponse:
        """Get index components"""
        try:
            self.log_info(
                "Getting index components",
                index_id=request.index_id,
                page=request.page_index,
                size=request.page_size
            )
            
            response = await self.client.get_index_components(request)
            
            self.log_info(
                "Index components retrieved",
                count=len(response.data) if response.data else 0
            )
            
            return response
            
        except Exception as e:
            self.log_error("Failed to get index components", error=str(e))
            raise SSIIntegrationError(f"Index components retrieval failed: {e}")

    async def get_index_list(
        self, 
        request: GetIndexListRequest
    ) -> GetIndexListResponse:
        """Get index list"""
        try:
            self.log_info(
                "Getting index list",
                market=request.market,
                page=request.page_index,
                size=request.page_size
            )
            
            response = await self.client.get_index_list(request)
            
            self.log_info(
                "Index list retrieved",
                count=len(response.data) if response.data else 0
            )
            
            return response
            
        except Exception as e:
            self.log_error("Failed to get index list", error=str(e))
            raise SSIIntegrationError(f"Index list retrieval failed: {e}")
