SELECT
    dd.date_key AS date_key,
    ds.stock_key AS stock_key,
    dsrc.source_key AS source_key,
    (date_trunc('month', ysrt.load_ts::date) + (CAST(REPLACE(ysrt.period, 'm', '') AS INTEGER) * INTERVAL '1 month'))::date AS recommendation_period,
    ysrt.buy,
    ysrt._hold,
    ysrt.sell,
    ysrt.strong_buy,
    ysrt.strong_sell,
    (CURRENT_TIMESTAMP)::timestamp AS load_ts
FROM stock_landing.yfin_stock_recomendations_tbls src
INNER JOIN stock_dw.dim_stock ds
    ON ds.nk_symbol = ysrt.symbol
INNER JOIN stock_dw.dim_date dd
    ON dd.nk_full_date = (date_trunc('month', ysrt.load_ts::date) + (CAST(REPLACE(ysrt.period, 'm', '') AS INTEGER) * INTERVAL '1 month'))::date
INNER JOIN stock_dw.dim_source dsrc
    ON dsrc.source_name = 'YFIN'
WHERE ysrt.load_ts > (SELECT last_success_timestamp FROM {{ df_1 }})