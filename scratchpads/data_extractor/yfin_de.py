import yfinance as yf
import os
import json
import pandas as pd
from datetime import datetime

# Output directory
OUTDIR = "yfinance_powerbi_outputs"
os.makedirs(OUTDIR, exist_ok=True)

# Helper to save structured data
def save_data(obj, fname, func_name):
    path = os.path.join(OUTDIR, fname)
    try:
        if isinstance(obj, (pd.DataFrame, pd.Series)):
            obj.to_csv(path)
        elif isinstance(obj, dict):
            with open(path, "w", encoding="utf-8") as f:
                json.dump(obj, f, indent=2)
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write(str(obj))
        print(f"✅ Saved {func_name} to {path}")
    except Exception as e:
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"Error saving {func_name}: {e}")

# Ticker symbol
symbols = "TCS.NS"
now = datetime.now().strftime("%Y-%m-%d")

tickers = yf.Ticker(symbols)

tickers.info

# Functions to run
selected_calls = {
    "info": lambda t: t.info,
    "sustainability": lambda t: t.sustainability,
    "get_major_holders": lambda t: t.get_major_holders(),
    "earnings_dates": lambda t: t.earnings_dates,
    "get_earnings_forecast": lambda t: t.get_earnings_forecast(),
    "get_growth_estimates": lambda t: t.get_growth_estimates(),
    "history_with_interval": lambda t: t.history(start="2022-01-01", end=now, interval="1d"),
    "recommendations": lambda t: t.recommendations,
}

# Run and save results
# for sym in symbols:
#     ticker = yf.Ticker(sym)
#     for fname, func in selected_calls.items():
#         key = f"{sym}_{fname}"
#         try:
#             result = func(ticker)
#             ext = ".csv" if isinstance(result, (pd.DataFrame, pd.Series)) else ".json"
#             save_data(result, f"{key}{ext}", key)
#         except Exception as e:
#             save_data(f"Error: {e}", f"{key}_error.txt", key)

t = yf.Ticker(symbols)

data = t.info
# if isinstance(data,dict):
#     data = pd.DataFrame.from_dict(data, orient='index')
#     data.reset_index(inplace=True)
# save_data(data, "yfin_info.csv", "info")

with open("./yfinance_powerbi_outputs/TCS.NS_info.json", "r", encoding="utf-8") as f:
    data = json.load(f)

def serialize(val):
    if isinstance(val, (dict, list)):
        return json.dumps(val)
    return val

row = {k: serialize(v) for k, v in data.items()}
df = pd.DataFrame([row])
save_data(df, "yfin_info_3.csv", "info")


