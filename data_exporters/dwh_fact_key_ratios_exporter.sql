
INSERT INTO stock_dw.fact_key_ratios (
    date_key,
    stock_key,
    source_key,
    risk,
    letter_3mavgvol,
    letter_4wpct,
    letter_52whigh,
    letter_52wlow,
    letter_52wpct,
    beta,
    bps,
    div_yield,
    eps,
    inddy,
    indpb,
    indpe,
    market_cap,
    mrkt_cap_rank,
    pb,
    pe,
    roe,
    n_shareholders,
    last_price,
    ttm_pe,
    market_cap_label,
    letter_12mvol,
    mrkt_capf,
    apef,
    pbr,
    etf_liq,
    etf_liq_label,
    expense_ratio,
    track_err,
    ind_expense_ratio,
    ind_track_err,
    asst_under_man,
    load_ts
)
SELECT
    dd.date_key,
    ds.stock_key,
    dsrc.source_key,
    src.risk,
    src.letter_3mavgvol,
    src.letter_4wpct,
    src.letter_52whigh,
    src.letter_52wlow,
    src.letter_52wpct,
    src.beta,
    src.bps,
    src.div_yield,
    src.eps,
    src.inddy,
    src.indpb,
    src.indpe,
    src.market_cap,
    src.mrkt_cap_rank,
    src.pb,
    src.pe,
    src.roe,
    src.n_shareholders,
    src.last_price,
    src.ttm_pe,
    src.market_cap_label,
    src.letter_12mvol,
    src.mrkt_capf,
    src.apef,
    src.pbr,
    src.etf_liq,
    src.etf_liq_label,
    src.expense_ratio,
    src.track_err,
    src.ind_expense_ratio,
    src.ind_track_err,
    src.asst_under_man,
    src.load_ts
FROM stock_landing.tick_stock_key_ratios_tbls src
INNER JOIN stock_dw.dim_stock ds
    ON ds.nk_symbol = src.symbol
INNER JOIN stock_dw.dim_date dd
    ON dd.nk_full_date = src.load_ts::date
INNER JOIN stock_dw.dim_source dsrc
    ON dsrc.source_name = 'TICK'
ON CONFLICT (date_key, stock_key, source_key)
DO UPDATE SET
    risk = EXCLUDED.risk,
    letter_3mavgvol = EXCLUDED.letter_3mavgvol,
    letter_4wpct = EXCLUDED.letter_4wpct,
    letter_52whigh = EXCLUDED.letter_52whigh,
    letter_52wlow = EXCLUDED.letter_52wlow,
    letter_52wpct = EXCLUDED.letter_52wpct,
    beta = EXCLUDED.beta,
    bps = EXCLUDED.bps,
    div_yield = EXCLUDED.div_yield,
    eps = EXCLUDED.eps,
    inddy = EXCLUDED.inddy,
    indpb = EXCLUDED.indpb,
    indpe = EXCLUDED.indpe,
    market_cap = EXCLUDED.market_cap,
    mrkt_cap_rank = EXCLUDED.mrkt_cap_rank,
    pb = EXCLUDED.pb,
    pe = EXCLUDED.pe,
    roe = EXCLUDED.roe,
    n_shareholders = EXCLUDED.n_shareholders,
    last_price = EXCLUDED.last_price,
    ttm_pe = EXCLUDED.ttm_pe,
    market_cap_label = EXCLUDED.market_cap_label,
    letter_12mvol = EXCLUDED.letter_12mvol,
    mrkt_capf = EXCLUDED.mrkt_capf,
    apef = EXCLUDED.apef,
    pbr = EXCLUDED.pbr,
    etf_liq = EXCLUDED.etf_liq,
    etf_liq_label = EXCLUDED.etf_liq_label,
    expense_ratio = EXCLUDED.expense_ratio,
    track_err = EXCLUDED.track_err,
    ind_expense_ratio = EXCLUDED.ind_expense_ratio,
    ind_track_err = EXCLUDED.ind_track_err,
    asst_under_man = EXCLUDED.asst_under_man,
    load_ts = EXCLUDED.load_ts
WHERE
    fact_key_ratios.risk IS DISTINCT FROM EXCLUDED.risk OR
    fact_key_ratios.letter_3mavgvol IS DISTINCT FROM EXCLUDED.letter_3mavgvol OR
    fact_key_ratios.letter_4wpct IS DISTINCT FROM EXCLUDED.letter_4wpct OR
    fact_key_ratios.letter_52whigh IS DISTINCT FROM EXCLUDED.letter_52whigh OR
    fact_key_ratios.letter_52wlow IS DISTINCT FROM EXCLUDED.letter_52wlow OR
    fact_key_ratios.letter_52wpct IS DISTINCT FROM EXCLUDED.letter_52wpct OR
    fact_key_ratios.beta IS DISTINCT FROM EXCLUDED.beta OR
    fact_key_ratios.bps IS DISTINCT FROM EXCLUDED.bps OR
    fact_key_ratios.div_yield IS DISTINCT FROM EXCLUDED.div_yield OR
    fact_key_ratios.eps IS DISTINCT FROM EXCLUDED.eps OR
    fact_key_ratios.inddy IS DISTINCT FROM EXCLUDED.inddy OR
    fact_key_ratios.indpb IS DISTINCT FROM EXCLUDED.indpb OR
    fact_key_ratios.indpe IS DISTINCT FROM EXCLUDED.indpe OR
    fact_key_ratios.market_cap IS DISTINCT FROM EXCLUDED.market_cap OR
    fact_key_ratios.mrkt_cap_rank IS DISTINCT FROM EXCLUDED.mrkt_cap_rank OR
    fact_key_ratios.pb IS DISTINCT FROM EXCLUDED.pb OR
    fact_key_ratios.pe IS DISTINCT FROM EXCLUDED.pe OR
    fact_key_ratios.roe IS DISTINCT FROM EXCLUDED.roe OR
    fact_key_ratios.n_shareholders IS DISTINCT FROM EXCLUDED.n_shareholders OR
    fact_key_ratios.last_price IS DISTINCT FROM EXCLUDED.last_price OR
    fact_key_ratios.ttm_pe IS DISTINCT FROM EXCLUDED.ttm_pe OR
    fact_key_ratios.market_cap_label IS DISTINCT FROM EXCLUDED.market_cap_label OR
    fact_key_ratios.letter_12mvol IS DISTINCT FROM EXCLUDED.letter_12mvol OR
    fact_key_ratios.mrkt_capf IS DISTINCT FROM EXCLUDED.mrkt_capf OR
    fact_key_ratios.apef IS DISTINCT FROM EXCLUDED.apef OR
    fact_key_ratios.pbr IS DISTINCT FROM EXCLUDED.pbr OR
    fact_key_ratios.etf_liq IS DISTINCT FROM EXCLUDED.etf_liq OR
    fact_key_ratios.etf_liq_label IS DISTINCT FROM EXCLUDED.etf_liq_label OR
    fact_key_ratios.expense_ratio IS DISTINCT FROM EXCLUDED.expense_ratio OR
    fact_key_ratios.track_err IS DISTINCT FROM EXCLUDED.track_err OR
    fact_key_ratios.ind_expense_ratio IS DISTINCT FROM EXCLUDED.ind_expense_ratio OR
    fact_key_ratios.ind_track_err IS DISTINCT FROM EXCLUDED.ind_track_err OR
    fact_key_ratios.asst_under_man IS DISTINCT FROM EXCLUDED.asst_under_man;