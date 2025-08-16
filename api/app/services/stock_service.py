"""
Stock service for stock-related operations.
"""

from typing import List, Optional, Dict, Any
from datetime import date, datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from app.db.models import DimStock, FactOHLCV, DimDate, DimSource
from app.services.base import BaseService
from app.schemas import StockQuery, PaginationQuery, PaginationMeta


class StockService(BaseService[DimStock]):
    """Service for stock operations."""
    
    def __init__(self):
        super().__init__(DimStock)
    
    def get_by_symbol(self, db: Session, symbol: str) -> Optional[DimStock]:
        """Get stock by symbol."""
        return db.query(DimStock).filter(DimStock.nk_symbol == symbol).first()
    
    def get_stocks_with_filters(
        self, 
        db: Session, 
        query: StockQuery
    ) -> tuple[List[Dict[str, Any]], PaginationMeta]:
        """Get stocks with advanced filtering."""
        # Build base query with joins
        base_query = db.query(DimStock)
        
        # Apply filters
        filters = []
        if query.symbol:
            filters.append(DimStock.nk_symbol.ilike(f"%{query.symbol}%"))
        if query.industry:
            filters.append(DimStock.industry.ilike(f"%{query.industry}%"))
        
        if filters:
            base_query = base_query.filter(and_(*filters))
        
        # Get total count
        total_count = base_query.count()
        
        # Apply pagination
        offset = (query.page - 1) * query.page_size
        stocks = base_query.offset(offset).limit(query.page_size).all()
        
        # Convert to dict with additional info
        result = []
        for stock in stocks:
            stock_dict = {
                "stock_key": stock.stock_key,
                "symbol": stock.nk_symbol,
                "company_name": stock.company_name,
                "industry": stock.industry,
                "series": stock.series,
                "isin_code": stock.isin_code,
                "yfin_symbol": stock.yfin_symbol,
                "load_ts": stock.load_ts
            }
            result.append(stock_dict)
        
        # Calculate pagination metadata
        import math
        total_pages = math.ceil(total_count / query.page_size)
        
        meta = PaginationMeta(
            page=query.page,
            page_size=query.page_size,
            total_count=total_count,
            total_pages=total_pages,
            has_next=query.page < total_pages,
            has_prev=query.page > 1
        )
        
        return result, meta
    
    def get_stock_summary(self, db: Session, symbol: str) -> Optional[Dict[str, Any]]:
        """Get comprehensive stock summary."""
        stock = self.get_by_symbol(db, symbol)
        if not stock:
            return None
        
        # Get latest OHLCV data
        latest_ohlcv = db.query(FactOHLCV).join(DimDate).filter(
            FactOHLCV.stock_key == stock.stock_key
        ).order_by(DimDate.nk_full_date.desc()).first()
        
        # Get data count by source
        source_counts = db.query(
            DimSource.source_name,
            func.count(FactOHLCV.ohlcv_key).label('count')
        ).join(FactOHLCV).filter(
            FactOHLCV.stock_key == stock.stock_key
        ).group_by(DimSource.source_name).all()
        
        return {
            "stock_key": stock.stock_key,
            "symbol": stock.nk_symbol,
            "company_name": stock.company_name,
            "industry": stock.industry,
            "series": stock.series,
            "isin_code": stock.isin_code,
            "yfin_symbol": stock.yfin_symbol,
            "latest_price": latest_ohlcv.close_price if latest_ohlcv else None,
            "latest_date": latest_ohlcv.date.nk_full_date if latest_ohlcv else None,
            "data_sources": {row.source_name: row.count for row in source_counts},
            "load_ts": stock.load_ts
        }
    
    def search_stocks(self, db: Session, search_term: str, limit: int = 10) -> List[DimStock]:
        """Search stocks by symbol or company name."""
        return db.query(DimStock).filter(
            or_(
                DimStock.nk_symbol.ilike(f"%{search_term}%"),
                DimStock.company_name.ilike(f"%{search_term}%")
            )
        ).limit(limit).all()
    
    def get_industries(self, db: Session) -> List[str]:
        """Get list of all industries."""
        industries = db.query(DimStock.industry).distinct().filter(
            DimStock.industry.is_not(None)
        ).all()
        return [industry[0] for industry in industries if industry[0]]
    
    def get_stocks_by_industry(self, db: Session, industry: str) -> List[DimStock]:
        """Get all stocks in a specific industry."""
        return db.query(DimStock).filter(
            DimStock.industry.ilike(f"%{industry}%")
        ).all()


# Global instance
stock_service = StockService()
