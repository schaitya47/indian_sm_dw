SELECT
    dd.date_key AS date_key,  -- from end_date
    ds.stock_key AS stock_key,  -- from symbol
    dsrc.source_key AS source_key,  -- you must define how to join to dim_source
    src.display_period AS reporting_period,
    src.q_inc_trev,
    src.q_inc_raw,
    src.q_inc_pfc,
    src.q_inc_epc,
    src.q_inc_sga,
    src.q_inc_ope,
    src.q_inc_ebi,
    src.q_inc_dep,
    src.q_inc_pbi,
    src.q_inc_ioi,
    src.q_inc_pbt,
    src.q_inc_toi,
    src.q_inc_ninc,
    src.q_inc_eps,
    src.q_inc_dps,
    src.q_inc_pyr,
    src.load_ts
FROM stock_landing.tick_stock_income_tbls src
INNER JOIN stock_dw.dim_date dd
    ON dd.nk_full_date = src.end_date
INNER JOIN stock_dw.dim_stock ds
    ON ds.nk_symbol = src.symbol
INNER JOIN stock_dw.dim_source dsrc
    ON dsrc.source_name = 'TICK'
WHERE src.load_ts > (SELECT last_success_timestamp FROM {{ df_1 }})