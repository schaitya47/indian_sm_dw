import yfinance as yf
from datetime import datetime
import os

# Directory for output
OUTDIR = "yfinance_outputs"
os.makedirs(OUTDIR, exist_ok=True)

# Helper: save data with comment
def save(obj, fname, func_name):
    path = os.path.join(OUTDIR, fname)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# Result of {func_name}\n")
        try:
            f.write(repr(obj))
        except Exception:
            f.write(str(obj))
    print(f"✅ Saved {func_name} to {path}")

# Tickers to test
symbols = ["TCS.NS"]  # adjust as needed
tickers = yf.Tickers(" ".join(symbols))

# Timestamp for period-based calls
now = datetime.now().strftime("%Y-%m-%d")

# Mapping of functions to call on Ticker class
ticker_calls = {
    "history": lambda t: t.history(period="1mo"),
    "actions": lambda t: t.actions,
    "dividends": lambda t: t.dividends,
    "splits": lambda t: t.splits,
    "earnings": lambda t: t.earnings,
    "quarterly_earnings": lambda t: t.quarterly_earnings,
    "earnings_dates": lambda t: t.earnings_dates,
    "calendar": lambda t: t.calendar,
    "recommendations": lambda t: t.recommendations,
    "sustainability": lambda t: t.sustainability,
    "options": lambda t: t.options,
    "get_earnings_forecast": lambda t: t.get_growth_estimates(),
    "get_growth_estimates": lambda t: t.growth_estimates,
    "get_funds_data": lambda t: t.get_funds_data(),
    "funds_data": lambda t: t.funds_data,
    "get_insider_purchases": lambda t: t.get_insider_purchases(),
    "insider_purchases": lambda t: t.insider_purchases,
    "get_insider_transactions": lambda t: t.get_insider_transactions(),
    "insider_transactions": lambda t: t.insider_transactions,
    "get_insider_roster_holders": lambda t: t.get_insider_roster_holders(),
    "insider_roster_holders": lambda t: t.insider_roster_holders,
    "get_major_holders": lambda t: t.get_major_holders(),
    "major_holders": lambda t: t.major_holders,
    "get_institutional_holders": lambda t: t.get_institutional_holders(),
    "institutional_holders": lambda t: t.institutional_holders,
    "get_mutualfund_holders": lambda t: t.get_mutualfund_holders(),
    "mutualfund_holders": lambda t: t.mutualfund_holders,
    "info": lambda t: t.info,
    "fast_info": lambda t: t.fast_info,
    "recommendation_trend": lambda t: t.recommendation_trend,
    "history_with_interval": lambda t: t.history(start="2022-01-01", end=now, interval="1d"),
}

# Functions from the yfinance module
module_calls = {
    "download": lambda: yf.download(symbols, period="1mo"),
    "enable_debug_mode": lambda: yf.enable_debug_mode(),
    "set_tz_cache_location": lambda: yf.set_tz_cache_location(OUTDIR),
}

# Run module-level functions
for fname, func in module_calls.items():
    try:
        res = func()
        save(res, f"{fname}.txt", fname)
    except Exception as e:
        save(f"Error: {e}", f"{fname}_error.txt", fname)

# Run per-ticker functions
for sym in symbols:
    t = yf.Ticker(sym)
    for fname, func in ticker_calls.items():
        key = f"{sym}_{fname}"
        try:
            res = func(t)
            save(res, f"{key}.txt", key)
        except Exception as e:
            save(f"Error: {e}", f"{key}_error.txt", key)
