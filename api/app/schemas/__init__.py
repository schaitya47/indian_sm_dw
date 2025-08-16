"""
Pydantic schemas for API request/response models.
"""

from typing import Optional, List, Any
from datetime import datetime, date
from pydantic import BaseModel, Field, ConfigDict


class BaseResponse(BaseModel):
    """Base response model with common fields."""
    model_config = ConfigDict(from_attributes=True)


class PaginationMeta(BaseModel):
    """Pagination metadata."""
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    total_count: int = Field(..., description="Total number of items")
    total_pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Whether there is a next page")
    has_prev: bool = Field(..., description="Whether there is a previous page")


class PaginatedResponse(BaseModel):
    """Paginated response wrapper."""
    data: List[Any] = Field(..., description="List of data items")
    meta: PaginationMeta = Field(..., description="Pagination metadata")


# Stock Schemas
class StockBase(BaseModel):
    """Base stock schema."""
    symbol: str = Field(..., description="Stock symbol")
    company_name: Optional[str] = Field(None, description="Company name")
    industry: Optional[str] = Field(None, description="Industry")
    series: Optional[str] = Field(None, description="Series")
    isin_code: Optional[str] = Field(None, description="ISIN code")
    yfin_symbol: Optional[str] = Field(None, description="Yahoo Finance symbol")


class Stock(StockBase, BaseResponse):
    """Stock response model."""
    stock_key: int = Field(..., description="Stock key")
    load_ts: Optional[datetime] = Field(None, description="Load timestamp")


class StockCreate(StockBase):
    """Stock creation model."""
    pass


class StockUpdate(BaseModel):
    """Stock update model."""
    company_name: Optional[str] = None
    industry: Optional[str] = None
    series: Optional[str] = None
    isin_code: Optional[str] = None
    yfin_symbol: Optional[str] = None


# OHLCV Schemas
class OHLCVBase(BaseModel):
    """Base OHLCV schema."""
    date: date = Field(..., description="Trading date")
    symbol: str = Field(..., description="Stock symbol")
    source: str = Field(..., description="Data source")
    open_price: Optional[float] = Field(None, description="Opening price")
    high_price: Optional[float] = Field(None, description="High price")
    low_price: Optional[float] = Field(None, description="Low price")
    close_price: Optional[float] = Field(None, description="Closing price")
    volume: Optional[int] = Field(None, description="Volume")
    dividends: Optional[float] = Field(None, description="Dividends")
    stock_splits: Optional[float] = Field(None, description="Stock splits")


class OHLCV(OHLCVBase, BaseResponse):
    """OHLCV response model."""
    ohlcv_key: int = Field(..., description="OHLCV key")
    load_ts: Optional[datetime] = Field(None, description="Load timestamp")


class OHLCVCreate(OHLCVBase):
    """OHLCV creation model."""
    pass


# Balance Sheet Schemas
class BalanceSheetBase(BaseModel):
    """Base balance sheet schema."""
    date: date = Field(..., description="Reporting date")
    symbol: str = Field(..., description="Stock symbol")
    source: str = Field(..., description="Data source")
    reporting_period: Optional[str] = Field(None, description="Reporting period")
    bal_tca: Optional[float] = Field(None, description="Total Current Assets")
    bal_tota: Optional[float] = Field(None, description="Total Assets")
    bal_tcl: Optional[float] = Field(None, description="Total Current Liabilities")
    bal_totl: Optional[float] = Field(None, description="Total Liabilities")
    bal_teq: Optional[float] = Field(None, description="Total Equity")


class BalanceSheet(BalanceSheetBase, BaseResponse):
    """Balance sheet response model."""
    balance_sheet_key: int = Field(..., description="Balance sheet key")
    load_ts: Optional[datetime] = Field(None, description="Load timestamp")


# Cash Flow Schemas
class CashFlowBase(BaseModel):
    """Base cash flow schema."""
    date: date = Field(..., description="Reporting date")
    symbol: str = Field(..., description="Stock symbol")
    source: str = Field(..., description="Data source")
    reporting_period: Optional[str] = Field(None, description="Reporting period")
    caf_cfoa: Optional[float] = Field(None, description="Cash Flow from Operating Activities")
    caf_cfia: Optional[float] = Field(None, description="Cash Flow from Investing Activities")
    caf_cffa: Optional[float] = Field(None, description="Cash Flow from Financing Activities")
    caf_fcf: Optional[float] = Field(None, description="Free Cash Flow")


class CashFlow(CashFlowBase, BaseResponse):
    """Cash flow response model."""
    cashflow_key: int = Field(..., description="Cash flow key")
    load_ts: Optional[datetime] = Field(None, description="Load timestamp")


# Income Statement Schemas
class IncomeBase(BaseModel):
    """Base income statement schema."""
    date: date = Field(..., description="Reporting date")
    symbol: str = Field(..., description="Stock symbol")
    source: str = Field(..., description="Data source")
    reporting_period: Optional[str] = Field(None, description="Reporting period")
    q_inc_trev: Optional[float] = Field(None, description="Total Revenue")
    q_inc_ope: Optional[float] = Field(None, description="Operating Expenses")
    q_inc_ninc: Optional[float] = Field(None, description="Net Income")
    q_inc_eps: Optional[float] = Field(None, description="Earnings Per Share")


class Income(IncomeBase, BaseResponse):
    """Income statement response model."""
    income_key: int = Field(..., description="Income key")
    load_ts: Optional[datetime] = Field(None, description="Load timestamp")


# Key Ratios Schemas
class KeyRatiosBase(BaseModel):
    """Base key ratios schema."""
    date: date = Field(..., description="Date")
    symbol: str = Field(..., description="Stock symbol")
    source: str = Field(..., description="Data source")
    pe: Optional[float] = Field(None, description="Price-to-Earnings ratio")
    pb: Optional[float] = Field(None, description="Price-to-Book ratio")
    market_cap: Optional[float] = Field(None, description="Market capitalization")
    div_yield: Optional[float] = Field(None, description="Dividend yield")
    roe: Optional[float] = Field(None, description="Return on Equity")
    beta: Optional[float] = Field(None, description="Beta coefficient")
    eps: Optional[float] = Field(None, description="Earnings per share")


class KeyRatios(KeyRatiosBase, BaseResponse):
    """Key ratios response model."""
    key_ratios_key: int = Field(..., description="Key ratios key")
    load_ts: Optional[datetime] = Field(None, description="Load timestamp")


# Recommendations Schemas
class RecommendationsBase(BaseModel):
    """Base recommendations schema."""
    date: date = Field(..., description="Date")
    symbol: str = Field(..., description="Stock symbol")
    source: str = Field(..., description="Data source")
    recommendation_period: Optional[datetime] = Field(None, description="Recommendation period")
    strong_buy: Optional[int] = Field(None, description="Strong buy count")
    buy: Optional[int] = Field(None, description="Buy count")
    hold: Optional[int] = Field(None, description="Hold count")
    sell: Optional[int] = Field(None, description="Sell count")
    strong_sell: Optional[int] = Field(None, description="Strong sell count")


class Recommendations(RecommendationsBase, BaseResponse):
    """Recommendations response model."""
    recommendation_key: int = Field(..., description="Recommendation key")
    load_ts: Optional[datetime] = Field(None, description="Load timestamp")


# Query Parameters
class DateRangeQuery(BaseModel):
    """Date range query parameters."""
    start_date: Optional[date] = Field(None, description="Start date")
    end_date: Optional[date] = Field(None, description="End date")


class PaginationQuery(BaseModel):
    """Pagination query parameters."""
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(50, ge=1, le=1000, description="Page size")


class StockQuery(DateRangeQuery, PaginationQuery):
    """Stock query parameters."""
    symbol: Optional[str] = Field(None, description="Stock symbol filter")
    industry: Optional[str] = Field(None, description="Industry filter")
    source: Optional[str] = Field(None, description="Source filter")


# Health Check
class HealthCheck(BaseModel):
    """Health check response."""
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(..., description="Check timestamp")
    version: str = Field(..., description="API version")
    database: str = Field(..., description="Database status")
    cache: str = Field(..., description="Cache status")


# Error Response
class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Error detail")
    code: Optional[str] = Field(None, description="Error code")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Error timestamp")
