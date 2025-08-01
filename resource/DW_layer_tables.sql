--====================================================== To create a date table=========================================================
-- Step 0: load dw pipeline to control table
INSERT INTO stock_landing.stage_load_control (pipeline_name)
VALUES 
  ('dim_date_dw'),
  ('dim_source_dw'),
  ('dim_stock_dw'),
  ('fact_ohlcv_dw'),
  ('fact_balance_sheet_dw'),
  ('fact_cashflow_dw'),
  ('fact_income_dw'),
  ('fact_key_ratios_dw'),
  ('fact_recommendations_dw');

UPDATE stock_landing.stage_load_control 
SET last_success_timestamp = '1995-01-01 00:00:00' 
WHERE last_success_timestamp IS NULL;

-- Step 1: Create the dim_date table
CREATE TABLE stock_dw.dim_date (
    date_key INTEGER PRIMARY KEY,         -- Surrogate key
    nk_full_date DATE NOT NULL UNIQUE,    -- Natural key
    day INTEGER,
    month INTEGER,
    month_name TEXT,
    quarter INTEGER,
    year INTEGER,
    day_of_week INTEGER,
    day_name TEXT,
    is_weekend BOOLEAN
);
--====================================================To load the date table============================================================

-- Step 2: Populate the table
DO $$
DECLARE
    d DATE := '1995-01-01';
BEGIN
    WHILE d <= '2045-12-31' LOOP
        INSERT INTO stock_dw.dim_date (
            date_key,
            nk_full_date,
            day,
            month,
            month_name,
            quarter,
            year,
            day_of_week,
            day_name,
            is_weekend
        )
        VALUES (
            TO_CHAR(d, 'YYYYMMDD')::INTEGER,
            d,
            EXTRACT(DAY FROM d),
            EXTRACT(MONTH FROM d),
            TO_CHAR(d, 'Month'),
            EXTRACT(QUARTER FROM d),
            EXTRACT(YEAR FROM d),
            EXTRACT(DOW FROM d) + 1,
            TO_CHAR(d, 'Day'),
            CASE WHEN EXTRACT(DOW FROM d) IN (0, 6) THEN TRUE ELSE FALSE END
        );
        d := d + INTERVAL '1 day';
    END LOOP;
END $$;
--====================================================Create Dim SOurce============================================================
CREATE TABLE stock_dw.dim_source
(
    source_key SERIAL PRIMARY KEY,
    source_name TEXT NOT NULL,
    source_url TEXT,
    load_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE IF EXISTS stock_dw.dim_source
    OWNER to postgres;

INSERT INTO stock_dw.dim_source (source_name, source_url)
VALUES
  ('NSE',   'https://www.nseindia.com/'),
  ('YFIN',  'https://finance.yahoo.com/'),
  ('TICK',  'https://www.tickertape.in/');
--====================================================Create Dim Stock================================================================

CREATE TABLE stock_dw.dim_stock (
    stock_key SERIAL PRIMARY KEY,         -- Surrogate key
    nk_symbol TEXT NOT NULL UNIQUE,       -- Natural key
    company_name TEXT,
    industry TEXT,
    series TEXT,
    isin_code TEXT,
    yfin_symbol TEXT,
    load_ts TIMESTAMP
);

--====================================================Create Fact Ohlcv============================================================
CREATE TABLE stock_dw.fact_ohlcv (
    ohlcv_key SERIAL PRIMARY KEY,
    date_key BIGINT NOT NULL REFERENCES stock_dw.dim_date(date_key),
    stock_key BIGINT NOT NULL REFERENCES stock_dw.dim_stock(stock_key),
    source_key BIGINT NOT NULL REFERENCES stock_dw.dim_source(source_key),
    open_price DOUBLE PRECISION,
    high_price DOUBLE PRECISION,
    low_price DOUBLE PRECISION,
    close_price DOUBLE PRECISION,
    volume BIGINT,
    dividends DOUBLE PRECISION,       -- Nullable, mostly for YFinance
    stock_splits DOUBLE PRECISION,    -- Nullable, mostly for YFinance
    load_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fact_ohlcv_unique_key UNIQUE (date_key, stock_key, source_key)
);
--====================================================Create Fact Balance Sheet============================================================
CREATE TABLE stock_dw.fact_balance_sheet (
    balance_sheet_key SERIAL PRIMARY KEY, -- Surrogate key for the fact table

    date_key INTEGER NOT NULL REFERENCES stock_dw.dim_date(date_key), -- Foreign key to dim_date, derived from end_date
    stock_key INTEGER NOT NULL REFERENCES stock_dw.dim_stock(stock_key), -- Foreign key to dim_stock, derived from symbol
    source_key INTEGER NOT NULL REFERENCES stock_dw.dim_source(source_key), -- Foreign key to dim_source, identifies data origin

    reporting_period TEXT, -- Textual representation of the reporting period (e.g., 'FY23', 'Q1 FY24')

    -- Balance Sheet Metrics (nullable, source: tick_stock_balance_sheet_tbls)
    bal_csti DOUBLE PRECISION, -- Cash & Short-Term Investments
    bal_trec DOUBLE PRECISION, -- Total Receivables
    bal_tinv DOUBLE PRECISION, -- Total Inventory
    bal_oca DOUBLE PRECISION, -- Other Current Assets
    bal_tca DOUBLE PRECISION, -- Total Current Assets
    bal_netl DOUBLE PRECISION, -- Net Loans
    bal_nppe DOUBLE PRECISION, -- Net Property, Plant & Equipment
    bal_gint DOUBLE PRECISION, -- Goodwill & Intangibles
    bal_lti DOUBLE PRECISION, -- Long-Term Investments
    bal_otha DOUBLE PRECISION, -- Other Assets
    bal_tota DOUBLE PRECISION, -- Total Assets

    bal_accp DOUBLE PRECISION, -- Accounts Payable
    bal_tdep DOUBLE PRECISION, -- Total Deposits
    bal_ocl DOUBLE PRECISION, -- Other Current Liabilities
    bal_tcl DOUBLE PRECISION, -- Total Current Liabilities
    bal_tltd DOUBLE PRECISION, -- Total Long-Term Debt
    bal_tdeb DOUBLE PRECISION, -- Total Debt
    bal_dit DOUBLE PRECISION, -- Deferred Income Taxes
    bal_mint DOUBLE PRECISION, -- Minority Interest
    bal_othl DOUBLE PRECISION, -- Other Liabilities
    bal_totl DOUBLE PRECISION, -- Total Liabilities

    bal_coms DOUBLE PRECISION, -- Common Stock
    bal_apic DOUBLE PRECISION, -- Additional Paid-In Capital
    bal_rtne DOUBLE PRECISION, -- Retained Earnings
    bal_oeq DOUBLE PRECISION, -- Other Equity
    bal_teq DOUBLE PRECISION, -- Total Equity
    bal_tlse DOUBLE PRECISION, -- Total Liabilities & Shareholders' Equity

    bal_tcso DOUBLE PRECISION, -- Total Common Shares Outstanding
    bal_tpso TEXT, -- Total Preferred Shares Outstanding (text format in source)
    bal_nca DOUBLE PRECISION, -- Net Current Assets
    bal_ca DOUBLE PRECISION, -- Current Assets
    bal_ncl DOUBLE PRECISION, -- Net Current Liabilities
    bal_dta DOUBLE PRECISION, -- Deferred Tax Assets

    load_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp of data load
);
--====================================================Create Fact Cashflow============================================================
CREATE TABLE stock_dw.fact_cashflow (
    cashflow_key SERIAL PRIMARY KEY, -- Surrogate key for the fact table

    date_key INTEGER NOT NULL REFERENCES stock_dw.dim_date(date_key), -- Foreign key to dim_date, derived from end_date
    stock_key INTEGER NOT NULL REFERENCES stock_dw.dim_stock(stock_key), -- Foreign key to dim_stock, derived from symbol
    source_key INTEGER NOT NULL REFERENCES stock_dw.dim_source(source_key), -- Foreign key to dim_source

    reporting_period TEXT, -- Textual representation of the reporting period (e.g., 'FY23', 'Q1 FY24')

    -- Cash Flow Metrics (nullable, source: tick_stock_cashflow_tbls)
    caf_ciwc DOUBLE PRECISION, -- Cash Flow: Change in Working Capital
    caf_cfoa DOUBLE PRECISION, -- Cash Flow from Operating Activities
    caf_cexp DOUBLE PRECISION, -- Capital Expenditures
    caf_cfia DOUBLE PRECISION, -- Cash Flow from Investing Activities
    caf_tcdp DOUBLE PRECISION, -- Total Cash Dividends Paid
    caf_cffa DOUBLE PRECISION, -- Cash Flow from Financing Activities
    caf_fee TEXT,              -- Free-form field, possibly Fee or Expense Explanation
    caf_ncic DOUBLE PRECISION, -- Net Change in Cash & Cash Equivalents
    caf_fcf DOUBLE PRECISION,  -- Free Cash Flow

    load_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp of data load
);
--====================================================Create Fact Income ============================================================
CREATE TABLE stock_dw.fact_income (
    income_key SERIAL PRIMARY KEY, -- Surrogate key for the fact table

    date_key INTEGER NOT NULL REFERENCES stock_dw.dim_date(date_key), -- Foreign key to dim_date, derived from end_date
    stock_key INTEGER NOT NULL REFERENCES stock_dw.dim_stock(stock_key), -- Foreign key to dim_stock, derived from symbol
    source_key INTEGER NOT NULL REFERENCES stock_dw.dim_source(source_key), -- Foreign key to dim_source

    reporting_period TEXT, -- Textual representation of the reporting period (e.g., 'FY23', 'Q1 FY24')

    -- Income Statement Metrics (nullable, source: tick_stock_income_tbls)
    q_inc_trev DOUBLE PRECISION, -- Total Revenue
    q_inc_raw TEXT,              -- Raw Material Costs (text format in source)
    q_inc_pfc TEXT,              -- Profit from Core (text format in source)
    q_inc_epc TEXT,              -- Earnings per Core (text format in source)
    q_inc_sga TEXT,              -- Selling, General & Admin Expenses (text format in source)
    q_inc_ope DOUBLE PRECISION, -- Operating Expenses
    q_inc_ebi DOUBLE PRECISION, -- Earnings Before Interest
    q_inc_dep DOUBLE PRECISION, -- Depreciation
    q_inc_pbi DOUBLE PRECISION, -- Profit Before Interest
    q_inc_ioi DOUBLE PRECISION, -- Income from Other Investments
    q_inc_pbt DOUBLE PRECISION, -- Profit Before Tax
    q_inc_toi DOUBLE PRECISION, -- Total Operating Income
    q_inc_ninc DOUBLE PRECISION, -- Net Income
    q_inc_eps DOUBLE PRECISION, -- Earnings Per Share
    q_inc_dps TEXT,              -- Dividends Per Share (text format in source)
    q_inc_pyr TEXT,              -- Payout Ratio (text format in source)

    load_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp of data load
);

--====================================================Create Fact Income ============================================================
CREATE TABLE stock_dw.fact_key_ratios (
    key_ratios_key SERIAL PRIMARY KEY, -- Surrogate key for the fact table

    date_key INTEGER NOT NULL REFERENCES stock_dw.dim_date(date_key), -- Snapshot date (from load_ts or extraction date)
    stock_key INTEGER NOT NULL REFERENCES stock_dw.dim_stock(stock_key), -- Foreign key to dim_stock
    source_key INTEGER NOT NULL REFERENCES stock_dw.dim_source(source_key), -- Foreign key to dim_source

    -- Key Ratios (nullable, source: tick_stock_key_ratios_tbls)
    risk DOUBLE PRECISION, -- Risk score or metric
    letter_3mavgvol DOUBLE PRECISION, -- 3-month average volume
    letter_4wpct DOUBLE PRECISION, -- 4-week price change percentage
    letter_52whigh DOUBLE PRECISION, -- 52-week high price
    letter_52wlow DOUBLE PRECISION, -- 52-week low price
    letter_52wpct DOUBLE PRECISION, -- 52-week price change percentage
    beta DOUBLE PRECISION, -- Beta coefficient (volatility)
    bps DOUBLE PRECISION, -- Book value per share
    div_yield DOUBLE PRECISION, -- Dividend yield
    eps DOUBLE PRECISION, -- Earnings per share
    inddy DOUBLE PRECISION, -- Industry dividend yield
    indpb DOUBLE PRECISION, -- Industry price-to-book ratio
    indpe DOUBLE PRECISION, -- Industry price-to-earnings ratio
    market_cap DOUBLE PRECISION, -- Market capitalization
    mrkt_cap_rank SMALLINT, -- Market cap rank
    pb DOUBLE PRECISION, -- Price-to-book ratio
    pe DOUBLE PRECISION, -- Price-to-earnings ratio
    roe DOUBLE PRECISION, -- Return on equity
    n_shareholders INTEGER, -- Number of shareholders
    last_price DOUBLE PRECISION, -- Last traded price
    ttm_pe DOUBLE PRECISION, -- Trailing twelve-month P/E ratio
    market_cap_label TEXT, -- Market cap category (e.g., Large Cap)
    letter_12mvol DOUBLE PRECISION, -- 12-month volume
    mrkt_capf DOUBLE PRECISION, -- Market cap (float-adjusted)
    apef DOUBLE PRECISION, -- Adjusted P/E forward
    pbr DOUBLE PRECISION, -- Price-to-book ratio (redundant, but included)
    etf_liq DOUBLE PRECISION, -- ETF liquidity score
    etf_liq_label TEXT, -- ETF liquidity category
    expense_ratio TEXT, -- Expense ratio (text format)
    track_err TEXT, -- Tracking error (text format)
    ind_expense_ratio TEXT, -- Industry average expense ratio
    ind_track_err TEXT, -- Industry average tracking error
    asst_under_man TEXT, -- Assets under management (text format)

    load_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp of data load
);


--====================================================Create Fact Recommendations ============================================================
CREATE TABLE stock_dw.fact_recommendations (
    recommendation_key SERIAL PRIMARY KEY, -- Surrogate key for the fact table

    date_key INTEGER NOT NULL REFERENCES stock_dw.dim_date(date_key), -- Snapshot or recommendation date
    stock_key INTEGER NOT NULL REFERENCES stock_dw.dim_stock(stock_key), -- Foreign key to dim_stock
    source_key INTEGER NOT NULL REFERENCES stock_dw.dim_source(source_key), -- Foreign key to dim_source

    recommendation_period TEXT, -- Period for which recommendation applies (e.g., '2024-07')

    -- Analyst Recommendation Counts (nullable, source: yfin_stock_recomendations_tbls)
    strong_buy SMALLINT, -- Number of analysts recommending 'Strong Buy'
    buy SMALLINT,        -- Number recommending 'Buy'
    hold SMALLINT,       -- Number recommending 'Hold'
    sell SMALLINT,       -- Number recommending 'Sell'
    strong_sell SMALLINT,-- Number recommending 'Strong Sell'

    load_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp of data load
);


