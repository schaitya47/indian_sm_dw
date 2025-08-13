SELECT
    dd.date_key AS date_key,  -- from load_ts
    ds.stock_key AS stock_key,  -- from symbol
    dsrc.source_key AS source_key,  -- you must define how to join to dim_source
    src.risk,
    src.letter_3mavgvol,
    src.letter_4wpct,
    src.letter_52whigh,
    src.letter_52wlow,
    src.letter_52wpct,
    src.beta,
    src.bps,
    src.div_yield,
    src.eps,
    src.inddy,
    src.indpb,
    src.indpe,
    src.market_cap,
    src.mrkt_cap_rank,
    src.pb,
    src.pe,
    src.roe,
    src.n_shareholders,
    src.last_price,
    src.ttm_pe,
    src.market_cap_label,
    src.letter_12mvol,
    src.mrkt_capf,
    src.apef,
    src.pbr,
    src.etf_liq,
    src.etf_liq_label,
    src.expense_ratio,
    src.track_err,
    src.ind_expense_ratio,
    src.ind_track_err,
    src.asst_under_man,
    src.load_ts
FROM stock_landing.tick_stock_key_ratios_tbls src
INNER JOIN stock_dw.dim_stock ds
    ON ds.nk_symbol = src.symbol
INNER JOIN stock_dw.dim_date dd
    ON dd.nk_full_date = src.load_ts::date  -- adjust if your dim_date uses a different field
INNER JOIN stock_dw.dim_source dsrc
    ON dsrc.source_name = 'TICK'  -- adjust as needed for your source dimension
WHERE src.load_ts > (SELECT last_success_timestamp FROM {{ df_1 }})
