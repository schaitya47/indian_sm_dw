CREATE SCHEMA IF NOT EXISTS stock_landing;

-- Table: stock_landing.nifty_50_companies

-- DROP TABLE IF EXISTS stock_landing.nifty_50_companies;

CREATE TABLE IF NOT EXISTS stock_landing.nifty_50_companies
(
    company_name text COLLATE pg_catalog."default",
    industry text COLLATE pg_catalog."default",
    symbol text COLLATE pg_catalog."default" NOT NULL,
    series text COLLATE pg_catalog."default",
    isin_code text COLLATE pg_catalog."default",
    yfin_symbol text COLLATE pg_catalog."default",
    load_ts timestamp without time zone,
    CONSTRAINT nifty_50_companies_pkey PRIMARY KEY (symbol)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS stock_landing.nifty_50_companies
    OWNER to postgres;

-- Table: stock_landing.tick_stock_balance_sheet_tbls

-- DROP TABLE IF EXISTS stock_landing.tick_stock_balance_sheet_tbls;

CREATE TABLE IF NOT EXISTS stock_landing.tick_stock_balance_sheet_tbls
(
    display_period text COLLATE pg_catalog."default" NOT NULL,
    end_date text COLLATE pg_catalog."default",
    reporting text COLLATE pg_catalog."default",
    bal_csti double precision,
    bal_trec double precision,
    bal_tinv double precision,
    bal_oca double precision,
    bal_tca double precision,
    bal_netl double precision,
    bal_nppe double precision,
    bal_gint double precision,
    bal_lti double precision,
    bal_otha double precision,
    bal_tota double precision,
    bal_accp double precision,
    bal_tdep double precision,
    bal_ocl double precision,
    bal_tcl double precision,
    bal_tltd double precision,
    bal_tdeb double precision,
    bal_dit double precision,
    bal_mint double precision,
    bal_othl double precision,
    bal_totl double precision,
    bal_coms double precision,
    bal_apic double precision,
    bal_rtne double precision,
    bal_oeq double precision,
    bal_teq double precision,
    bal_tlse double precision,
    bal_tcso double precision,
    bal_tpso text COLLATE pg_catalog."default",
    bal_nca double precision,
    bal_ca double precision,
    bal_ncl double precision,
    bal_dta double precision,
    symbol text COLLATE pg_catalog."default" NOT NULL,
    load_ts text COLLATE pg_catalog."default",
    CONSTRAINT tick_stock_balance_sheet_tbls_pkey PRIMARY KEY (display_period, symbol)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS stock_landing.tick_stock_balance_sheet_tbls
    OWNER to postgres;


-- Table: stock_landing.tick_stock_cashflow_tbls

-- DROP TABLE IF EXISTS stock_landing.tick_stock_cashflow_tbls;

CREATE TABLE IF NOT EXISTS stock_landing.tick_stock_cashflow_tbls
(
    display_period text COLLATE pg_catalog."default" NOT NULL,
    end_date text COLLATE pg_catalog."default",
    reporting text COLLATE pg_catalog."default",
    caf_ciwc double precision,
    caf_cfoa double precision,
    caf_cexp double precision,
    caf_cfia double precision,
    caf_tcdp double precision,
    caf_cffa double precision,
    caf_fee text COLLATE pg_catalog."default",
    caf_ncic double precision,
    caf_fcf double precision,
    symbol text COLLATE pg_catalog."default" NOT NULL,
    load_ts text COLLATE pg_catalog."default",
    CONSTRAINT tick_stock_cashflow_tbls_pkey PRIMARY KEY (display_period, symbol)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS stock_landing.tick_stock_cashflow_tbls
    OWNER to postgres;


-- Table: stock_landing.tick_stock_dividend_history_tbls

-- DROP TABLE IF EXISTS stock_landing.tick_stock_dividend_history_tbls;

CREATE TABLE IF NOT EXISTS stock_landing.tick_stock_dividend_history_tbls
(
    id text COLLATE pg_catalog."default" NOT NULL,
    description text COLLATE pg_catalog."default",
    dividend double precision,
    ex_date text COLLATE pg_catalog."default",
    sid text COLLATE pg_catalog."default",
    _type text COLLATE pg_catalog."default",
    title text COLLATE pg_catalog."default",
    sub_type text COLLATE pg_catalog."default",
    _value text COLLATE pg_catalog."default",
    ticker text COLLATE pg_catalog."default",
    symbol text COLLATE pg_catalog."default",
    load_ts text COLLATE pg_catalog."default",
    CONSTRAINT tick_stock_dividend_history_tbls_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS stock_landing.tick_stock_dividend_history_tbls
    OWNER to postgres;

-- Table: stock_landing.tick_stock_equity_screener_tbls

-- DROP TABLE IF EXISTS stock_landing.tick_stock_equity_screener_tbls;

CREATE TABLE IF NOT EXISTS stock_landing.tick_stock_equity_screener_tbls
(
    slug text COLLATE pg_catalog."default",
    advancedratios_sector text COLLATE pg_catalog."default",
    advancedratios_subindustry text COLLATE pg_catalog."default",
    advancedratios_12mpctn double precision,
    advancedratios_26wpct double precision,
    advancedratios_4wpct double precision,
    advancedratios_4wpctn double precision,
    advancedratios_52whd double precision,
    advancedratios_52wld double precision,
    advancedratios_52wpct double precision,
    advancedratios_6mpctn double precision,
    advancedratios_acvol integer,
    advancedratios_lastprice double precision,
    advancedratios_pr1d double precision,
    advancedratios_pr1w double precision,
    advancedratios_pr1wn double precision,
    advancedratios_pravmontheva double precision,
    advancedratios_relvol double precision,
    advancedratios_vol1dchpct double precision,
    advancedratios_vol1mavg double precision,
    advancedratios_vol1wchpct double precision,
    advancedratios_vol3mavg double precision,
    advancedratios_chmuthldng6m double precision,
    advancedratios_chpromhldng6m double precision,
    advancedratios_dominsthldng double precision,
    advancedratios_dominsthldng3m double precision,
    advancedratios_dominsthldng6m double precision,
    advancedratios_forinsthldng double precision,
    advancedratios_forinsthldng3m double precision,
    advancedratios_forinsthldng6m double precision,
    advancedratios_instown double precision,
    advancedratios_instown3 double precision,
    advancedratios_promshrpled double precision,
    advancedratios_strown double precision,
    advancedratios_strown3 double precision,
    advancedratios_12mvol double precision,
    advancedratios_12mvoln double precision,
    advancedratios_3ywal double precision,
    advancedratios_3ywsh double precision,
    advancedratios_beta double precision,
    advancedratios_ccnc double precision,
    advancedratios_ftbas double precision,
    advancedratios_ftcp double precision,
    advancedratios_ftls double precision,
    advancedratios_ftoi double precision,
    advancedratios_ftvol double precision,
    advancedratios_inddy double precision,
    advancedratios_indpb double precision,
    advancedratios_indpe double precision,
    advancedratios_mrktcapf double precision,
    advancedratios_opcoi double precision,
    advancedratios_oppoi double precision,
    advancedratios_pab12mma double precision,
    advancedratios_pab1mma double precision,
    advancedratios_3ydivgwth double precision,
    advancedratios_5yaroi double precision,
    advancedratios_5ypftmrg double precision,
    advancedratios_5yrevchg double precision,
    advancedratios_5yroe double precision,
    advancedratios_5yrtnasts double precision,
    advancedratios_aint double precision,
    advancedratios_aopm double precision,
    advancedratios_aqui double precision,
    advancedratios_aroi double precision,
    advancedratios_balaccp double precision,
    advancedratios_balapic double precision,
    advancedratios_balcoms double precision,
    advancedratios_balcsti double precision,
    advancedratios_baldit double precision,
    advancedratios_baldta double precision,
    advancedratios_balgint double precision,
    advancedratios_ballti double precision,
    advancedratios_balmint double precision,
    advancedratios_balnca double precision,
    advancedratios_balncl double precision,
    advancedratios_balnetl double precision,
    advancedratios_balnppe double precision,
    advancedratios_baloca double precision,
    advancedratios_balocl double precision,
    advancedratios_balotha double precision,
    advancedratios_balothl double precision,
    advancedratios_balrtne double precision,
    advancedratios_baltca double precision,
    advancedratios_baltcl double precision,
    advancedratios_baltcso double precision,
    advancedratios_baltdeb double precision,
    advancedratios_baltdep double precision,
    advancedratios_balteq double precision,
    advancedratios_baltinv double precision,
    advancedratios_baltltd double precision,
    advancedratios_baltota double precision,
    advancedratios_baltotl double precision,
    advancedratios_baltrec double precision,
    advancedratios_cafcexp double precision,
    advancedratios_cafcffa double precision,
    advancedratios_cafcfia double precision,
    advancedratios_cafcfoa double precision,
    advancedratios_cafciwc double precision,
    advancedratios_caffcf double precision,
    advancedratios_cafncic double precision,
    advancedratios_caftcdp double precision,
    advancedratios_cfog double precision,
    advancedratios_cfotr double precision,
    advancedratios_dbteqt double precision,
    advancedratios_earnings double precision,
    advancedratios_ebitg double precision,
    advancedratios_epsgwth double precision,
    advancedratios_epsg double precision,
    advancedratios_incdep double precision,
    advancedratios_incdps double precision,
    advancedratios_incebi double precision,
    advancedratios_incepc double precision,
    advancedratios_inceps double precision,
    advancedratios_incioi double precision,
    advancedratios_incninc double precision,
    advancedratios_incope double precision,
    advancedratios_incpbi double precision,
    advancedratios_incpbt double precision,
    advancedratios_incpfc double precision,
    advancedratios_incpyr double precision,
    advancedratios_incraw double precision,
    advancedratios_incsga double precision,
    advancedratios_inctoi double precision,
    advancedratios_inctrev double precision,
    advancedratios_ldbteqt double precision,
    advancedratios_opmg double precision,
    advancedratios_pftmrg double precision,
    advancedratios_qincebik double precision,
    advancedratios_qincepsk double precision,
    advancedratios_qincninck double precision,
    advancedratios_qincopek double precision,
    advancedratios_qincpbik double precision,
    advancedratios_qincpbtk double precision,
    advancedratios_qinctrevk double precision,
    advancedratios_qcur double precision,
    advancedratios_roe double precision,
    advancedratios_rtnasts double precision,
    advancedratios_rvng double precision,
    advancedratios_apef double precision,
    advancedratios_divdps double precision,
    advancedratios_evebitd double precision,
    advancedratios_pbr double precision,
    advancedratios_ps double precision,
    advancedratios_vwap double precision,
    advancedratios_nshareholders integer,
    advancedratios_5ycafcfoamgn double precision,
    advancedratios_asstturnr double precision,
    advancedratios_balcogs double precision,
    advancedratios_cafcfoamgn double precision,
    advancedratios_erngpwrr double precision,
    advancedratios_invturnr double precision,
    advancedratios_wcturnr double precision,
    advancedratios_insholding double precision,
    advancedratios_retailholding double precision,
    advancedratios_5ycagrpct double precision,
    advancedratios_ema100d double precision,
    advancedratios_ema10d double precision,
    advancedratios_ema200d double precision,
    advancedratios_ema50d double precision,
    advancedratios_maxdrawdown double precision,
    advancedratios_sma100d double precision,
    advancedratios_sma10d double precision,
    advancedratios_sma200d double precision,
    advancedratios_sma50d double precision,
    advancedratios_bookvalue double precision,
    advancedratios_ev double precision,
    advancedratios_evbyic double precision,
    advancedratios_evbyrev double precision,
    advancedratios_evcaffcf double precision,
    advancedratios_evebit double precision,
    advancedratios_facevalue smallint,
    advancedratios_lcpcaffcf double precision,
    advancedratios_netincbylbl double precision,
    advancedratios_pricebysales double precision,
    advancedratios_pricecfor double precision,
    advancedratios_roce double precision,
    advancedratios_ttmpe double precision,
    advancedratios_lastpricesma50d double precision,
    advancedratios_lastpricesma200d double precision,
    info_name text COLLATE pg_catalog."default",
    info_ticker text COLLATE pg_catalog."default" NOT NULL,
    info_sector text COLLATE pg_catalog."default",
    advancedratios_expenseratio text COLLATE pg_catalog."default",
    advancedratios_trackerr text COLLATE pg_catalog."default",
    sid text COLLATE pg_catalog."default",
    CONSTRAINT tick_stock_equity_screener_tbls_pkey PRIMARY KEY (info_ticker)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS stock_landing.tick_stock_equity_screener_tbls
    OWNER to postgres;


-- Table: stock_landing.tick_stock_income_tbls

-- DROP TABLE IF EXISTS stock_landing.tick_stock_income_tbls;

CREATE TABLE IF NOT EXISTS stock_landing.tick_stock_income_tbls
(
    display_period text COLLATE pg_catalog."default" NOT NULL,
    end_date text COLLATE pg_catalog."default",
    reporting text COLLATE pg_catalog."default",
    q_inc_trev double precision,
    q_inc_raw text COLLATE pg_catalog."default",
    q_inc_pfc text COLLATE pg_catalog."default",
    q_inc_epc text COLLATE pg_catalog."default",
    q_inc_sga text COLLATE pg_catalog."default",
    q_inc_ope double precision,
    q_inc_ebi double precision,
    q_inc_dep double precision,
    q_inc_pbi double precision,
    q_inc_ioi double precision,
    q_inc_pbt double precision,
    q_inc_toi double precision,
    q_inc_ninc double precision,
    q_inc_eps double precision,
    q_inc_dps text COLLATE pg_catalog."default",
    q_inc_pyr text COLLATE pg_catalog."default",
    symbol text COLLATE pg_catalog."default" NOT NULL,
    load_ts text COLLATE pg_catalog."default",
    CONSTRAINT tick_stock_income_tbls_pkey PRIMARY KEY (display_period, symbol)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS stock_landing.tick_stock_income_tbls
    OWNER to postgres;

-- Table: stock_landing.tick_stock_key_ratios_tbls

-- DROP TABLE IF EXISTS stock_landing.tick_stock_key_ratios_tbls;

CREATE TABLE IF NOT EXISTS stock_landing.tick_stock_key_ratios_tbls
(
    risk double precision,
    letter_3mavgvol double precision,
    letter_4wpct double precision,
    letter_52whigh double precision,
    letter_52wlow double precision,
    letter_52wpct double precision,
    beta double precision,
    bps double precision,
    div_yield double precision,
    eps double precision,
    inddy double precision,
    indpb double precision,
    indpe double precision,
    market_cap double precision,
    mrkt_cap_rank smallint,
    pb double precision,
    pe double precision,
    roe double precision,
    n_shareholders integer,
    last_price double precision,
    ttm_pe double precision,
    market_cap_label text COLLATE pg_catalog."default",
    letter_12mvol double precision,
    mrkt_capf double precision,
    apef double precision,
    pbr double precision,
    etf_liq double precision,
    etf_liq_label text COLLATE pg_catalog."default",
    symbol text COLLATE pg_catalog."default" NOT NULL,
    load_ts text COLLATE pg_catalog."default",
    expense_ratio text COLLATE pg_catalog."default",
    track_err text COLLATE pg_catalog."default",
    ind_expense_ratio text COLLATE pg_catalog."default",
    ind_track_err text COLLATE pg_catalog."default",
    asst_under_man text COLLATE pg_catalog."default",
    CONSTRAINT tick_stock_key_ratios_tbls_pkey PRIMARY KEY (symbol)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS stock_landing.tick_stock_key_ratios_tbls
    OWNER to postgres;



-- Table: stock_landing.tick_stock_score_card_tbls

-- DROP TABLE IF EXISTS stock_landing.tick_stock_score_card_tbls;

CREATE TABLE IF NOT EXISTS stock_landing.tick_stock_score_card_tbls
(
    _name text COLLATE pg_catalog."default" NOT NULL,
    tag text COLLATE pg_catalog."default",
    _type text COLLATE pg_catalog."default",
    description text COLLATE pg_catalog."default",
    colour text COLLATE pg_catalog."default",
    _rank text COLLATE pg_catalog."default",
    peers text COLLATE pg_catalog."default",
    locked boolean,
    callout text COLLATE pg_catalog."default",
    _comment text COLLATE pg_catalog."default",
    stack smallint,
    elements jsonb,
    score_percentage boolean,
    score_max double precision,
    score_value text COLLATE pg_catalog."default",
    score_key text COLLATE pg_catalog."default",
    score text COLLATE pg_catalog."default",
    symbol text COLLATE pg_catalog."default" NOT NULL,
    load_ts text COLLATE pg_catalog."default",
    CONSTRAINT tick_stock_score_card_tbls_pkey PRIMARY KEY (_name, symbol)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS stock_landing.tick_stock_score_card_tbls
    OWNER to postgres;


-- Table: stock_landing.tick_stock_shareholding_pattern_tbls

-- DROP TABLE IF EXISTS stock_landing.tick_stock_shareholding_pattern_tbls;

CREATE TABLE IF NOT EXISTS stock_landing.tick_stock_shareholding_pattern_tbls
(
    _date text COLLATE pg_catalog."default" NOT NULL,
    data_pmpctt double precision,
    data_pmpctp double precision,
    data_plpctt double precision,
    data_uplpctt double precision,
    data_mfpctt double precision,
    data_ispctt double precision,
    data_dipctt double precision,
    data_othdipctt double precision,
    data_othexinsdipctt double precision,
    data_fipctt double precision,
    data_rhpctt double precision,
    data_othpctt double precision,
    data_rothpctt double precision,
    symbol text COLLATE pg_catalog."default" NOT NULL,
    load_ts text COLLATE pg_catalog."default",
    CONSTRAINT tick_stock_shareholding_pattern_tbls_pkey PRIMARY KEY (_date, symbol)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS stock_landing.tick_stock_shareholding_pattern_tbls
    OWNER to postgres;


-- Table: stock_landing.yfin_stock_earning_data_tbls

-- DROP TABLE IF EXISTS stock_landing.yfin_stock_earning_data_tbls;

CREATE TABLE IF NOT EXISTS stock_landing.yfin_stock_earning_data_tbls
(
    earnings_date text COLLATE pg_catalog."default" NOT NULL,
    eps_estimate double precision,
    reported_eps double precision,
    surprise double precision,
    event_type text COLLATE pg_catalog."default",
    symbol text COLLATE pg_catalog."default" NOT NULL,
    load_ts text COLLATE pg_catalog."default",
    CONSTRAINT yfin_stock_earning_data_tbls_pkey PRIMARY KEY (earnings_date, symbol)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS stock_landing.yfin_stock_earning_data_tbls
    OWNER to postgres;



-- Table: stock_landing.yfin_stock_earning_estimates_tbls

-- DROP TABLE IF EXISTS stock_landing.yfin_stock_earning_estimates_tbls;

CREATE TABLE IF NOT EXISTS stock_landing.yfin_stock_earning_estimates_tbls
(
    period text COLLATE pg_catalog."default" NOT NULL,
    _avg double precision,
    low double precision,
    high double precision,
    number_of_analysts smallint,
    year_ago_eps double precision,
    growth double precision,
    symbol text COLLATE pg_catalog."default" NOT NULL,
    load_ts text COLLATE pg_catalog."default",
    CONSTRAINT yfin_stock_earning_estimates_tbls_pkey PRIMARY KEY (symbol, period)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS stock_landing.yfin_stock_earning_estimates_tbls
    OWNER to postgres;



-- Table: stock_landing.yfin_stock_growth_estimate_tbls

-- DROP TABLE IF EXISTS stock_landing.yfin_stock_growth_estimate_tbls;

CREATE TABLE IF NOT EXISTS stock_landing.yfin_stock_growth_estimate_tbls
(
    period text COLLATE pg_catalog."default" NOT NULL,
    stock_trend double precision,
    index_trend double precision,
    symbol text COLLATE pg_catalog."default" NOT NULL,
    load_ts text COLLATE pg_catalog."default",
    CONSTRAINT yfin_stock_growth_estimate_tbls_pkey PRIMARY KEY (symbol, period)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS stock_landing.yfin_stock_growth_estimate_tbls
    OWNER to postgres;


-- Table: stock_landing.yfin_stock_history_ohlcv_tbls

-- DROP TABLE IF EXISTS stock_landing.yfin_stock_history_ohlcv_tbls;

CREATE TABLE IF NOT EXISTS stock_landing.yfin_stock_history_ohlcv_tbls
(
    _date timestamp with time zone NOT NULL,
    _open double precision,
    high double precision,
    low double precision,
    _close double precision,
    volume integer,
    dividends double precision,
    stock_splits double precision,
    symbol text COLLATE pg_catalog."default" NOT NULL,
    load_ts timestamp without time zone,
    CONSTRAINT yfin_stock_history_ohlcv_tbls_pkey PRIMARY KEY (symbol, _date)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS stock_landing.yfin_stock_history_ohlcv_tbls
    OWNER to postgres;


-- Table: stock_landing.yfin_stock_holders_tbls

-- DROP TABLE IF EXISTS stock_landing.yfin_stock_holders_tbls;

CREATE TABLE IF NOT EXISTS stock_landing.yfin_stock_holders_tbls
(
    insiders_percent_held double precision,
    institutions_percent_held double precision,
    institutions_float_percent_held double precision,
    institutions_count double precision,
    symbol text COLLATE pg_catalog."default" NOT NULL,
    load_ts text COLLATE pg_catalog."default",
    CONSTRAINT yfin_stock_holders_tbls_pkey PRIMARY KEY (symbol)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS stock_landing.yfin_stock_holders_tbls
    OWNER to postgres;

-- Table: stock_landing.yfin_stock_info_tbls

-- DROP TABLE IF EXISTS stock_landing.yfin_stock_info_tbls;

CREATE TABLE IF NOT EXISTS stock_landing.yfin_stock_info_tbls
(
    address1 text COLLATE pg_catalog."default",
    address2 text COLLATE pg_catalog."default",
    city text COLLATE pg_catalog."default",
    zip text COLLATE pg_catalog."default",
    country text COLLATE pg_catalog."default",
    phone text COLLATE pg_catalog."default",
    fax text COLLATE pg_catalog."default",
    website text COLLATE pg_catalog."default",
    industry text COLLATE pg_catalog."default",
    industry_key text COLLATE pg_catalog."default",
    industry_disp text COLLATE pg_catalog."default",
    sector text COLLATE pg_catalog."default",
    sector_key text COLLATE pg_catalog."default",
    sector_disp text COLLATE pg_catalog."default",
    long_business_summary text COLLATE pg_catalog."default",
    full_time_employees double precision,
    company_officers text COLLATE pg_catalog."default",
    audit_risk double precision,
    board_risk double precision,
    compensation_risk double precision,
    share_holder_rights_risk double precision,
    overall_risk double precision,
    governance_epoch_date double precision,
    compensation_as_of_epoch_date double precision,
    ir_website text COLLATE pg_catalog."default",
    executive_team text COLLATE pg_catalog."default",
    max_age integer,
    price_hint smallint,
    previous_close double precision,
    _open double precision,
    day_low double precision,
    day_high double precision,
    regular_market_previous_close double precision,
    regular_market_open double precision,
    regular_market_day_low double precision,
    regular_market_day_high double precision,
    dividend_rate double precision,
    dividend_yield double precision,
    ex_dividend_date double precision,
    payout_ratio double precision,
    five_year_avg_dividend_yield double precision,
    beta double precision,
    trailing_p_e double precision,
    volume integer,
    regular_market_volume integer,
    average_volume integer,
    averagevolume10days integer,
    averagedailyvolume10day integer,
    bid double precision,
    ask double precision,
    bid_size double precision,
    ask_size double precision,
    market_cap bigint,
    fifty_two_week_low double precision,
    fifty_two_week_high double precision,
    pricetosalestrailing12months double precision,
    fifty_day_average double precision,
    two_hundred_day_average double precision,
    trailing_annual_dividend_rate double precision,
    trailing_annual_dividend_yield double precision,
    currency text COLLATE pg_catalog."default",
    tradeable boolean,
    enterprise_value bigint,
    forward_p_e double precision,
    profit_margins double precision,
    float_shares bigint,
    shares_outstanding bigint,
    held_percent_insiders double precision,
    held_percent_institutions double precision,
    implied_shares_outstanding bigint,
    book_value double precision,
    price_to_book double precision,
    last_fiscal_year_end integer,
    next_fiscal_year_end integer,
    most_recent_quarter integer,
    earnings_quarterly_growth double precision,
    net_income_to_common bigint,
    trailing_eps double precision,
    last_split_factor text COLLATE pg_catalog."default",
    last_split_date double precision,
    enterprise_to_revenue double precision,
    enterprise_to_ebitda double precision,
    letter_52weekchange double precision,
    sandp52weekchange double precision,
    last_dividend_value double precision,
    last_dividend_date double precision,
    quote_type text COLLATE pg_catalog."default",
    current_price double precision,
    target_high_price double precision,
    target_low_price double precision,
    target_mean_price double precision,
    target_median_price double precision,
    recommendation_mean double precision,
    recommendation_key text COLLATE pg_catalog."default",
    number_of_analyst_opinions smallint,
    total_cash bigint,
    total_cash_per_share double precision,
    ebitda double precision,
    total_debt bigint,
    quick_ratio double precision,
    current_ratio double precision,
    total_revenue bigint,
    debt_to_equity double precision,
    revenue_per_share double precision,
    return_on_assets double precision,
    return_on_equity double precision,
    gross_profits bigint,
    free_cashflow double precision,
    operating_cashflow double precision,
    earnings_growth double precision,
    revenue_growth double precision,
    gross_margins double precision,
    ebitda_margins double precision,
    operating_margins double precision,
    financial_currency text COLLATE pg_catalog."default",
    symbol text COLLATE pg_catalog."default" NOT NULL,
    _language text COLLATE pg_catalog."default",
    region text COLLATE pg_catalog."default",
    type_disp text COLLATE pg_catalog."default",
    quote_source_name text COLLATE pg_catalog."default",
    triggerable boolean,
    custom_price_alert_confidence text COLLATE pg_catalog."default",
    regular_market_change double precision,
    regular_market_day_range text COLLATE pg_catalog."default",
    full_exchange_name text COLLATE pg_catalog."default",
    averagedailyvolume3month integer,
    fifty_two_week_low_change double precision,
    fifty_two_week_low_change_percent double precision,
    fifty_two_week_range text COLLATE pg_catalog."default",
    fifty_two_week_high_change double precision,
    fifty_two_week_high_change_percent double precision,
    fifty_two_week_change_percent double precision,
    earnings_timestamp double precision,
    earnings_timestamp_start integer,
    earnings_timestamp_end integer,
    earnings_call_timestamp_start double precision,
    earnings_call_timestamp_end double precision,
    is_earnings_date_estimate boolean,
    eps_trailing_twelve_months double precision,
    eps_current_year double precision,
    price_eps_current_year double precision,
    fifty_day_average_change double precision,
    fifty_day_average_change_percent double precision,
    two_hundred_day_average_change double precision,
    two_hundred_day_average_change_percent double precision,
    source_interval smallint,
    exchange_data_delayed_by smallint,
    average_analyst_rating text COLLATE pg_catalog."default",
    crypto_tradeable boolean,
    long_name text COLLATE pg_catalog."default",
    corporate_actions text COLLATE pg_catalog."default",
    regular_market_time integer,
    exchange text COLLATE pg_catalog."default",
    message_board_id text COLLATE pg_catalog."default",
    exchange_timezone_name text COLLATE pg_catalog."default",
    exchange_timezone_short_name text COLLATE pg_catalog."default",
    gmt_off_set_milliseconds integer,
    market text COLLATE pg_catalog."default",
    esg_populated boolean,
    regular_market_change_percent double precision,
    regular_market_price double precision,
    market_state text COLLATE pg_catalog."default",
    short_name text COLLATE pg_catalog."default",
    has_pre_post_market_data boolean,
    first_trade_date_milliseconds bigint,
    load_ts timestamp without time zone,
    forward_eps double precision,
    eps_forward double precision,
    trailing_peg_ratio double precision,
    CONSTRAINT yfin_stock_info_tbls_pkey PRIMARY KEY (symbol),
    -- CONSTRAINT uniquestock_landing_yfin_stock_info_tbls_symbol UNIQUE (symbol)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS stock_landing.yfin_stock_info_tbls
    OWNER to postgres;


-- Table: stock_landing.yfin_stock_recomendations_tbls

-- DROP TABLE IF EXISTS stock_landing.yfin_stock_recomendations_tbls;

CREATE TABLE IF NOT EXISTS stock_landing.yfin_stock_recomendations_tbls
(
    period text COLLATE pg_catalog."default" NOT NULL,
    strong_buy smallint,
    buy smallint,
    _hold smallint,
    sell smallint,
    strong_sell smallint,
    symbol text COLLATE pg_catalog."default" NOT NULL,
    load_ts text COLLATE pg_catalog."default",
    CONSTRAINT yfin_stock_recomendations_tbls_pkey PRIMARY KEY (period, symbol)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS stock_landing.yfin_stock_recomendations_tbls
    OWNER to postgres;

-- Table: stock_landing.nse_stock_history_ohlcv_tbls

-- DROP TABLE IF EXISTS stock_landing.nse_stock_history_ohlcv_tbls;

CREATE TABLE IF NOT EXISTS stock_landing.nse_stock_history_ohlcv_tbls
(
    _timestamp timestamp without time zone NOT NULL,
    _open double precision,
    high double precision,
    low double precision,
    _close double precision,
    volume bigint,
    symbol text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT nse_stock_history_ohlcv_tbls_pkey PRIMARY KEY (_timestamp, symbol)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS stock_landing.nse_stock_history_ohlcv_tbls
    OWNER to postgres;
    
-- Table: stock_landing.stage_load_control

-- DROP TABLE IF EXISTS stock_landing.stage_load_control;

CREATE TABLE IF NOT EXISTS stock_landing.stage_load_control
(
    pipeline_name character varying(50) COLLATE pg_catalog."default" NOT NULL,
    last_success_timestamp timestamp without time zone,
    status character varying(20) COLLATE pg_catalog."default" DEFAULT 'READY'::character varying,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT stage_load_control_pkey PRIMARY KEY (pipeline_name)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS stock_landing.stage_load_control
    OWNER to postgres;

UPDATE stock_landing.stage_load_control 
SET last_success_timestamp = '1995-01-01 00:00:00' 
WHERE last_success_timestamp IS NULL;

INSERT INTO stock_landing.stage_load_control (pipeline_name)
VALUES 
  ('get_nifty50_companies'),
  ('nse_landing_daily'),
  ('tick_landing_monthly'),
  ('yfin_landing_daliy'),
  ('yfin_landing_monthly'),
  ('yfin_landing_weekly');