from utils.nse.nse_data_extractor import NSEMasterData
from datetime import timedelta,datetime as dt
import pandas as pd
import time
import random

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data(symbol: list,*args, **kwargs):
    # Symbol is a list where the first element is a list of stock symbols
    # and the second element is the number of days to look back for data.
    # This data loader function loads daily stock data from NSE for the given symbols.
    # It fetches data for the last 'time_diff' days and returns a DataFrame
    # symbol: list of stock symbols to fetch data for
    # time_diff: number of days to look back for data
    symbol,time_diff = symbol[0],symbol[1] 
    data = pd.DataFrame()

    # Prepare timeframe
    end_date = dt.now() # Current date 
    start_date = end_date - timedelta(days=time_diff+3) # Calculate start date based on time_diff + 3 fallback window

    # Instantiate class NSEMasterData
    # This class is responsible for fetching data from charting.nseindia.com
    nse = NSEMasterData()

    # Download symbol master
    nse.download_symbol_master()

    # Fetches the data for the specified date range and add Symbol and load timestamp to the DataFrame
    # Returns a DataFrame with the stock data
    def fetch_daily_data(symbol,start_date, end_date):
        try:
            data = nse.get_history(symbol,"NSE",start_date, end_date,"1d")
            data['Symbol'] = symbol
            data['load_ts'] = dt.now()
            data.reset_index(inplace=True)
            return data
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
    

    # cnt = 1
    # Loop through each symbol and fetch daily data
    # Concatenate the data into a single DataFrame
    # The loop also includes a random wait time to avoid hitting the server too quickly
    for sym in symbol:
        # print("Pointer is here 1",cnt)
        # cnt += 1
        daily_data = fetch_daily_data(sym,start_date,end_date)
        if daily_data is not None:
            data = pd.concat([data, daily_data], ignore_index=True)
        wait_time = random.uniform(1, 4)
        time.sleep(wait_time)
    return data



@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
