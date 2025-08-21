SELECT
    dd.date_key AS date_key,  -- from end_date
    ds.stock_key AS stock_key,  -- from symbol
    dsrc.source_key AS source_key,  -- you must define how to join to dim_source
    tsit.display_period AS reporting_period,
    tsit.q_inc_trev,
    tsit.q_inc_raw,
    tsit.q_inc_pfc,
    tsit.q_inc_epc,
    tsit.q_inc_sga,
    tsit.q_inc_ope,
    tsit.q_inc_ebi,
    tsit.q_inc_dep,
    tsit.q_inc_pbi,
    tsit.q_inc_ioi,
    tsit.q_inc_pbt,
    tsit.q_inc_toi,
    tsit.q_inc_ninc,
    tsit.q_inc_eps,
    tsit.q_inc_dps,
    tsit.q_inc_pyr,
    (CURRENT_TIMESTAMP)::timestamp AS load_ts
FROM stock_landing.tick_stock_income_tbls tsit
INNER JOIN stock_dw.dim_date dd
    ON dd.nk_full_date = tsit.end_date
INNER JOIN stock_dw.dim_stock ds
    ON ds.nk_symbol = tsit.symbol
INNER JOIN stock_dw.dim_source dsrc
    ON dsrc.source_name = 'TICK'
WHERE tsit.load_ts > (SELECT last_success_timestamp FROM {{ df_1 }})