import pandas as pd
import yfinance as yf
from datetime import datetime as dt, timedelta, timezone
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data(data1: list, *args, **kwargs):

    # data1 is a list of two elements
    # data1[0] is a list of stock symbols  
    # data1[1] is the time difference in days for which data needs to be fetched
    symbol,time_diff = data1[0],data1[1] 


    # symbol = ["TCS"]

    # initializing an empty dataframe to store the data
    data = pd.DataFrame()

    # Calculate the start and end dates based on the time difference
    end_date = dt.now(timezone(timedelta(hours=5, minutes=30)))
    start_date = end_date - timedelta(days=time_diff+3) # Calculate start date based on time_diff + 3 fallback window

    # Function to fetch daily data for a given symbol
    # This function fetches daily stock data from Yahoo Finance
    # and returns it as a DataFrame with the symbol and load timestamp included.
    def fetch_daily_data(symbol,start_date, end_date):
        ticker = yf.Ticker(symbol+".NS")
        try:
            data = ticker.history(start=start_date, end=end_date, interval="1d")
            data['Symbol'] = symbol
            data['load_ts'] = dt.now(timezone(timedelta(hours=5, minutes=30))) 
            data.reset_index(inplace=True)
            data.rename(columns={'Date': 'date'}, inplace=True)
            return data
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
    
    # cnt = 1
    # Loop through each symbol and fetch the daily data
    # The fetched data is concatenated into a single DataFrame
    for sym in symbol:
        # print("Pointer is here 1",cnt)
        # cnt = cnt + 1
        daily_data = fetch_daily_data(sym,start_date,end_date)
        if daily_data is not None:
            data = pd.concat([data, daily_data], ignore_index=True)
    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
