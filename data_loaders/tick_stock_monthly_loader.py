from Fundamentals import Tickertape
import pandas as pd
from datetime import datetime as dt

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data(symbol: list,*args, **kwargs):
    # Symbol is a list where the first element is a list of stock symbols
    # and the second element is the number of days to look back for data.
    # This data loader function loads financial data from Tickertape for the given symbols.
    # It fetches data for the last 'time_diff' days and returns a dictionary of DataFrames
    symbol,time_diff = symbol[0],symbol[1]

    # Initialize a dictionary to hold DataFrames for different financial data
    # Each key corresponds to a type of financial data, and the value is a DataFrame
    data = {
        "income": pd.DataFrame(),
        "balance_sheet": pd.DataFrame(),
        "cash_flow": pd.DataFrame(),
        "score_card": pd.DataFrame(),
        "shareholding_pattern": pd.DataFrame(),
        "dividend": pd.DataFrame(),
        "key_ratios": pd.DataFrame(),
        "screener" : pd.DataFrame()
    }

    # Function to convert fetched data into a DataFrame and append it to the existing DataFrame
    # This function checks if the fetched data is None or empty, and if not, it appends it to the existing DataFrame
    # It also adds the symbol and load timestamp to the DataFrame
    # Returns the updated DataFrame
    def convert_to_dataframe(c_data,symbol,data):
        if c_data is None:
            # print(c_data)
            return data if data is not None else pd.DataFrame()
        c_data['Symbol'] = symbol
        c_data['load_ts'] = dt.now()

        if c_data is not None and not c_data.empty:
            # Ensure the index is reset before concatenation
            data = pd.concat([data,c_data], ignore_index=True)
        return data
    
    # Instantiate the Tickertape class to fetch financial data
    # This class is responsible for fetching data from Tickertape
    ttp = Tickertape()

    # cnt = 1
    # This function retrieves all available filters for the equity screener
    # It returns a list of filters that can be used to fetch specific financial data
    screener_filters = list(ttp.get_equity_screener_all_filters().values())

    # Fetching the equity screener data with the specified filters, sorting by market capitalization.
    # Data is fetched for the top 200 companies sorted by market capitalization
    data["screener"] = ttp.get_equity_screener_data(filters=screener_filters, sortby="mrktCapf",number_of_records=200)

    # Extracting the stock symbols, IDs, and slug URLs from the screener data
    # These will be used to fetch detailed financial data for each stock
    sym = data["screener"]["info.ticker"]
    sid = data["screener"]["sid"]
    slug_url = data["screener"]["slug"]

    # Determine the time period for fetching financial data based on the time_diff
    # If time_diff is less than 180 days, use 6 months; otherwise, use 100 months
    # This is used to specify the number of time periods for fetching historical financial data
    time_period = 0
    if time_diff < 180:
        time_period = 6
    else:
        time_period = 100

    # Loop through each stock symbol and fetch financial data
    # For each symbol, it fetches income data, balance sheet data, cash flow data
    # scorecard data, shareholding pattern, dividend history, and key ratios
    # Each fetched data is converted to a DataFrame and appended to the corresponding DataFrame in `data`
    # The loop runs for the first 200 symbols in the screener data
    # cnt  = 1
    for i in range(0, 200):
        if sym[i] in symbol:
            # print(sym[i],cnt)
            # cnt+=1
            data["income"]  = convert_to_dataframe(ttp.get_income_data(sid[i],num_time_periods=time_period), sym[i], data["income"])
            data["balance_sheet"] = convert_to_dataframe(ttp.get_balance_sheet_data(sid[i],num_time_periods=time_period), sym[i], data["balance_sheet"])
            data["cash_flow"] = convert_to_dataframe(ttp.get_cash_flow_data(sid[i],num_time_periods=time_period), sym[i], data["cash_flow"])
            data["score_card"] = convert_to_dataframe(ttp.get_score_card(sid[i]), sym[i], data["score_card"])
            if slug_url[i] is not None:
                # print(slug_url[i])
                data["shareholding_pattern"] = convert_to_dataframe(ttp.get_share_holding_pattern(slug_url[i]), sym[i], data["shareholding_pattern"])
                data["dividend"] = convert_to_dataframe(ttp.get_dividends_history(slug_url[i]), sym[i], data["dividend"])
                data["key_ratios"] = convert_to_dataframe(ttp.get_key_ratios(slug_url[i]).T, sym[i], data["key_ratios"])
    return data

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'


# def load_data1():
#     symbol = ["TCS"]  

#     ttp = Tickertape()
#     screnner_filters = list(ttp.get_equity_screener_all_filters().values())
#     data = {"screener": pd.DataFrame()}
#     data["screener"] = ttp.get_equity_screener_data(filters=screnner_filters, sortby="mrktCapf",number_of_records=60)
#     # print(data["screener"])
#     sym = data["screener"]["info.ticker"]
#     sid = data["screener"]["sid"]
#     slug_url = data["screener"]["slug"]
#     # _,raw_data = ttp.get_ticker(symbol[0])
#     # slug_url = raw_data[0].get('slug') if raw_data else None
#     # fetching income data for the given symbol and returns dataframe with 40 time periods
#     print(symbol)
#     res = ttp.get_income_data(symbol[0],num_time_periods=3)
#     # res = ttp.get_balance_sheet_data(symbol[0],num_time_periods=40)
#     # res = ttp.get_cash_flow_data(symbol[0],num_time_periods=40)
#     # res = ttp.get_score_card(symbol[0])
#     # res = None
#     # if slug_url:
#     #     # res = ttp.get_share_holding_pattern(sulg_url)
#     #     # res = ttp.get_dividends_history(slug_url)
#     #     # res = ttp.get_key_ratios(slug_url)
#     #     res = ttp.get_equity_screener_all_filters()
#     #     x = []
#     #     for item in res:
#     #         x.append(res[item])
#     #     res = ttp.get_equity_screener_data(filters=x, sortby='mrktCapf', number_of_records=50)
#     #     print(res)
#     # x = ttp.get_key_ratios(slug_url[0])
#     # x = x.T
#     # x['Symbol'] = symbol[0]
#     return res

# if __name__ == "__main__":
#     data = load_data1()
#     print(data)