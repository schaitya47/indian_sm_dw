import pandas as pd
import yfinance as yf
from datetime import datetime as dt, timedelta, timezone

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


    # symbol=["TCS"]
    # initalize an dict of DataFrames to hold the empty dataframes for each type of data
    # This will be used to store the data fetched from Yahoo Finance for each symbol.
    data = {
        # "info": pd.DataFrame(), #Moving the info to other loader as it requires a lot of transformation.
        "holders": pd.DataFrame(),
        "earn_dates": pd.DataFrame(),
        "earn_est": pd.DataFrame(),
        "growth_est": pd.DataFrame(),
        "recom": pd.DataFrame()
    }


    # Function to merge the current DataFrame with the master DataFrame.
    # It concatenates the two DataFrames and ignores the index, ensuring that the columns are not ignored.
    # If the current DataFrame is None, it returns the master DataFrame.
    def merge_dataframe(data,symbol,c_data):
        if data is None:
            return c_data if c_data is not None else pd.DataFrame()
        data['Symbol'] = symbol
        data['load_ts'] = dt.now(timezone(timedelta(hours=5, minutes=30)))
        if c_data is not None and not c_data.empty:
            # Ensure the index is reset before concatenation
            data = pd.concat([c_data,data], ignore_index=True)
        return data

    # Loop through each symbol and fetch the data
    for sym in symbol:
        ticker = yf.Ticker(sym+".NS")

        # data is transposed to have the data as columns instead of rows
        # This is done because the data have only one row and multiple columns.
        data["holders"]  = merge_dataframe(ticker.get_major_holders().T, sym, data["holders"])

        # earnings_dates, earnings_estimate, growth_estimates, and recommendations are fetched from the ticker object
        # The index is reset because the index hold the date and we want that as it's a key column.
        earn_dates = ticker.earnings_dates
        earn_dates.reset_index(inplace=True)
        data["earn_dates"] = merge_dataframe(earn_dates, sym, data["earn_dates"])

        earn_est = ticker.get_earnings_estimate()
        earn_est.reset_index(inplace=True)
        data["earn_est"] = merge_dataframe(earn_est, sym, data["earn_est"])

        growth_est = ticker.get_growth_estimates()
        growth_est.reset_index(inplace=True)
        data["growth_est"] = merge_dataframe(growth_est, sym, data["growth_est"])

        data["recom"] = merge_dataframe(ticker.recommendations, sym, data["recom"])

    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'

# def load_data1():
#     yf1 = yf.Ticker("TCS.NS")
#     x = yf1.get_growth_estimates()
#     # x.reset_index(inplace=True)
    
#     print(x)



# if __name__ == "__main__":
#     data = load_data1()
#     print(data)
