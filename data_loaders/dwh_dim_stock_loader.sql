    SELECT
    symbol AS nk_symbol,
    company_name,
    industry,
    series,
    isin_code,
    symbol || '.NS' AS symbol_ns,
    (CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Kolkata')::timestamp AS load_ts
FROM
    stock_landing.nifty_50_companies g
WHERE load_ts > (
    SELECT
        last_success_timestamp
    FROM
        {{ df_1 }}
)
