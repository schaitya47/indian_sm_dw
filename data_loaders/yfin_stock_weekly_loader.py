import pandas as pd
import yfinance as yf
import datetime as dt
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data(*args, **kwargs):
    symbol = ["TCS.NS"]

    # Initialize an empty DataFrame to hold the data
    data = {
        # "info": pd.DataFrame(), #Moving the info to other loader as it requires a lot of transformation.
        "holders": pd.DataFrame(),
        "earn_dates": pd.DataFrame(),
        "earn_est": pd.DataFrame(),
        "growth_est": pd.DataFrame(),
        "recom": pd.DataFrame()
    }


    # Need to devlop further to handle incremental data loading
    # For now, we will fetch daily data from 2024-01-01 to today
    # and overwrite the existing data
    def convert_to_dataframe(data,symbol,c_data):
        if isinstance(data,dict):
            data = pd.DataFrame.from_dict(data, orient='index')
            data.reset_index(inplace=True)
        elif data is None:
            return c_data if c_data is not None else pd.DataFrame()
        data['Symbol'] = symbol
        if c_data is not None and not c_data.empty:
            # Ensure the index is reset before concatenation
            data = pd.concat([c_data,data], ignore_index=True)
            data.reset_index(inplace=True)
        return data
        

    t = yf.Tickers(symbol)
    for sym in t.tickers:
        # data["info"] = convert_to_dataframe(t.tickers[sym].info, sym, data["info"])
        data["holders"]  = convert_to_dataframe(t.tickers[sym].get_major_holders(), sym, data["holders"])
        data["earn_dates"] = convert_to_dataframe(t.tickers[sym].earnings_dates, sym, data["earn_dates"])
        data["earn_est"] = convert_to_dataframe(t.tickers[sym].get_earnings_estimate(), sym, data["earn_est"])
        data["growth_est"] = convert_to_dataframe(t.tickers[sym].get_growth_estimates(), sym, data["growth_est"])
        data["recom"] = convert_to_dataframe(t.tickers[sym].recommendations, sym, data["recom"])

    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
