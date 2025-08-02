SELECT
    -- cashflow_key is SERIAL PRIMARY KEY in target, so not selected here
    d.date_key AS date_key, -- Join to dim_date on end_date
    s.stock_key AS stock_key, -- Join to dim_stock on symbol
    src.source_key AS source_key, -- Join to dim_source (define your join logic)
    t.display_period AS reporting_period,
    t.caf_ciwc,
    t.caf_cfoa,
    t.caf_cexp,
    t.caf_cfia,
    t.caf_tcdp,
    t.caf_cffa,
    t.caf_fee,
    t.caf_ncic,
    t.caf_fcf,
    t.load_ts
FROM stock_landing.tick_stock_cashflow_tbls t
INNER JOIN stock_dw.dim_date d
    ON d.nk_full_date = t.end_date -- or your date mapping logic
INNER JOIN stock_dw.dim_stock s
    ON s.nk_symbol = t.symbol
INNER JOIN stock_dw.dim_source src
    ON src.source_name = 'TICK'
WHERE t.load_ts > (SELECT last_success_timestamp FROM {{ df_1 }})