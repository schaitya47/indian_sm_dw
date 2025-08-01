INSERT INTO stock_dw.dim_stock (
    nk_symbol,
    company_name,
    industry,
    series,
    isin_code,
    yfin_symbol,
    load_ts
)
SELECT
    nk_symbol,
    company_name,
    industry,
    series,
    isin_code,
    symbol_ns AS yfin_symbol,
    load_ts
FROM {{ df_1 }}
ON CONFLICT (nk_symbol)
DO UPDATE SET
    company_name = EXCLUDED.company_name,
    industry = EXCLUDED.industry,
    series = EXCLUDED.series,
    isin_code = EXCLUDED.isin_code,
    yfin_symbol = EXCLUDED.yfin_symbol,
    load_ts = EXCLUDED.load_ts
WHERE
    dim_stock.company_name IS DISTINCT FROM EXCLUDED.company_name OR
    dim_stock.industry IS DISTINCT FROM EXCLUDED.industry OR
    dim_stock.series IS DISTINCT FROM EXCLUDED.series OR
    dim_stock.isin_code IS DISTINCT FROM EXCLUDED.isin_code OR
    dim_stock.yfin_symbol IS DISTINCT FROM EXCLUDED.yfin_symbol;
