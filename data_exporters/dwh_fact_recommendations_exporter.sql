INSERT INTO stock_dw.fact_recommendations (
    date_key,
    stock_key,
    source_key,
    recommendation_period,
    strong_buy,
    buy,
    hold,
    sell,
    strong_sell,
    load_ts
)
SELECT
    date_key,
    stock_key,
    source_key,
    recommendation_period,
    strong_buy,
    buy,
    _hold,
    sell,
    strong_sell,
    load_ts
FROM {{ df_1 }}
ON CONFLICT (date_key, stock_key, source_key, recommendation_period)
DO UPDATE SET
    strong_buy = EXCLUDED.strong_buy,
    buy = EXCLUDED.buy,
    hold = EXCLUDED.hold,
    sell = EXCLUDED.sell,
    strong_sell = EXCLUDED.strong_sell,
    load_ts = EXCLUDED.load_ts
WHERE
    fact_recommendations.strong_buy IS DISTINCT FROM EXCLUDED.strong_buy OR
    fact_recommendations.buy IS DISTINCT FROM EXCLUDED.buy OR
    fact_recommendations.hold IS DISTINCT FROM EXCLUDED.hold OR
    fact_recommendations.sell IS DISTINCT FROM EXCLUDED.sell OR
    fact_recommendations.strong_sell IS DISTINCT FROM EXCLUDED.strong_sell;
