-- This script is used to test the nse_stock_history_ohlcv_tbls table in the landing layer
-- It checks for duplicate entries based on timestamp and symbol
SELECT _timestamp, symbol, count(*) FROM stock_landing.nse_stock_history_ohlcv_tbls
group by 1,2
having count(*) > 1;

SELECT _date, symbol
FROM stock_landing.yfin_stock_history_ohlcv_tbls
group by 1,2
having count(*) > 1;

-- Check for duplicates for all the tick tables
SELECT 'tick_stock_balance_sheet_tbls' AS table_name, display_period::text AS key1, symbol AS key2, NULL AS key3, COUNT(*) AS duplicate_count
FROM stock_landing.tick_stock_balance_sheet_tbls
GROUP BY display_period, symbol
HAVING COUNT(*) > 1
UNION ALL
SELECT 'tick_stock_cashflow_tbls', display_period::text, symbol, NULL, COUNT(*)
FROM stock_landing.tick_stock_cashflow_tbls
GROUP BY display_period, symbol
HAVING COUNT(*) > 1
UNION ALL
SELECT 'tick_stock_dividend_history_tbls', id, NULL, NULL, COUNT(*)
FROM stock_landing.tick_stock_dividend_history_tbls
GROUP BY id
HAVING COUNT(*) > 1
UNION ALL
SELECT 'tick_stock_equity_screener_tbls', info_ticker, NULL, NULL, COUNT(*)
FROM stock_landing.tick_stock_equity_screener_tbls
GROUP BY info_ticker
HAVING COUNT(*) > 1
UNION ALL
SELECT 'tick_stock_income_tbls', display_period::text, symbol, NULL, COUNT(*)
FROM stock_landing.tick_stock_income_tbls
GROUP BY display_period, symbol
HAVING COUNT(*) > 1
UNION ALL
SELECT 'tick_stock_key_ratios_tbls', symbol, NULL, NULL, COUNT(*)
FROM stock_landing.tick_stock_key_ratios_tbls
GROUP BY symbol
HAVING COUNT(*) > 1
UNION ALL
SELECT 'tick_stock_score_card_tbls', _name, symbol, NULL, COUNT(*)
FROM stock_landing.tick_stock_score_card_tbls
GROUP BY _name, symbol
HAVING COUNT(*) > 1
UNION ALL
SELECT 'tick_stock_shareholding_pattern_tbls', _date, symbol, NULL, COUNT(*)
FROM stock_landing.tick_stock_shareholding_pattern_tbls
GROUP BY _date, symbol
HAVING COUNT(*) > 1;

