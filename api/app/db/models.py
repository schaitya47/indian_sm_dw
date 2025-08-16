"""
SQLAlchemy models for the data warehouse.
"""

from sqlalchemy import (
    Column, Integer, String, DateTime, Double, Boolean, 
    Text, BigInteger, SmallInteger, ForeignKey, UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class DimDate(Base):
    """Date dimension table."""
    __tablename__ = "dim_date"
    __table_args__ = {"schema": "stock_dw"}
    
    date_key = Column(Integer, primary_key=True)
    nk_full_date = Column(DateTime, nullable=False, unique=True)
    day = Column(Integer)
    month = Column(Integer)
    month_name = Column(Text)
    quarter = Column(Integer)
    year = Column(Integer)
    day_of_week = Column(Integer)
    day_name = Column(Text)
    is_weekend = Column(Boolean)


class DimSource(Base):
    """Source dimension table."""
    __tablename__ = "dim_source"
    __table_args__ = {"schema": "stock_dw"}
    
    source_key = Column(Integer, primary_key=True, autoincrement=True)
    source_name = Column(Text, nullable=False)
    source_url = Column(Text)
    load_ts = Column(DateTime, default=func.now())


class DimStock(Base):
    """Stock dimension table."""
    __tablename__ = "dim_stock"
    __table_args__ = {"schema": "stock_dw"}
    
    stock_key = Column(Integer, primary_key=True, autoincrement=True)
    nk_symbol = Column(Text, nullable=False, unique=True)
    company_name = Column(Text)
    industry = Column(Text)
    series = Column(Text)
    isin_code = Column(Text)
    yfin_symbol = Column(Text)
    load_ts = Column(DateTime, default=func.now())


class FactOHLCV(Base):
    """OHLCV fact table."""
    __tablename__ = "fact_ohlcv"
    __table_args__ = (
        UniqueConstraint('date_key', 'stock_key', 'source_key', name='fact_ohlcv_unique_key'),
        {"schema": "stock_dw"}
    )
    
    ohlcv_key = Column(Integer, primary_key=True, autoincrement=True)
    date_key = Column(BigInteger, ForeignKey('stock_dw.dim_date.date_key'), nullable=False)
    stock_key = Column(BigInteger, ForeignKey('stock_dw.dim_stock.stock_key'), nullable=False)
    source_key = Column(BigInteger, ForeignKey('stock_dw.dim_source.source_key'), nullable=False)
    open_price = Column(Double)
    high_price = Column(Double)
    low_price = Column(Double)
    close_price = Column(Double)
    volume = Column(BigInteger)
    dividends = Column(Double)
    stock_splits = Column(Double)
    load_ts = Column(DateTime, default=func.now())
    
    # Relationships
    date = relationship("DimDate")
    stock = relationship("DimStock")
    source = relationship("DimSource")


class FactBalanceSheet(Base):
    """Balance Sheet fact table."""
    __tablename__ = "fact_balance_sheet"
    __table_args__ = (
        UniqueConstraint('date_key', 'stock_key', 'source_key', 'reporting_period', 
                        name='fact_balance_sheet_unique_key'),
        {"schema": "stock_dw"}
    )
    
    balance_sheet_key = Column(Integer, primary_key=True, autoincrement=True)
    date_key = Column(Integer, ForeignKey('stock_dw.dim_date.date_key'), nullable=False)
    stock_key = Column(Integer, ForeignKey('stock_dw.dim_stock.stock_key'), nullable=False)
    source_key = Column(Integer, ForeignKey('stock_dw.dim_source.source_key'), nullable=False)
    reporting_period = Column(Text)
    
    # Balance Sheet metrics
    bal_csti = Column(Double)  # Cash & Short-Term Investments
    bal_trec = Column(Double)  # Total Receivables
    bal_tinv = Column(Double)  # Total Inventory
    bal_oca = Column(Double)   # Other Current Assets
    bal_tca = Column(Double)   # Total Current Assets
    bal_netl = Column(Double)  # Net Loans
    bal_nppe = Column(Double)  # Net Property, Plant & Equipment
    bal_gint = Column(Double)  # Goodwill & Intangibles
    bal_lti = Column(Double)   # Long-Term Investments
    bal_otha = Column(Double)  # Other Assets
    bal_tota = Column(Double)  # Total Assets
    bal_accp = Column(Double)  # Accounts Payable
    bal_tdep = Column(Double)  # Total Deposits
    bal_ocl = Column(Double)   # Other Current Liabilities
    bal_tcl = Column(Double)   # Total Current Liabilities
    bal_tltd = Column(Double)  # Total Long-Term Debt
    bal_tdeb = Column(Double)  # Total Debt
    bal_dit = Column(Double)   # Deferred Income Taxes
    bal_mint = Column(Double)  # Minority Interest
    bal_othl = Column(Double)  # Other Liabilities
    bal_totl = Column(Double)  # Total Liabilities
    bal_coms = Column(Double)  # Common Stock
    bal_apic = Column(Double)  # Additional Paid-In Capital
    bal_rtne = Column(Double)  # Retained Earnings
    bal_oeq = Column(Double)   # Other Equity
    bal_teq = Column(Double)   # Total Equity
    bal_tlse = Column(Double)  # Total Liabilities & Shareholders' Equity
    bal_tcso = Column(Double)  # Total Common Shares Outstanding
    bal_tpso = Column(Text)    # Total Preferred Shares Outstanding
    bal_nca = Column(Double)   # Net Current Assets
    bal_ca = Column(Double)    # Current Assets
    bal_ncl = Column(Double)   # Net Current Liabilities
    bal_dta = Column(Double)   # Deferred Tax Assets
    
    load_ts = Column(DateTime, default=func.now())
    
    # Relationships
    date = relationship("DimDate")
    stock = relationship("DimStock")
    source = relationship("DimSource")


class FactCashFlow(Base):
    """Cash Flow fact table."""
    __tablename__ = "fact_cashflow"
    __table_args__ = (
        UniqueConstraint('date_key', 'stock_key', 'source_key', 'reporting_period',
                        name='fact_cashflow_unique_key'),
        {"schema": "stock_dw"}
    )
    
    cashflow_key = Column(Integer, primary_key=True, autoincrement=True)
    date_key = Column(Integer, ForeignKey('stock_dw.dim_date.date_key'), nullable=False)
    stock_key = Column(Integer, ForeignKey('stock_dw.dim_stock.stock_key'), nullable=False)
    source_key = Column(Integer, ForeignKey('stock_dw.dim_source.source_key'), nullable=False)
    reporting_period = Column(Text)
    
    # Cash Flow metrics
    caf_ciwc = Column(Double)  # Change in Working Capital
    caf_cfoa = Column(Double)  # Cash Flow from Operating Activities
    caf_cexp = Column(Double)  # Capital Expenditures
    caf_cfia = Column(Double)  # Cash Flow from Investing Activities
    caf_tcdp = Column(Double)  # Total Cash Dividends Paid
    caf_cffa = Column(Double)  # Cash Flow from Financing Activities
    caf_fee = Column(Text)     # Fee or Expense Explanation
    caf_ncic = Column(Double)  # Net Change in Cash & Cash Equivalents
    caf_fcf = Column(Double)   # Free Cash Flow
    
    load_ts = Column(DateTime, default=func.now())
    
    # Relationships
    date = relationship("DimDate")
    stock = relationship("DimStock")
    source = relationship("DimSource")


class FactIncome(Base):
    """Income Statement fact table."""
    __tablename__ = "fact_income"
    __table_args__ = (
        UniqueConstraint('date_key', 'stock_key', 'source_key', 'reporting_period',
                        name='fact_income_unique_key'),
        {"schema": "stock_dw"}
    )
    
    income_key = Column(Integer, primary_key=True, autoincrement=True)
    date_key = Column(Integer, ForeignKey('stock_dw.dim_date.date_key'), nullable=False)
    stock_key = Column(Integer, ForeignKey('stock_dw.dim_stock.stock_key'), nullable=False)
    source_key = Column(Integer, ForeignKey('stock_dw.dim_source.source_key'), nullable=False)
    reporting_period = Column(Text)
    
    # Income Statement metrics
    q_inc_trev = Column(Double)  # Total Revenue
    q_inc_raw = Column(Text)     # Raw Material Costs
    q_inc_pfc = Column(Text)     # Profit from Core
    q_inc_epc = Column(Text)     # Earnings per Core
    q_inc_sga = Column(Text)     # Selling, General & Admin Expenses
    q_inc_ope = Column(Double)   # Operating Expenses
    q_inc_ebi = Column(Double)   # Earnings Before Interest
    q_inc_dep = Column(Double)   # Depreciation
    q_inc_pbi = Column(Double)   # Profit Before Interest
    q_inc_ioi = Column(Double)   # Income from Other Investments
    q_inc_pbt = Column(Double)   # Profit Before Tax
    q_inc_toi = Column(Double)   # Total Operating Income
    q_inc_ninc = Column(Double)  # Net Income
    q_inc_eps = Column(Double)   # Earnings Per Share
    q_inc_dps = Column(Text)     # Dividends Per Share
    q_inc_pyr = Column(Text)     # Payout Ratio
    
    load_ts = Column(DateTime, default=func.now())
    
    # Relationships
    date = relationship("DimDate")
    stock = relationship("DimStock")
    source = relationship("DimSource")


class FactKeyRatios(Base):
    """Key Ratios fact table."""
    __tablename__ = "fact_key_ratios"
    __table_args__ = (
        UniqueConstraint('date_key', 'stock_key', 'source_key',
                        name='fact_key_ratios_unique_key'),
        {"schema": "stock_dw"}
    )
    
    key_ratios_key = Column(Integer, primary_key=True, autoincrement=True)
    date_key = Column(Integer, ForeignKey('stock_dw.dim_date.date_key'), nullable=False)
    stock_key = Column(Integer, ForeignKey('stock_dw.dim_stock.stock_key'), nullable=False)
    source_key = Column(Integer, ForeignKey('stock_dw.dim_source.source_key'), nullable=False)
    
    # Key Ratios
    risk = Column(Double)
    letter_3mavgvol = Column(Double)
    letter_4wpct = Column(Double)
    letter_52whigh = Column(Double)
    letter_52wlow = Column(Double)
    letter_52wpct = Column(Double)
    beta = Column(Double)
    bps = Column(Double)
    div_yield = Column(Double)
    eps = Column(Double)
    inddy = Column(Double)
    indpb = Column(Double)
    indpe = Column(Double)
    market_cap = Column(Double)
    mrkt_cap_rank = Column(SmallInteger)
    pb = Column(Double)
    pe = Column(Double)
    roe = Column(Double)
    n_shareholders = Column(Integer)
    last_price = Column(Double)
    ttm_pe = Column(Double)
    market_cap_label = Column(Text)
    letter_12mvol = Column(Double)
    mrkt_capf = Column(Double)
    apef = Column(Double)
    pbr = Column(Double)
    etf_liq = Column(Double)
    etf_liq_label = Column(Text)
    expense_ratio = Column(Text)
    track_err = Column(Text)
    ind_expense_ratio = Column(Text)
    ind_track_err = Column(Text)
    asst_under_man = Column(Text)
    
    load_ts = Column(DateTime, default=func.now())
    
    # Relationships
    date = relationship("DimDate")
    stock = relationship("DimStock")
    source = relationship("DimSource")


class FactRecommendations(Base):
    """Recommendations fact table."""
    __tablename__ = "fact_recommendations"
    __table_args__ = (
        UniqueConstraint('date_key', 'stock_key', 'source_key', 'recommendation_period',
                        name='fact_recommendations_unique_key'),
        {"schema": "stock_dw"}
    )
    
    recommendation_key = Column(Integer, primary_key=True, autoincrement=True)
    date_key = Column(Integer, ForeignKey('stock_dw.dim_date.date_key'), nullable=False)
    stock_key = Column(Integer, ForeignKey('stock_dw.dim_stock.stock_key'), nullable=False)
    source_key = Column(Integer, ForeignKey('stock_dw.dim_source.source_key'), nullable=False)
    recommendation_period = Column(DateTime)
    
    # Recommendation counts
    strong_buy = Column(SmallInteger)
    buy = Column(SmallInteger)
    hold = Column(SmallInteger)
    sell = Column(SmallInteger)
    strong_sell = Column(SmallInteger)
    
    load_ts = Column(DateTime, default=func.now())
    
    # Relationships
    date = relationship("DimDate")
    stock = relationship("DimStock")
    source = relationship("DimSource")
