"""
OHLCV service for price and volume data operations.
"""

from typing import List, Optional, Dict, Any
from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, desc
from app.db.models import FactOHLCV, DimStock, DimDate, DimSource
from app.services.base import BaseService
from app.schemas import PaginationQuery, PaginationMeta, DateRangeQuery


class OHLCVService(BaseService[FactOHLCV]):
    """Service for OHLCV operations."""
    
    def __init__(self):
        super().__init__(FactOHLCV)
    
    def get_ohlcv_data(
        self,
        db: Session,
        symbol: str,
        date_range: DateRangeQuery,
        source: Optional[str] = None,
        pagination: Optional[PaginationQuery] = None
    ) -> tuple[List[Dict[str, Any]], Optional[PaginationMeta]]:
        """Get OHLCV data for a stock with filtering."""
        
        # Build query with joins
        query = db.query(
            FactOHLCV,
            DimDate.nk_full_date.label('date'),
            DimStock.nk_symbol.label('symbol'),
            DimSource.source_name.label('source_name')
        ).join(DimDate, FactOHLCV.date_key == DimDate.date_key)\
         .join(DimStock, FactOHLCV.stock_key == DimStock.stock_key)\
         .join(DimSource, FactOHLCV.source_key == DimSource.source_key)
        
        # Apply filters
        filters = [DimStock.nk_symbol == symbol]
        
        if date_range.start_date:
            filters.append(DimDate.nk_full_date >= date_range.start_date)
        if date_range.end_date:
            filters.append(DimDate.nk_full_date <= date_range.end_date)
        if source:
            filters.append(DimSource.source_name == source)
        
        query = query.filter(and_(*filters))
        
        # Order by date descending
        query = query.order_by(desc(DimDate.nk_full_date))
        
        # Handle pagination
        meta = None
        if pagination:
            total_count = query.count()
            offset = (pagination.page - 1) * pagination.page_size
            results = query.offset(offset).limit(pagination.page_size).all()
            
            import math
            total_pages = math.ceil(total_count / pagination.page_size)
            meta = PaginationMeta(
                page=pagination.page,
                page_size=pagination.page_size,
                total_count=total_count,
                total_pages=total_pages,
                has_next=pagination.page < total_pages,
                has_prev=pagination.page > 1
            )
        else:
            results = query.all()
        
        # Convert to response format
        data = []
        for row in results:
            ohlcv, trade_date, stock_symbol, source_name = row
            data.append({
                "ohlcv_key": ohlcv.ohlcv_key,
                "date": trade_date,
                "symbol": stock_symbol,
                "source": source_name,
                "open_price": ohlcv.open_price,
                "high_price": ohlcv.high_price,
                "low_price": ohlcv.low_price,
                "close_price": ohlcv.close_price,
                "volume": ohlcv.volume,
                "dividends": ohlcv.dividends,
                "stock_splits": ohlcv.stock_splits,
                "load_ts": ohlcv.load_ts
            })
        
        return data, meta
    
    def get_latest_price(self, db: Session, symbol: str) -> Optional[Dict[str, Any]]:
        """Get latest price for a stock."""
        result = db.query(
            FactOHLCV,
            DimDate.nk_full_date.label('date'),
            DimSource.source_name.label('source_name')
        ).join(DimDate, FactOHLCV.date_key == DimDate.date_key)\
         .join(DimStock, FactOHLCV.stock_key == DimStock.stock_key)\
         .join(DimSource, FactOHLCV.source_key == DimSource.source_key)\
         .filter(DimStock.nk_symbol == symbol)\
         .order_by(desc(DimDate.nk_full_date))\
         .first()
        
        if not result:
            return None
        
        ohlcv, trade_date, source_name = result
        return {
            "symbol": symbol,
            "date": trade_date,
            "source": source_name,
            "open_price": ohlcv.open_price,
            "high_price": ohlcv.high_price,
            "low_price": ohlcv.low_price,
            "close_price": ohlcv.close_price,
            "volume": ohlcv.volume,
            "change": None,  # Will be calculated if previous data exists
            "change_percent": None
        }
    
    def get_price_summary(self, db: Session, symbol: str, days: int = 30) -> Optional[Dict[str, Any]]:
        """Get price summary for the last N days."""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        
        # Get OHLCV data for the period
        results = db.query(
            FactOHLCV.close_price,
            FactOHLCV.volume,
            DimDate.nk_full_date
        ).join(DimDate, FactOHLCV.date_key == DimDate.date_key)\
         .join(DimStock, FactOHLCV.stock_key == DimStock.stock_key)\
         .filter(
            and_(
                DimStock.nk_symbol == symbol,
                DimDate.nk_full_date >= start_date,
                DimDate.nk_full_date <= end_date
            )
        ).order_by(DimDate.nk_full_date).all()
        
        if not results:
            return None
        
        prices = [r.close_price for r in results if r.close_price]
        volumes = [r.volume for r in results if r.volume]
        
        if not prices:
            return None
        
        # Calculate summary statistics
        current_price = prices[-1]
        previous_price = prices[0] if len(prices) > 1 else current_price
        
        return {
            "symbol": symbol,
            "period_days": days,
            "current_price": current_price,
            "period_start_price": previous_price,
            "change": current_price - previous_price,
            "change_percent": ((current_price - previous_price) / previous_price * 100) if previous_price else 0,
            "min_price": min(prices),
            "max_price": max(prices),
            "avg_price": sum(prices) / len(prices),
            "avg_volume": sum(volumes) / len(volumes) if volumes else 0,
            "total_volume": sum(volumes) if volumes else 0,
            "data_points": len(results)
        }
    
    def get_volume_analysis(self, db: Session, symbol: str, days: int = 30) -> Optional[Dict[str, Any]]:
        """Get volume analysis for a stock."""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        
        # Get volume data
        results = db.query(
            FactOHLCV.volume,
            FactOHLCV.close_price,
            DimDate.nk_full_date
        ).join(DimDate, FactOHLCV.date_key == DimDate.date_key)\
         .join(DimStock, FactOHLCV.stock_key == DimStock.stock_key)\
         .filter(
            and_(
                DimStock.nk_symbol == symbol,
                DimDate.nk_full_date >= start_date,
                DimDate.nk_full_date <= end_date,
                FactOHLCV.volume.is_not(None)
            )
        ).order_by(DimDate.nk_full_date).all()
        
        if not results:
            return None
        
        volumes = [r.volume for r in results]
        
        return {
            "symbol": symbol,
            "period_days": days,
            "avg_volume": sum(volumes) / len(volumes),
            "min_volume": min(volumes),
            "max_volume": max(volumes),
            "total_volume": sum(volumes),
            "latest_volume": volumes[-1] if volumes else 0,
            "volume_trend": "increasing" if len(volumes) > 1 and volumes[-1] > volumes[0] else "decreasing"
        }
    
    def get_technical_indicators(self, db: Session, symbol: str, days: int = 50) -> Optional[Dict[str, Any]]:
        """Calculate basic technical indicators."""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        
        # Get price data
        results = db.query(
            FactOHLCV.close_price,
            FactOHLCV.high_price,
            FactOHLCV.low_price,
            DimDate.nk_full_date
        ).join(DimDate, FactOHLCV.date_key == DimDate.date_key)\
         .join(DimStock, FactOHLCV.stock_key == DimStock.stock_key)\
         .filter(
            and_(
                DimStock.nk_symbol == symbol,
                DimDate.nk_full_date >= start_date,
                DimDate.nk_full_date <= end_date
            )
        ).order_by(DimDate.nk_full_date).all()
        
        if len(results) < 20:  # Need minimum data for calculations
            return None
        
        close_prices = [r.close_price for r in results if r.close_price]
        high_prices = [r.high_price for r in results if r.high_price]
        low_prices = [r.low_price for r in results if r.low_price]
        
        if len(close_prices) < 20:
            return None
        
        # Simple Moving Averages
        sma_20 = sum(close_prices[-20:]) / 20 if len(close_prices) >= 20 else None
        sma_50 = sum(close_prices[-50:]) / 50 if len(close_prices) >= 50 else None
        
        # Support and Resistance (basic)
        support = min(low_prices[-20:]) if len(low_prices) >= 20 else None
        resistance = max(high_prices[-20:]) if len(high_prices) >= 20 else None
        
        # Volatility (simple standard deviation)
        if len(close_prices) >= 20:
            recent_prices = close_prices[-20:]
            mean_price = sum(recent_prices) / len(recent_prices)
            variance = sum((p - mean_price) ** 2 for p in recent_prices) / len(recent_prices)
            volatility = variance ** 0.5
        else:
            volatility = None
        
        return {
            "symbol": symbol,
            "current_price": close_prices[-1],
            "sma_20": sma_20,
            "sma_50": sma_50,
            "support_level": support,
            "resistance_level": resistance,
            "volatility": volatility,
            "trend": "bullish" if sma_20 and sma_50 and sma_20 > sma_50 else "bearish"
        }


# Global instance
ohlcv_service = OHLCVService()
