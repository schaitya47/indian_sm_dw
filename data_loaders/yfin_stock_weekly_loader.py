import pandas as pd
import yfinance as yf
from datetime import datetime as dt

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data(symbol: list,*args, **kwargs):
    symbol = symbol[0]
    # symbol=["TCS"]
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
        if data is None:
            return c_data if c_data is not None else pd.DataFrame()
        data['Symbol'] = symbol
        data['load_ts'] = dt.now()
        if c_data is not None and not c_data.empty:
            # Ensure the index is reset before concatenation
            data = pd.concat([c_data,data], ignore_index=True)
        return data

    for sym in symbol:
        ticker = yf.Ticker(sym+".NS")

        data["holders"]  = convert_to_dataframe(ticker.get_major_holders().T, sym, data["holders"])

        earn_dates = ticker.earnings_dates
        earn_dates.reset_index(inplace=True)
        data["earn_dates"] = convert_to_dataframe(earn_dates, sym, data["earn_dates"])

        earn_est = ticker.get_earnings_estimate()
        earn_est.reset_index(inplace=True)
        data["earn_est"] = convert_to_dataframe(earn_est, sym, data["earn_est"])

        growth_est = ticker.get_growth_estimates()
        growth_est.reset_index(inplace=True)
        data["growth_est"] = convert_to_dataframe(growth_est, sym, data["growth_est"])

        data["recom"] = convert_to_dataframe(ticker.recommendations, sym, data["recom"])

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
