INSERT INTO stock_dw.fact_cashflow (
    date_key,
    stock_key,
    source_key,
    reporting_period,
    caf_ciwc,
    caf_cfoa,
    caf_cexp,
    caf_cfia,
    caf_tcdp,
    caf_cffa,
    caf_fee,
    caf_ncic,
    caf_fcf,
    load_ts
)
SELECT
    date_key,
    stock_key,
    source_key, 
    reporting_period,
    caf_ciwc,
    caf_cfoa,
    caf_cexp,
    caf_cfia,
    caf_tcdp,
    caf_cffa,
    caf_fee,
    caf_ncic,
    caf_fcf,
    CURRENT_TIMESTAMP
FROM {{ df_1 }}
ON CONFLICT (date_key, stock_key, source_key, reporting_period)
DO UPDATE SET
    caf_ciwc = EXCLUDED.caf_ciwc,
    caf_cfoa = EXCLUDED.caf_cfoa,
    caf_cexp = EXCLUDED.caf_cexp,
    caf_cfia = EXCLUDED.caf_cfia,
    caf_tcdp = EXCLUDED.caf_tcdp,
    caf_cffa = EXCLUDED.caf_cffa,
    caf_fee = EXCLUDED.caf_fee,
    caf_ncic = EXCLUDED.caf_ncic,
    caf_fcf = EXCLUDED.caf_fcf,
    load_ts = CURRENT_TIMESTAMP
WHERE
     fact_cashflow.caf_ciwc IS DISTINCT FROM EXCLUDED.caf_ciwc OR
     fact_cashflow.caf_cfoa IS DISTINCT FROM EXCLUDED.caf_cfoa OR
     fact_cashflow.caf_cexp IS DISTINCT FROM EXCLUDED.caf_cexp OR
     fact_cashflow.caf_cfia IS DISTINCT FROM EXCLUDED.caf_cfia OR
     fact_cashflow.caf_tcdp IS DISTINCT FROM EXCLUDED.caf_tcdp OR
     fact_cashflow.caf_cffa IS DISTINCT FROM EXCLUDED.caf_cffa OR
     fact_cashflow.caf_fee IS DISTINCT FROM EXCLUDED.caf_fee OR
     fact_cashflow.caf_ncic IS DISTINCT FROM EXCLUDED.caf_ncic OR
     fact_cashflow.caf_fcf IS DISTINCT FROM EXCLUDED.caf_fcf;
    