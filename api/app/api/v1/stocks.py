"""
Stock API endpoints.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db import get_db
from app.services import stock_service
from app.schemas import (
    Stock, StockQuery, PaginatedResponse, PaginationQuery, 
    ErrorResponse
)
from app.utils import cached, check_rate_limit
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/stocks", tags=["stocks"])


@router.get("", response_model=PaginatedResponse)
async def list_stocks(
    query: StockQuery = Depends(),
    db: Session = Depends(get_db)
):
    """
    Get paginated list of stocks with filtering options.
    
    - **symbol**: Filter by stock symbol (partial match)
    - **industry**: Filter by industry (partial match)
    - **source**: Filter by data source
    - **page**: Page number (default: 1)
    - **page_size**: Items per page (default: 50, max: 1000)
    """
    try:
        stocks, meta = stock_service.get_stocks_with_filters(db, query)
        
        return PaginatedResponse(
            data=stocks,
            meta=meta
        )
    except Exception as e:
        logger.error(f"Error listing stocks: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/search")
async def search_stocks(
    q: str = Query(..., description="Search term for symbol or company name"),
    limit: int = Query(10, ge=1, le=50, description="Maximum results"),
    db: Session = Depends(get_db)
):
    """
    Search stocks by symbol or company name.
    
    - **q**: Search term (required)
    - **limit**: Maximum number of results (default: 10, max: 50)
    """
    try:
        stocks = stock_service.search_stocks(db, q, limit)
        
        return {
            "query": q,
            "results": [
                {
                    "stock_key": stock.stock_key,
                    "symbol": stock.nk_symbol,
                    "company_name": stock.company_name,
                    "industry": stock.industry,
                    "series": stock.series
                }
                for stock in stocks
            ],
            "count": len(stocks)
        }
    except Exception as e:
        logger.error(f"Error searching stocks: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/industries")
@cached(ttl=3600, key_prefix="stocks")
async def list_industries(db: Session = Depends(get_db)):
    """
    Get list of all industries.
    
    Returns a list of unique industry names.
    """
    try:
        industries = stock_service.get_industries(db)
        return {
            "industries": sorted(industries),
            "count": len(industries)
        }
    except Exception as e:
        logger.error(f"Error listing industries: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/industries/{industry}")
async def get_stocks_by_industry(
    industry: str,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=1000, description="Page size"),
    db: Session = Depends(get_db)
):
    """
    Get all stocks in a specific industry.
    
    - **industry**: Industry name
    - **page**: Page number (default: 1)
    - **page_size**: Items per page (default: 50)
    """
    try:
        # Get stocks by industry
        stocks = stock_service.get_stocks_by_industry(db, industry)
        
        # Manual pagination
        total_count = len(stocks)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_stocks = stocks[start_idx:end_idx]
        
        # Calculate metadata
        import math
        total_pages = math.ceil(total_count / page_size)
        
        return {
            "industry": industry,
            "data": [
                {
                    "stock_key": stock.stock_key,
                    "symbol": stock.nk_symbol,
                    "company_name": stock.company_name,
                    "series": stock.series,
                    "isin_code": stock.isin_code
                }
                for stock in paginated_stocks
            ],
            "meta": {
                "page": page,
                "page_size": page_size,
                "total_count": total_count,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_prev": page > 1
            }
        }
    except Exception as e:
        logger.error(f"Error getting stocks by industry: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{symbol}")
async def get_stock_by_symbol(
    symbol: str,
    db: Session = Depends(get_db)
):
    """
    Get detailed information for a specific stock.
    
    - **symbol**: Stock symbol (e.g., 'TCS', 'RELIANCE')
    
    Returns comprehensive stock information including latest price and data sources.
    """
    try:
        stock_info = stock_service.get_stock_summary(db, symbol.upper())
        
        if not stock_info:
            raise HTTPException(
                status_code=404, 
                detail=f"Stock with symbol '{symbol}' not found"
            )
        
        return stock_info
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting stock {symbol}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{symbol}/basic")
@cached(ttl=300, key_prefix="stock_basic")
async def get_stock_basic_info(
    symbol: str,
    db: Session = Depends(get_db)
):
    """
    Get basic stock information (cached for 5 minutes).
    
    - **symbol**: Stock symbol
    
    Returns basic stock details without heavy calculations.
    """
    try:
        stock = stock_service.get_by_symbol(db, symbol.upper())
        
        if not stock:
            raise HTTPException(
                status_code=404,
                detail=f"Stock with symbol '{symbol}' not found"
            )
        
        return {
            "stock_key": stock.stock_key,
            "symbol": stock.nk_symbol,
            "company_name": stock.company_name,
            "industry": stock.industry,
            "series": stock.series,
            "isin_code": stock.isin_code,
            "yfin_symbol": stock.yfin_symbol,
            "load_ts": stock.load_ts
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting basic stock info for {symbol}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
