INSERT INTO stock_dw.fact_balance_sheet (
    date_key,
    stock_key,
    source_key,
    reporting_period,
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
    load_ts
)
select
    date_key,
    stock_key,
    source_key,
    reporting_period,
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
    CURRENT_TIMESTAMP
FROM {{ df_1 }}
ON CONFLICT (date_key, stock_key, source_key, reporting_period)
DO UPDATE SET
    bal_csti = EXCLUDED.bal_csti,
    bal_trec = EXCLUDED.bal_trec,
    bal_tinv = EXCLUDED.bal_tinv,
    bal_oca = EXCLUDED.bal_oca,
    bal_tca = EXCLUDED.bal_tca,
    bal_netl = EXCLUDED.bal_netl,
    bal_nppe = EXCLUDED.bal_nppe,
    bal_gint = EXCLUDED.bal_gint,
    bal_lti = EXCLUDED.bal_lti,
    bal_otha = EXCLUDED.bal_otha,
    bal_tota = EXCLUDED.bal_tota,
    bal_accp = EXCLUDED.bal_accp,
    bal_tdep = EXCLUDED.bal_tdep,
    bal_ocl = EXCLUDED.bal_ocl,
    bal_tcl = EXCLUDED.bal_tcl,
    bal_tltd = EXCLUDED.bal_tltd,
    bal_tdeb = EXCLUDED.bal_tdeb,
    bal_dit = EXCLUDED.bal_dit,
    bal_mint = EXCLUDED.bal_mint,
    bal_othl = EXCLUDED.bal_othl,
    bal_totl = EXCLUDED.bal_totl,
    bal_coms = EXCLUDED.bal_coms,
    bal_apic = EXCLUDED.bal_apic,
    bal_rtne = EXCLUDED.bal_rtne,
    bal_oeq = EXCLUDED.bal_oeq,
    bal_teq = EXCLUDED.bal_teq,
    bal_tlse = EXCLUDED.bal_tlse,
    bal_tcso = EXCLUDED.bal_tcso,
    bal_tpso = EXCLUDED.bal_tpso,
    bal_nca = EXCLUDED.bal_nca,
    bal_ca = EXCLUDED.bal_ca,
    bal_ncl = EXCLUDED.bal_ncl,
    bal_dta = EXCLUDED.bal_dta,
    load_ts = CURRENT_TIMESTAMP
WHERE
    (fact_balance_sheet.bal_csti IS DISTINCT FROM EXCLUDED.bal_csti OR
     fact_balance_sheet.bal_trec IS DISTINCT FROM EXCLUDED.bal_trec OR
     fact_balance_sheet.bal_tinv IS DISTINCT FROM EXCLUDED.bal_tinv OR
     fact_balance_sheet.bal_oca IS DISTINCT FROM EXCLUDED.bal_oca OR
     fact_balance_sheet.bal_tca IS DISTINCT FROM EXCLUDED.bal_tca OR
     fact_balance_sheet.bal_netl IS DISTINCT FROM EXCLUDED.bal_netl OR
     fact_balance_sheet.bal_nppe IS DISTINCT FROM EXCLUDED.bal_nppe OR
     fact_balance_sheet.bal_gint IS DISTINCT FROM EXCLUDED.bal_gint OR
     fact_balance_sheet.bal_lti IS DISTINCT FROM EXCLUDED.bal_lti OR
     fact_balance_sheet.bal_otha IS DISTINCT FROM EXCLUDED.bal_otha OR
     fact_balance_sheet.bal_tota IS DISTINCT FROM EXCLUDED.bal_tota OR
     fact_balance_sheet.bal_accp IS DISTINCT FROM EXCLUDED.bal_accp OR
     fact_balance_sheet.bal_tdep IS DISTINCT FROM EXCLUDED.bal_tdep OR
     fact_balance_sheet.bal_ocl IS DISTINCT FROM EXCLUDED.bal_ocl OR
     fact_balance_sheet.bal_tcl IS DISTINCT FROM EXCLUDED.bal_tcl OR
     fact_balance_sheet.bal_tltd IS DISTINCT FROM EXCLUDED.bal_tltd OR
     fact_balance_sheet.bal_tdeb IS DISTINCT FROM EXCLUDED.bal_tdeb OR
     fact_balance_sheet.bal_dit IS DISTINCT FROM EXCLUDED.bal_dit OR
     fact_balance_sheet.bal_mint IS DISTINCT FROM EXCLUDED.bal_mint OR
     fact_balance_sheet.bal_othl IS DISTINCT FROM EXCLUDED.bal_othl OR
     fact_balance_sheet.bal_totl IS DISTINCT FROM EXCLUDED.bal_totl OR
     fact_balance_sheet.bal_coms IS DISTINCT FROM EXCLUDED.bal_coms OR
     fact_balance_sheet.bal_apic IS DISTINCT FROM EXCLUDED.bal_apic OR
     fact_balance_sheet.bal_rtne IS DISTINCT FROM EXCLUDED.bal_rtne OR
     fact_balance_sheet.bal_oeq IS DISTINCT FROM EXCLUDED.bal_oeq OR
     fact_balance_sheet.bal_teq IS DISTINCT FROM EXCLUDED.bal_teq OR
     fact_balance_sheet.bal_tlse IS DISTINCT FROM EXCLUDED.bal_tlse OR
     fact_balance_sheet.bal_tcso IS DISTINCT FROM EXCLUDED.bal_tcso OR
     fact_balance_sheet.bal_tpso IS DISTINCT FROM EXCLUDED.bal_tpso OR
     fact_balance_sheet.bal_nca IS DISTINCT FROM EXCLUDED.bal_nca OR
     fact_balance_sheet.bal_ca IS DISTINCT FROM EXCLUDED.bal_ca OR
     fact_balance_sheet.bal_ncl IS DISTINCT FROM EXCLUDED.bal_ncl OR
     fact_balance_sheet.bal_dta IS DISTINCT FROM EXCLUDED.bal_dta
    );