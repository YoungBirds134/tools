"""
FC Data API client
"""
from typing import Dict, Any, Optional
from app.clients.base import BaseHTTPClient
from app.utils.cache import cache_manager, CacheKeys
from app.schemas.fc_data import *
from config import settings


class FCDataClient(BaseHTTPClient):
    """FC Data API client"""
    
    def __init__(self):
        super().__init__(
            base_url=settings.fc_data_url,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )
        self.consumer_id = settings.consumer_id_fc_data
        self.consumer_secret = settings.consumer_secret_fc_data
        self.private_key = settings.private_key_fc_data
        self.public_key = settings.public_key_fc_data
    
    async def _get_access_token(self) -> str:
        """Get access token with caching"""
        cache_key = CacheKeys.token_key("fc_data", self.consumer_id)
        
        # Try to get from cache first
        cached_token = await cache_manager.get(cache_key)
        if cached_token:
            self.log_debug("Using cached FC Data token", cache_key=cache_key)
            return cached_token
        
        # Request new token from SSI FastConnect Data API automatically
        endpoint = "api/v2/Market/AccessToken"
        self.log_info(
            "Requesting new FC Data access token",
            endpoint=endpoint,
            consumer_id=self.consumer_id
        )
        
        payload = {
            "consumerID": self.consumer_id,
            "consumerSecret": self.consumer_secret
        }
        
        try:
            # Call SSI FastConnect Data AccessToken API without auth headers
            # since this is the authentication endpoint itself
            data = await self.post(endpoint, json=payload)
            
            self.log_info(
                "FC Data access token response received",
                endpoint=endpoint,
                status=data.get("status"),
                message=data.get("message"),
                has_data=bool(data.get("data"))
            )
            
            if data.get("status") != 200:
                error_msg = data.get("message", "Unknown error")
                self.log_error("Failed to get FC Data access token", error=error_msg, status=data.get("status"))
                raise Exception(f"Authentication failed: {error_msg}")
            
            token_data = data.get("data", {})
            access_token = token_data.get("accessToken")
            
            if not access_token:
                self.log_error("No access token in response", response_data=data)
                raise Exception("No access token received from SSI")
            
            # Cache the token with 15 minutes TTL (as specified by SSI)
            ttl_seconds = 15 * 60  # 15 minutes
            await cache_manager.set(cache_key, access_token, ttl=ttl_seconds)
            
            self.log_info("FC Data access token obtained and cached", ttl_minutes=15)
            return access_token
            
        except Exception as e:
            self.log_error(
                "Failed to get FC Data access token", 
                endpoint=endpoint,
                error=str(e), 
                consumer_id=self.consumer_id
            )
            raise
    
    async def _get_auth_headers(self) -> Dict[str, str]:
        """Get authorization headers"""
        token = await self._get_access_token()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
    async def get_access_token(
        self, 
        request: FCDataAccessTokenRequest
    ) -> FCDataAccessTokenResponse:
        """Get FC Data access token directly (for public access)"""
        endpoint = "api/v2/Market/AccessToken"
        payload = {
            "consumerID": request.consumer_id,
            "consumerSecret": request.consumer_secret
        }
        
        self.log_info(
            "Requesting FC Data access token from SSI",
            endpoint=endpoint,
            consumer_id=request.consumer_id
        )
        
        try:
            # Call SSI FastConnect Data AccessToken API without auth headers
            # since this is the authentication endpoint itself
            data = await self.post(endpoint, json=payload)
            
            response = FCDataAccessTokenResponse(**data)
            
            self.log_info(
                "FC Data access token response received",
                endpoint=endpoint,
                status=response.status,
                message=response.message,
                has_token=bool(response.data and response.data.accessToken)
            )
            
            if response.status != 200:
                self.log_error("Failed to get FC Data access token", 
                             error=response.message, status=response.status)
                raise Exception(f"Authentication failed: {response.message}")
            
            return response
            
        except Exception as e:
            self.log_error(
                "Failed to get FC Data access token", 
                endpoint=endpoint,
                error=str(e), 
                consumer_id=request.consumer_id
            )
            raise

    async def get_securities_info(
        self, 
        request: GetSecuritiesInfoRequest
    ) -> GetSecuritiesInfoResponse:
        """Get securities information"""
        endpoint = "api/v2/Market/Securities"
        headers = await self._get_auth_headers()
        
        params = {
            "pageIndex": request.page_index,
            "pageSize": request.page_size
        }
        
        if request.market:
            params["market"] = request.market.value
        if request.symbol:
            params["symbol"] = request.symbol
        if request.ascending is not None:
            params["ascending"] = request.ascending
        
        # Check cache first
        cache_key = CacheKeys.master_data_key(
            "securities_info", 
            f"{request.market}_{request.symbol}_{request.page_index}_{request.page_size}"
        )
        
        cached_result = await cache_manager.get(cache_key)
        if cached_result:
            self.log_debug("Using cached securities info", cache_key=cache_key)
            return GetSecuritiesInfoResponse(**cached_result)

        self.log_info(
            "Requesting securities info from SSI",
            endpoint=endpoint,
            market=request.market,
            symbol=request.symbol,
            page_index=request.page_index,
            page_size=request.page_size
        )
        
        # Make API call
        try:
            data = await self.get(endpoint, params=params, headers=headers)
            response = GetSecuritiesInfoResponse(**data)
            
            self.log_info(
                "Securities info response received",
                endpoint=endpoint,
                status=response.status,
                message=response.message,
                total_records=response.totalRecord,
                data_count=len(response.data) if response.data else 0
            )
            
            # Cache the result
            await cache_manager.set(
                cache_key,
                response.model_dump(),
                ttl=settings.cache_ttl_master_data
            )
            
            return response
            
        except Exception as e:
            self.log_error("Failed to get securities info", error=str(e), params=params)
            raise
    
    async def get_daily_ohlc(
        self, 
        request: GetDailyOhlcRequest
    ) -> GetDailyOhlcResponse:
        """Get daily OHLC data"""
        headers = await self._get_auth_headers()
        
        params = {
            "pageIndex": request.page_index,
            "pageSize": request.page_size,
            "fromDate": request.from_date,
            "toDate": request.to_date
        }
        
        if request.symbol:
            params["symbol"] = request.symbol
        if request.market:
            params["market"] = request.market.value
        if request.ascending is not None:
            params["ascending"] = request.ascending
        
        # Cache key includes date range
        cache_key = CacheKeys.market_data_key(
            request.symbol or "ALL",
            request.market.value if request.market else "ALL",
            f"daily_ohlc_{request.from_date}_{request.to_date}_{request.page_index}_{request.page_size}"
        )
        
        cached_result = await cache_manager.get(cache_key)
        if cached_result:
            self.log_debug("Using cached daily OHLC", cache_key=cache_key)
            return GetDailyOhlcResponse(**cached_result)
        
        try:
            data = await self.get("api/v2/Market/DailyOhlc", params=params, headers=headers)
            self.log_info("Raw daily OHLC response", data=data)
            response = GetDailyOhlcResponse(**data)
            
            # Cache with shorter TTL for market data
            await cache_manager.set(
                cache_key,
                response.model_dump(),
                ttl=settings.cache_ttl_market_data
            )
            
            return response
            
        except Exception as e:
            self.log_error("Failed to get daily OHLC", error=str(e), params=params)
            raise
    
    async def get_intraday_ohlc(
        self, 
        request: GetIntradayOhlcRequest
    ) -> GetIntradayOhlcResponse:
        """Get intraday OHLC data"""
        headers = await self._get_auth_headers()
        
        params = {
            "pageIndex": request.page_index,
            "pageSize": request.page_size,
            "fromDate": request.from_date,
            "toDate": request.to_date
        }
        
        if request.symbol:
            params["symbol"] = request.symbol
        if request.resolution:
            params["resolution"] = request.resolution
        if request.ascending is not None:
            params["ascending"] = request.ascending
        
        try:
            data = await self.get("api/v2/Market/IntradayOhlc", params=params, headers=headers)
            self.log_info("Raw intraday OHLC response", data=data)
            return GetIntradayOhlcResponse(**data)
            
        except Exception as e:
            self.log_error("Failed to get intraday OHLC", error=str(e), params=params)
            raise
    
    async def get_daily_index(
        self, 
        request: GetDailyIndexRequest
    ) -> GetDailyIndexResponse:
        """Get daily index data"""
        headers = await self._get_auth_headers()
        
        params = {
            "pageIndex": request.page_index,
            "pageSize": request.page_size,
            "indexId": request.index_id,
            "fromDate": request.from_date,
            "toDate": request.to_date
        }
        
        if request.ascending is not None:
            params["ascending"] = request.ascending
        
        # Cache index data
        cache_key = CacheKeys.market_data_key(
            request.index_id,
            "INDEX",
            f"daily_{request.from_date}_{request.to_date}_{request.page_index}_{request.page_size}"
        )
        
        cached_result = await cache_manager.get(cache_key)
        if cached_result:
            self.log_debug("Using cached daily index", cache_key=cache_key)
            return GetDailyIndexResponse(**cached_result)
        
        try:
            data = await self.get("api/v2/Market/DailyIndex", params=params, headers=headers)
            self.log_info("Raw daily index response", data=data)
            response = GetDailyIndexResponse(**data)
            
            await cache_manager.set(
                cache_key,
                response.model_dump(),
                ttl=settings.cache_ttl_market_data
            )
            
            return response
            
        except Exception as e:
            self.log_error("Failed to get daily index", error=str(e), params=params)
            raise
    
    async def get_daily_stock_price(
        self, 
        request: GetDailyStockPriceRequest
    ) -> GetDailyStockPriceResponse:
        """Get daily stock price data"""
        headers = await self._get_auth_headers()
        
        params = {
            "pageIndex": request.page_index,
            "pageSize": request.page_size,
            "fromDate": request.from_date,
            "toDate": request.to_date
        }
        
        if request.symbol:
            params["symbol"] = request.symbol
        if request.market:
            params["market"] = request.market.value
        
        try:
            data = await self.get("api/v2/Market/DailyStockPrice", params=params, headers=headers)
            self.log_info("Raw daily stock price response", data=data)
            return GetDailyStockPriceResponse(**data)
            
        except Exception as e:
            self.log_error("Failed to get daily stock price", error=str(e), params=params)
            raise

    # Additional methods for comprehensive FC Data API support
    
    async def get_securities_details(
        self, 
        request: GetSecuritiesDetailsRequest
    ) -> GetSecuritiesDetailsResponse:
        """Get securities details"""
        headers = await self._get_auth_headers()
        
        params = {
            "symbol": request.symbol
        }
        
        if request.market:
            params["market"] = request.market.value
        
        try:
            data = await self.get("api/v2/Market/SecuritiesDetails", params=params, headers=headers)
            self.log_info("Raw securities details response", data=data)
            return GetSecuritiesDetailsResponse(**data)
            
        except Exception as e:
            self.log_error("Failed to get securities details", error=str(e), params=params)
            raise

    async def get_index_components(
        self, 
        request: GetIndexComponentsRequest
    ) -> GetIndexComponentsResponse:
        """Get index components"""
        headers = await self._get_auth_headers()
        
        params = {
            "indexId": request.index_id,
            "pageIndex": request.page_index,
            "pageSize": request.page_size
        }
        
        try:
            data = await self.get("api/v2/Market/IndexComponents", params=params, headers=headers)
            self.log_info("Raw index components response", data=data)
            return GetIndexComponentsResponse(**data)
            
        except Exception as e:
            self.log_error("Failed to get index components", error=str(e), params=params)
            raise

    async def get_index_list(
        self, 
        request: GetIndexListRequest
    ) -> GetIndexListResponse:
        """Get index list"""
        headers = await self._get_auth_headers()
        
        params = {
            "pageIndex": request.page_index,
            "pageSize": request.page_size
        }
        
        if request.market:
            params["market"] = request.market.value
        
        try:
            data = await self.get("api/v2/Market/IndexList", params=params, headers=headers)
            self.log_info("Raw index list response", data=data)
            return GetIndexListResponse(**data)
            
        except Exception as e:
            self.log_error("Failed to get index list", error=str(e), params=params)
            raise
