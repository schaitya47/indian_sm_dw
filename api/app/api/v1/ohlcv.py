"""
OHLCV (Price and Volume) API endpoints.
"""

from typing import Optional
from datetime import date, datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db import get_db
from app.services import ohlcv_service
from app.schemas import DateRangeQuery, PaginationQuery, PaginatedResponse
from app.utils import cached
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ohlcv", tags=["ohlcv"])


@router.get("/{symbol}")
async def get_ohlcv_data(
    symbol: str,
    start_date: Optional[date] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date (YYYY-MM-DD)"),
    source: Optional[str] = Query(None, description="Data source filter"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=1000, description="Page size"),
    db: Session = Depends(get_db)
):
    """
    Get OHLCV (Open, High, Low, Close, Volume) data for a stock.
    
    - **symbol**: Stock symbol (e.g., 'TCS', 'RELIANCE')
    - **start_date**: Start date for data range (optional)
    - **end_date**: End date for data range (optional)
    - **source**: Filter by data source (e.g., 'NSE', 'YFIN', 'TICK')
    - **page**: Page number for pagination
    - **page_size**: Number of records per page
    
    Returns paginated OHLCV data with metadata.
    """
    try:
        # Set default date range if not provided
        if not end_date:
            end_date = datetime.now().date()
        if not start_date:
            start_date = end_date - timedelta(days=30)  # Default 30 days
        
        date_range = DateRangeQuery(start_date=start_date, end_date=end_date)
        pagination = PaginationQuery(page=page, page_size=page_size)
        
        data, meta = ohlcv_service.get_ohlcv_data(
            db, symbol.upper(), date_range, source, pagination
        )
        
        if not data:
            raise HTTPException(
                status_code=404,
                detail=f"No OHLCV data found for symbol '{symbol}'"
            )
        
        return PaginatedResponse(data=data, meta=meta)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting OHLCV data for {symbol}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{symbol}/latest")
@cached(ttl=60, key_prefix="ohlcv_latest")
async def get_latest_price(
    symbol: str,
    db: Session = Depends(get_db)
):
    """
    Get latest available price for a stock (cached for 1 minute).
    
    - **symbol**: Stock symbol
    
    Returns the most recent OHLCV record.
    """
    try:
        latest_data = ohlcv_service.get_latest_price(db, symbol.upper())
        
        if not latest_data:
            raise HTTPException(
                status_code=404,
                detail=f"No price data found for symbol '{symbol}'"
            )
        
        return latest_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting latest price for {symbol}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{symbol}/summary")
@cached(ttl=300, key_prefix="ohlcv_summary")
async def get_price_summary(
    symbol: str,
    days: int = Query(30, ge=1, le=365, description="Number of days for summary"),
    db: Session = Depends(get_db)
):
    """
    Get price summary and statistics for a stock (cached for 5 minutes).
    
    - **symbol**: Stock symbol
    - **days**: Number of days to include in summary (default: 30, max: 365)
    
    Returns comprehensive price statistics including:
    - Current and previous prices
    - Price change and percentage
    - Min/max prices
    - Average price and volume
    """
    try:
        summary = ohlcv_service.get_price_summary(db, symbol.upper(), days)
        
        if not summary:
            raise HTTPException(
                status_code=404,
                detail=f"No price data found for symbol '{symbol}'"
            )
        
        return summary
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting price summary for {symbol}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{symbol}/volume")
@cached(ttl=300, key_prefix="ohlcv_volume")
async def get_volume_analysis(
    symbol: str,
    days: int = Query(30, ge=1, le=365, description="Number of days for analysis"),
    db: Session = Depends(get_db)
):
    """
    Get volume analysis for a stock (cached for 5 minutes).
    
    - **symbol**: Stock symbol
    - **days**: Number of days to analyze (default: 30, max: 365)
    
    Returns volume statistics and trends.
    """
    try:
        volume_data = ohlcv_service.get_volume_analysis(db, symbol.upper(), days)
        
        if not volume_data:
            raise HTTPException(
                status_code=404,
                detail=f"No volume data found for symbol '{symbol}'"
            )
        
        return volume_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting volume analysis for {symbol}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{symbol}/technical")
@cached(ttl=600, key_prefix="ohlcv_technical")
async def get_technical_indicators(
    symbol: str,
    days: int = Query(50, ge=20, le=200, description="Number of days for calculations"),
    db: Session = Depends(get_db)
):
    """
    Get basic technical indicators for a stock (cached for 10 minutes).
    
    - **symbol**: Stock symbol
    - **days**: Number of days for calculations (default: 50, min: 20, max: 200)
    
    Returns basic technical analysis including:
    - Simple Moving Averages (SMA 20, SMA 50)
    - Support and resistance levels
    - Volatility measures
    - Trend indication
    """
    try:
        indicators = ohlcv_service.get_technical_indicators(db, symbol.upper(), days)
        
        if not indicators:
            raise HTTPException(
                status_code=404,
                detail=f"Insufficient data for technical analysis of '{symbol}'"
            )
        
        return indicators
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting technical indicators for {symbol}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{symbol}/historical")
async def get_historical_data(
    symbol: str,
    period: str = Query("1y", description="Period: 1w, 1m, 3m, 6m, 1y, 2y, 5y"),
    source: Optional[str] = Query(None, description="Data source filter"),
    db: Session = Depends(get_db)
):
    """
    Get historical OHLCV data for predefined periods.
    
    - **symbol**: Stock symbol
    - **period**: Time period (1w, 1m, 3m, 6m, 1y, 2y, 5y)
    - **source**: Filter by data source (optional)
    
    Returns all historical data for the specified period without pagination.
    """
    try:
        # Map period to days
        period_map = {
            "1w": 7,
            "1m": 30,
            "3m": 90,
            "6m": 180,
            "1y": 365,
            "2y": 730,
            "5y": 1825
        }
        
        if period not in period_map:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid period '{period}'. Use: {', '.join(period_map.keys())}"
            )
        
        days = period_map[period]
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        
        date_range = DateRangeQuery(start_date=start_date, end_date=end_date)
        
        data, _ = ohlcv_service.get_ohlcv_data(
            db, symbol.upper(), date_range, source, None
        )
        
        if not data:
            raise HTTPException(
                status_code=404,
                detail=f"No historical data found for symbol '{symbol}'"
            )
        
        return {
            "symbol": symbol.upper(),
            "period": period,
            "start_date": start_date,
            "end_date": end_date,
            "data": data,
            "count": len(data)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting historical data for {symbol}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
