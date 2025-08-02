INSERT INTO stock_dw.fact_income (
    date_key,
    stock_key,
    source_key,
    reporting_period,
    q_inc_trev,
    q_inc_raw,
    q_inc_pfc,
    q_inc_epc,
    q_inc_sga,
    q_inc_ope,
    q_inc_ebi,
    q_inc_dep,
    q_inc_pbi,
    q_inc_ioi,
    q_inc_pbt,
    q_inc_toi,
    q_inc_ninc,
    q_inc_eps,
    q_inc_dps,
    q_inc_pyr,
    load_ts
)
SELECT
    date_key,
    stock_key,
    source_key,
    reporting_period,
    q_inc_trev,
    q_inc_raw,
    q_inc_pfc,
    q_inc_epc,
    q_inc_sga,
    q_inc_ope,
    q_inc_ebi,
    q_inc_dep,
    q_inc_pbi,
    q_inc_ioi,
    q_inc_pbt,
    q_inc_toi,
    q_inc_ninc,
    q_inc_eps,
    q_inc_dps,
    q_inc_pyr,
    load_ts
FROM {{ df_1 }}
ON CONFLICT (date_key, stock_key, source_key,reporting_period)
DO UPDATE SET
    reporting_period = EXCLUDED.reporting_period,
    q_inc_trev = EXCLUDED.q_inc_trev,
    q_inc_raw = EXCLUDED.q_inc_raw,
    q_inc_pfc = EXCLUDED.q_inc_pfc,
    q_inc_epc = EXCLUDED.q_inc_epc,
    q_inc_sga = EXCLUDED.q_inc_sga,
    q_inc_ope = EXCLUDED.q_inc_ope,
    q_inc_ebi = EXCLUDED.q_inc_ebi,
    q_inc_dep = EXCLUDED.q_inc_dep,
    q_inc_pbi = EXCLUDED.q_inc_pbi,
    q_inc_ioi = EXCLUDED.q_inc_ioi,
    q_inc_pbt = EXCLUDED.q_inc_pbt,
    q_inc_toi = EXCLUDED.q_inc_toi,
    q_inc_ninc = EXCLUDED.q_inc_ninc,
    q_inc_eps = EXCLUDED.q_inc_eps,
    q_inc_dps = EXCLUDED.q_inc_dps,
    q_inc_pyr = EXCLUDED.q_inc_pyr,
    load_ts = EXCLUDED.load_ts
WHERE
    fact_income.reporting_period IS DISTINCT FROM EXCLUDED.reporting_period OR
    fact_income.q_inc_trev IS DISTINCT FROM EXCLUDED.q_inc_trev OR
    fact_income.q_inc_raw IS DISTINCT FROM EXCLUDED.q_inc_raw OR
    fact_income.q_inc_pfc IS DISTINCT FROM EXCLUDED.q_inc_pfc OR
    fact_income.q_inc_epc IS DISTINCT FROM EXCLUDED.q_inc_epc OR
    fact_income.q_inc_sga IS DISTINCT FROM EXCLUDED.q_inc_sga OR
    fact_income.q_inc_ope IS DISTINCT FROM EXCLUDED.q_inc_ope OR
    fact_income.q_inc_ebi IS DISTINCT FROM EXCLUDED.q_inc_ebi OR
    fact_income.q_inc_dep IS DISTINCT FROM EXCLUDED.q_inc_dep OR
    fact_income.q_inc_pbi IS DISTINCT FROM EXCLUDED.q_inc_pbi OR
    fact_income.q_inc_ioi IS DISTINCT FROM EXCLUDED.q_inc_ioi OR
    fact_income.q_inc_pbt IS DISTINCT FROM EXCLUDED.q_inc_pbt OR
    fact_income.q_inc_toi IS DISTINCT FROM EXCLUDED.q_inc_toi OR
    fact_income.q_inc_ninc IS DISTINCT FROM EXCLUDED.q_inc_ninc OR
    fact_income.q_inc_eps IS DISTINCT FROM EXCLUDED.q_inc_eps OR
    fact_income.q_inc_dps IS DISTINCT FROM EXCLUDED.q_inc_dps OR
    fact_income.q_inc_pyr IS DISTINCT FROM EXCLUDED.q_inc_pyr;