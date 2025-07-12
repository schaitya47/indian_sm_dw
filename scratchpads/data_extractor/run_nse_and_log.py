from nse_data_extractor import NSEMasterData
from datetime import datetime, timedelta
from contextlib import redirect_stdout
import pandas as pd
import os

# Configure pandas to show full output
pd.set_option("display.max_rows", None, "display.max_columns", None)

# Output log file
output_file = "nse_function_outputs.txt"

# Prepare timeframe
end_date = datetime.now()
start_date = end_date - timedelta(days=7)

# Start capturing function outputs
with open(output_file, "w") as f, redirect_stdout(f):
    print("======= NSE FUNCTION OUTPUTS LOG =======")
    print(f"Date & Time: {datetime.now()}")
    print("=" * 50)

    # Instantiate class
    print("\n--- Creating NSEMasterData instance ---")
    nse = NSEMasterData()

    # Test: download_symbol_master()
    print("\n--- Running download_symbol_master() ---")
    nse.download_symbol_master()
    print("NSE Master Sample:\n", nse.nse_data.head(2))
    print("NFO Master Sample:\n", nse.nfo_data.head(2))

    # Test: get_nse_symbol_master() with both URLs
    print("\n--- Running get_nse_symbol_master() for NSE ---")
    nse_df = nse.get_nse_symbol_master(nse.nse_url)
    print(nse_df.head(2))

    print("\n--- Running get_nse_symbol_master() for NFO ---")
    nfo_df = nse.get_nse_symbol_master(nse.nfo_url)
    print(nfo_df.head(2))

    # Test: search() - NSE
    print("\n--- Running search('RELIANCE', 'NSE', match=False) ---")
    print(nse.search('RELIANCE', 'NSE', match=False))

    # Test: search() - NFO
    print("\n--- Running search('BANKNIFTY', 'NFO', match=False) ---")
    print(nse.search('BANKNIFTY', 'NFO', match=False))

    # Test: search_symbol()
    print("\n--- Running search_symbol('INFY', 'NSE') ---")
    print(nse.search_symbol('INFY', 'NSE'))

    # Test: get_history() - Index EOD
    print("\n--- Running get_history('NIFTY', 'NSE', interval='1d') ---")
    df_index = nse.get_history('NIFTY', 'NSE', start=start_date, end=end_date, interval='1d')
    print(df_index.head(2))

    # Test: get_history() - Index Intraday
    print("\n--- Running get_history('NIFTY BANK', 'NSE', interval='1m') ---")
    df_intraday = nse.get_history('NIFTY BANK', 'NSE', start=start_date, end=end_date, interval='1m')
    print(df_intraday.head(2))

    # Test: get_history() - Stock Intraday
    print("\n--- Running get_history('TCS', 'NSE', interval='10m') ---")
    df_stock = nse.get_history('TCS', 'NSE', start=start_date, end=end_date, interval='10m')
    print(df_stock.head(2))

    # Test: get_history() - Index Future
    print("\n--- Running get_history('NIFTY25JUNFUT', 'NFO', interval='1h') ---")
    df_ifut = nse.get_history('NIFTY25JUNFUT', 'NFO', start=start_date, end=end_date, interval='1h')
    print(df_ifut.head(2))

    # Test: get_history() - Stock Future
    print("\n--- Running get_history('RELIANCE25JUNFUT', 'NFO', interval='1h') ---")
    df_sfut = nse.get_history('RELIANCE25JUNFUT', 'NFO', start=start_date, end=end_date, interval='1h')
    print(df_sfut.head(2))

    # Test: get_history() - Index Option
    print("\n--- Running get_history('BANKNIFTY25JUN50000PE', 'NFO', interval='5m') ---")
    df_iopt = nse.get_history('BANKNIFTY25JUN50000PE', 'NFO', start=start_date, end=end_date, interval='5m')
    print(df_iopt.head(2))

    # Test: get_history() - Stock Option
    print("\n--- Running get_history('TCS25JUN3800CE', 'NFO', interval='5m') ---")
    df_sopt = nse.get_history('TCS25JUN3800CE', 'NFO', start=start_date, end=end_date, interval='5m')
    print(df_sopt.head(2))

    print("\n======= ALL FUNCTION OUTPUTS CAPTURED =======")
