-- Docs: https://docs.mage.ai/guides/sql-blocks
SELECT
    -- Surrogate key is SERIAL in target, so omit in SELECT (auto-generated)
    dd.date_key, -- get from dim_date
    -- You must join to dim_stock to get stock_key from symbol
    ds.stock_key,
    -- You must join to dim_source to get source_key (set as needed, e.g., TICK)
    dsrc.source_key,
    reporting AS reporting_period,
    bal_csti,
    bal_trec,
    bal_tinv,
    bal_oca,
    bal_tca,
    bal_netl,
    bal_nppe,
    bal_gint,
    bal_lti,
    bal_otha,
    bal_tota,
    bal_accp,
    bal_tdep,
    bal_ocl,
    bal_tcl,
    bal_tltd,
    bal_tdeb,
    bal_dit,
    bal_mint,
    bal_othl,
    bal_totl,
    bal_coms,
    bal_apic,
    bal_rtne,
    bal_oeq,
    bal_teq,
    bal_tlse,
    bal_tcso,
    bal_tpso,
    bal_nca,
    bal_ca,
    bal_ncl,
    bal_dta,
    -- Convert load_ts text to timestamp if needed
    (CURRENT_TIMESTAMP)::timestamp AS load_ts
FROM stock_landing.tick_stock_balance_sheet_tbls tsbst
INNER JOIN stock_dw.dim_stock ds ON tsbst.symbol = ds.nk_symbol
INNER JOIN stock_dw.dim_source dsrc ON dsrc.source_name = 'TICK'
INNER JOIN stock_dw.dim_date dd ON tsbst.end_date::date = dd.nk_full_date    
WHERE tsbst.load_ts > (SELECT last_success_timestamp FROM {{ df_1 }})