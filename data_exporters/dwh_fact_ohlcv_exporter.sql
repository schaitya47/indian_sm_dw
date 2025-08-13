INSERT INTO stock_dw.fact_ohlcv (
    date_key,
    stock_key,
    source_key,
    open_price,
    high_price,
    low_price,
    close_price,
    volume,
    dividends,
    stock_splits,
    load_ts
)
SELECT
    date_key,
    stock_key,
    source_key,
    open_price,
    high as high_price,
    low as low_price,
    close_price,
    volume,
    dividends,
    stock_splits,
    load_ts
FROM {{ df_1 }}
ON CONFLICT (date_key, stock_key, source_key)
DO UPDATE SET
    open_price = EXCLUDED.open_price,
    high_price = EXCLUDED.high_price,
    low_price = EXCLUDED.low_price,
    close_price = EXCLUDED.close_price,
    volume = EXCLUDED.volume,
    dividends = EXCLUDED.dividends,
    stock_splits = EXCLUDED.stock_splits,
    load_ts = EXCLUDED.load_ts
WHERE
    fact_ohlcv.open_price IS DISTINCT FROM EXCLUDED.open_price OR
    fact_ohlcv.high_price IS DISTINCT FROM EXCLUDED.high_price OR
    fact_ohlcv.low_price IS DISTINCT FROM EXCLUDED.low_price OR
    fact_ohlcv.close_price IS DISTINCT FROM EXCLUDED.close_price OR
    fact_ohlcv.volume IS DISTINCT FROM EXCLUDED.volume OR
    fact_ohlcv.dividends IS DISTINCT FROM EXCLUDED.dividends OR
    fact_ohlcv.stock_splits IS DISTINCT FROM EXCLUDED.stock_splits;

