SELECT
    -- cashflow_key is SERIAL PRIMARY KEY in target, so not selected here
    dd.date_key AS date_key, -- Join to dim_date on end_date
    ds.stock_key AS stock_key, -- Join to dim_stock on symbol
    dsrc.source_key AS source_key, -- Join to dim_source (define your join logic)
    tsct.display_period AS reporting_period,
    tsct.caf_ciwc,
    tsct.caf_cfoa,
    tsct.caf_cexp,
    tsct.caf_cfia,
    tsct.caf_tcdp,
    tsct.caf_cffa,
    tsct.caf_fee,
    tsct.caf_ncic,
    tsct.caf_fcf,
    (CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Kolkata')::timestamp AS load_ts
FROM stock_landing.tick_stock_cashflow_tbls tsct
INNER JOIN stock_dw.dim_date dd
    ON dd.nk_full_date = tsct.end_date -- or your date mapping logic
INNER JOIN stock_dw.dim_stock ds
    ON ds.nk_symbol = tsct.symbol
INNER JOIN stock_dw.dim_source dsrc
    ON dsrc.source_name = 'TICK'
WHERE tsct.load_ts > (SELECT last_success_timestamp FROM {{ df_1 }})