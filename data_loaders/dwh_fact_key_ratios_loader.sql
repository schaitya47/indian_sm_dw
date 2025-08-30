SELECT
    dd.date_key AS date_key,  -- from load_ts
    ds.stock_key AS stock_key,  -- from symbol
    dsrc.source_key AS source_key,  -- you must define how to join to dim_source
    tskrt.risk,
    tskrt.letter_3mavgvol,
    tskrt.letter_4wpct,
    tskrt.letter_52whigh,
    tskrt.letter_52wlow,
    tskrt.letter_52wpct,
    tskrt.beta,
    tskrt.bps,
    tskrt.div_yield,
    tskrt.eps,
    tskrt.inddy,
    tskrt.indpb,
    tskrt.indpe,
    tskrt.market_cap,
    tskrt.mrkt_cap_rank,
    tskrt.pb,
    tskrt.pe,
    tskrt.roe,
    tskrt.n_shareholders,
    tskrt.last_price,
    tskrt.ttm_pe,
    tskrt.market_cap_label,
    tskrt.letter_12mvol,
    tskrt.mrkt_capf,
    tskrt.apef,
    tskrt.pbr,
    tskrt.etf_liq,
    tskrt.etf_liq_label,
    tskrt.expense_ratio,
    tskrt.track_err,
    tskrt.ind_expense_ratio,
    tskrt.ind_track_err,
    tskrt.asst_under_man,
    (CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Kolkata')::timestamp AS load_ts
FROM stock_landing.tick_stock_key_ratios_tbls tskrt
INNER JOIN stock_dw.dim_stock ds
    ON ds.nk_symbol = tskrt.symbol
INNER JOIN stock_dw.dim_date dd
    ON dd.nk_full_date = tskrt.load_ts::date  -- adjust if your dim_date uses a different field
INNER JOIN stock_dw.dim_source dsrc
    ON dsrc.source_name = 'TICK'  -- adjust as needed for your source dimension
WHERE tskrt.load_ts > (SELECT last_success_timestamp FROM {{ df_1 }})
