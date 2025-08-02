import pandas as pd
import yfinance as yf
import json
from datetime import datetime as dt
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data(symbol: list,*args, **kwargs):

    # This function fetches the stock data for the given symbol(s) from Yahoo Finance.
    # It returns a DataFrame with the stock information including market cap, load timestamp, and symbol.
    # symbol is a list of stock symbols and time_diff is the time difference in days to fetch the data. But we are not using time_diff in this function.
    
    # symbol[0] is list of symbols
    symbol = symbol[0]

    # symbol = ["SBIN"]
    # Initialize an empty DataFrame to hold the current data
    c_data = pd.DataFrame()

    # Function to serialize data to JSON format if it is a dict or list
    # This is used to ensure that the data can be stored in a DataFrame without issues.
    def serialize(data):
        if isinstance(data, (dict, list)):
            return json.dumps(data)
        return data
    
    # merge_dataframes function combines the current DataFrame with the master DataFrame.
    # It concatenates the two DataFrames and ignores the index, ensuring that the columns are not ignored.
    # If the current DataFrame is None, it returns the master DataFrame.
    def merge_dataframes(current, master):
        return pd.concat([current, master], ignore_index=True,sort=False) if current is not None else master

    # cnt = 1
    # Loop through each symbol in the list and fetch its data from Yahoo Finance
    # The data is then serialized and added to the current DataFrame.
    # load_ts and symbol columns are added to the DataFrame to track when the data was loaded and which symbol it corresponds to.
    for sym in symbol:
        # print("pointer is here 1", cnt)
        # cnt +=1
        ticker = yf.Ticker(sym+".NS")
        data = ticker.info
        data = {k: serialize(v) for k, v in data.items() if v is not None}
        data = pd.DataFrame([data])
        data["load_ts"] = dt.now()
        data["symbol"] = sym
        c_data = merge_dataframes(data, c_data)
    # print(c_data.columns,"Abcd")
    c_data = c_data.dropna(subset=['marketCap'])
    return c_data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
