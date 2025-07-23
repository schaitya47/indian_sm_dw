import pandas as pd
import yfinance as yf
from datetime import timedelta,datetime as dt
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data(data1: list, *args, **kwargs):
    symbol,time_diff = data1[0],data1[1] 
    symbol = ["TCS"]
    data = pd.DataFrame()
    # In future st_date will be passed as an argument
    # For now, we will use a hardcoded date 
    end_date = dt.now()
    start_date = end_date - timedelta(days=time_diff)

    # Need to devlop further to handle incremental data loading
    # For now, we will fetch daily data from 2024-01-01 to today
    # and overwrite the existing data
    def fetch_daily_data(symbol,start_date="2024-01-01", end_date=dt.now()):
        ticker = yf.Ticker(symbol+".NS")
        try:
            data = ticker.history(start=start_date, end=end_date, interval="1d")
            data['Symbol'] = symbol
            data['load_ts'] = dt.now() 
            data.reset_index(inplace=True)
            data.rename(columns={'Date': 'date'}, inplace=True)
            return data
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
    # cnt = 1
    for sym in symbol:
        # print("Pointer is here 1",cnt)
        # cnt = cnt + 1
        daily_data = fetch_daily_data(sym,start_date)
        if daily_data is not None:
            data = pd.concat([data, daily_data], ignore_index=True)
    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
