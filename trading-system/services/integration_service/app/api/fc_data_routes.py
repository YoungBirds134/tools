"""
FC Data API routes
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import Optional
from app.services.fc_data_service import FCDataService
from app.schemas.fc_data import *
from app.schemas.base import ErrorResponse
from app.core.exceptions import (
    SSIIntegrationError, ssi_integration_error_to_http_exception,
    SSIAPIError, ssi_api_error_to_http_exception
)

router = APIRouter(prefix="/fc-data", tags=["FC Data"])


async def get_fc_data_service() -> FCDataService:
    """Dependency to get FC Data service"""
    service = FCDataService()
    try:
        await service.__aenter__()
        yield service
    finally:
        await service.__aexit__(None, None, None)


@router.post(
    "/access-token",
    response_model=FCDataAccessTokenResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Get FC Data Access Token",
    description="Obtain access token for FC Data APIs"
)
async def get_fc_data_access_token(
    request: FCDataAccessTokenRequest,
    service: FCDataService = Depends(get_fc_data_service)
) -> FCDataAccessTokenResponse:
    """Get FC Data access token"""
    try:
        return await service.get_access_token(request)
    
    except SSIAPIError as e:
        raise ssi_api_error_to_http_exception(e)
    except SSIIntegrationError as e:
        raise ssi_integration_error_to_http_exception(e)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal server error", "error": str(e)}
        )


@router.get(
    "/securities",
    response_model=GetSecuritiesInfoResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Get Securities Information",
    description="Retrieve information about securities/stocks with optional filtering"
)
async def get_securities_info(
    page_index: int = Query(1, ge=1, le=10, description="Page index (1-10)"),
    page_size: int = Query(10, ge=10, le=1000, description="Page size (10, 20, 50, 100, 1000)"),
    market: Optional[Market] = Query(None, description="Market filter"),
    symbol: Optional[str] = Query(None, max_length=10, description="Symbol filter"),
    ascending: Optional[bool] = Query(None, description="Sort order"),
    service: FCDataService = Depends(get_fc_data_service)
) -> GetSecuritiesInfoResponse:
    """Get securities information"""
    try:
        request = GetSecuritiesInfoRequest(
            page_index=page_index,
            page_size=page_size,
            market=market,
            symbol=symbol,
            ascending=ascending
        )
        return await service.get_securities_info(request)
    
    except SSIAPIError as e:
        raise ssi_api_error_to_http_exception(e)
    except SSIIntegrationError as e:
        raise ssi_integration_error_to_http_exception(e)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal server error", "error": str(e)}
        )


@router.get(
    "/securities-details",
    response_model=GetSecuritiesDetailsResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Get Securities Details",
    description="Retrieve detailed information about a specific security"
)
async def get_securities_details(
    symbol: str = Query(..., max_length=10, description="Stock symbol"),
    market: Optional[Market] = Query(None, description="Market"),
    service: FCDataService = Depends(get_fc_data_service)
) -> GetSecuritiesDetailsResponse:
    """Get securities details"""
    try:
        request = GetSecuritiesDetailsRequest(
            symbol=symbol,
            market=market
        )
        return await service.get_securities_details(request)
    
    except SSIAPIError as e:
        raise ssi_api_error_to_http_exception(e)
    except SSIIntegrationError as e:
        raise ssi_integration_error_to_http_exception(e)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal server error", "error": str(e)}
        )


@router.get(
    "/index-components",
    response_model=GetIndexComponentsResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Get Index Components",
    description="Retrieve components of a specific index"
)
async def get_index_components(
    index_id: str = Query(..., description="Index ID"),
    page_index: int = Query(1, ge=1, le=10, description="Page index (1-10)"),
    page_size: int = Query(10, ge=10, le=1000, description="Page size (10, 20, 50, 100, 1000)"),
    ascending: Optional[bool] = Query(None, description="Sort order"),
    service: FCDataService = Depends(get_fc_data_service)
) -> GetIndexComponentsResponse:
    """Get index components"""
    try:
        request = GetIndexComponentsRequest(
            index_id=index_id,
            page_index=page_index,
            page_size=page_size,
            ascending=ascending
        )
        return await service.get_index_components(request)
    
    except SSIAPIError as e:
        raise ssi_api_error_to_http_exception(e)
    except SSIIntegrationError as e:
        raise ssi_integration_error_to_http_exception(e)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal server error", "error": str(e)}
        )


@router.get(
    "/index-list",
    response_model=GetIndexListResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Get Index List",
    description="Retrieve list of available indices"
)
async def get_index_list(
    page_index: int = Query(1, ge=1, le=10, description="Page index (1-10)"),
    page_size: int = Query(10, ge=10, le=1000, description="Page size (10, 20, 50, 100, 1000)"),
    market: Optional[Market] = Query(None, description="Market filter"),
    ascending: Optional[bool] = Query(None, description="Sort order"),
    service: FCDataService = Depends(get_fc_data_service)
) -> GetIndexListResponse:
    """Get index list"""
    try:
        request = GetIndexListRequest(
            page_index=page_index,
            page_size=page_size,
            market=market,
            ascending=ascending
        )
        return await service.get_index_list(request)
    
    except SSIAPIError as e:
        raise ssi_api_error_to_http_exception(e)
    except SSIIntegrationError as e:
        raise ssi_integration_error_to_http_exception(e)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal server error", "error": str(e)}
        )


@router.get(
    "/daily-ohlc",
    response_model=GetDailyOhlcResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Get Daily OHLC Data",
    description="Retrieve daily Open, High, Low, Close data for securities"
)
async def get_daily_ohlc(
    from_date: str = Query(..., description="Start date (dd/mm/yyyy)"),
    to_date: str = Query(..., description="End date (dd/mm/yyyy)"),
    page_index: int = Query(1, ge=1, le=10, description="Page index (1-10)"),
    page_size: int = Query(10, ge=10, le=1000, description="Page size (10, 20, 50, 100, 1000)"),
    symbol: Optional[str] = Query(None, max_length=10, description="Stock symbol"),
    market: Optional[Market] = Query(None, description="Market"),
    ascending: Optional[bool] = Query(None, description="Sort order"),
    service: FCDataService = Depends(get_fc_data_service)
) -> GetDailyOhlcResponse:
    """Get daily OHLC data"""
    try:
        request = GetDailyOhlcRequest(
            from_date=from_date,
            to_date=to_date,
            page_index=page_index,
            page_size=page_size,
            symbol=symbol,
            market=market,
            ascending=ascending
        )
        return await service.get_daily_ohlc(request)
    
    except SSIAPIError as e:
        raise ssi_api_error_to_http_exception(e)
    except SSIIntegrationError as e:
        raise ssi_integration_error_to_http_exception(e)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal server error", "error": str(e)}
        )


@router.get(
    "/intraday-ohlc",
    response_model=GetIntradayOhlcResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Get Intraday OHLC Data",
    description="Retrieve intraday OHLC data with minute-level resolution"
)
async def get_intraday_ohlc(
    from_date: str = Query(..., description="Start date (dd/mm/yyyy)"),
    to_date: str = Query(..., description="End date (dd/mm/yyyy)"),
    page_index: int = Query(1, ge=1, le=10, description="Page index (1-10)"),
    page_size: int = Query(10, ge=10, le=1000, description="Page size (10, 20, 50, 100, 1000)"),
    symbol: Optional[str] = Query(None, max_length=10, description="Stock symbol"),
    resolution: Optional[int] = Query(1, ge=1, description="Resolution in minutes"),
    ascending: Optional[bool] = Query(None, description="Sort order"),
    service: FCDataService = Depends(get_fc_data_service)
) -> GetIntradayOhlcResponse:
    """Get intraday OHLC data"""
    try:
        request = GetIntradayOhlcRequest(
            from_date=from_date,
            to_date=to_date,
            page_index=page_index,
            page_size=page_size,
            symbol=symbol,
            resolution=resolution,
            ascending=ascending
        )
        return await service.get_intraday_ohlc(request)
    
    except SSIAPIError as e:
        raise ssi_api_error_to_http_exception(e)
    except SSIIntegrationError as e:
        raise ssi_integration_error_to_http_exception(e)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal server error", "error": str(e)}
        )


@router.get(
    "/daily-index",
    response_model=GetDailyIndexResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Get Daily Index Data",
    description="Retrieve daily index/market indicator data"
)
async def get_daily_index(
    index_id: str = Query(..., description="Index ID"),
    from_date: str = Query(..., description="Start date (dd/mm/yyyy)"),
    to_date: str = Query(..., description="End date (dd/mm/yyyy)"),
    page_index: int = Query(1, ge=1, le=10, description="Page index (1-10)"),
    page_size: int = Query(10, ge=10, le=1000, description="Page size (10, 20, 50, 100, 1000)"),
    ascending: Optional[bool] = Query(None, description="Sort order"),
    service: FCDataService = Depends(get_fc_data_service)
) -> GetDailyIndexResponse:
    """Get daily index data"""
    try:
        request = GetDailyIndexRequest(
            index_id=index_id,
            from_date=from_date,
            to_date=to_date,
            page_index=page_index,
            page_size=page_size,
            ascending=ascending
        )
        return await service.get_daily_index(request)
    
    except SSIAPIError as e:
        raise ssi_api_error_to_http_exception(e)
    except SSIIntegrationError as e:
        raise ssi_integration_error_to_http_exception(e)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal server error", "error": str(e)}
        )


@router.get(
    "/daily-stock-price",
    response_model=GetDailyStockPriceResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Get Daily Stock Price Data",
    description="Retrieve comprehensive daily stock price information including foreign trading data"
)
async def get_daily_stock_price(
    from_date: str = Query(..., description="Start date (dd/mm/yyyy)"),
    to_date: str = Query(..., description="End date (dd/mm/yyyy)"),
    page_index: int = Query(1, ge=1, le=10, description="Page index (1-10)"),
    page_size: int = Query(10, ge=10, le=1000, description="Page size (10, 20, 50, 100, 1000)"),
    symbol: Optional[str] = Query(None, max_length=10, description="Stock symbol"),
    market: Optional[Market] = Query(None, description="Market"),
    service: FCDataService = Depends(get_fc_data_service)
) -> GetDailyStockPriceResponse:
    """Get daily stock price data"""
    try:
        request = GetDailyStockPriceRequest(
            from_date=from_date,
            to_date=to_date,
            page_index=page_index,
            page_size=page_size,
            symbol=symbol,
            market=market
        )
        return await service.get_daily_stock_price(request)
    
    except SSIAPIError as e:
        raise ssi_api_error_to_http_exception(e)
    except SSIIntegrationError as e:
        raise ssi_integration_error_to_http_exception(e)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal server error", "error": str(e)}
        )
