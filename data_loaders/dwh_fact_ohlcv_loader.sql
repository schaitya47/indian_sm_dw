-- Docs: https://docs.mage.ai/guides/sql-blocks
SELECT
    d.date_key,
    s.stock_key,
    src.source_key,
    y._open AS open_price,
    y.high,
    y.low,
    y._close AS close_price,
    y.volume,
    y.dividends,
    y.stock_splits,
    y.load_ts
FROM stock_landing.yfin_stock_history_ohlcv_tbls y
JOIN stock_dw.dim_date d ON d.nk_full_date = y._date::date
JOIN stock_dw.dim_stock s ON s.nk_symbol = y.symbol
JOIN stock_dw.dim_source src ON src.source_name = 'YFIN'

union all 
SELECT
    d.date_key,
    s.stock_key,
    src.source_key,
    n._open AS open_price,
    n.high,
    n.low,
    n._close AS close_price,
    n.volume,
    NULL AS dividends,
    NULL AS stock_splits,
    CURRENT_TIMESTAMP AS load_ts
FROM stock_landing.nse_stock_history_ohlcv_tbls n
JOIN stock_dw.dim_date d ON d.nk_full_date = n._timestamp::date
JOIN stock_dw.dim_stock s ON s.nk_symbol = n.symbol
JOIN stock_dw.dim_source src ON src.source_name = 'NSE'
