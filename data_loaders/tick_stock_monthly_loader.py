from Fundamentals import Tickertape
import pandas as pd
import time
import random

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data(*args, **kwargs):
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
    def convert_to_dataframe(c_data,symbol,data):
        if c_data is None:
            print(c_data)
            return data if data is not None else pd.DataFrame()
        c_data['Symbol'] = symbol

        if c_data is not None and not c_data.empty:
            # Ensure the index is reset before concatenation
            data = pd.concat([data,c_data], ignore_index=True)
        return data
    
    ttp = Tickertape()
    # cnt = 1
    # getting all equity screener filters
    # and fetching data for the top 60 companies sorted by market capitalization 60 and not 50 because page size is 20
    screnner_filters = list(ttp.get_equity_screener_all_filters().values())
    data["screener"] = ttp.get_equity_screener_data(filters=screnner_filters, sortby="mrktCapf",number_of_records=60)
    sym = data["screener"]["info.ticker"]
    sid = data["screener"]["sid"]
    slug_url = data["screener"]["slug"]
    for i in range(0,50):
        data["income"]  = convert_to_dataframe(ttp.get_income_data(sid[i],num_time_periods=40), sym[i], data["income"])
        data["balance_sheet"] = convert_to_dataframe(ttp.get_balance_sheet_data(sid[i],num_time_periods=40), sym[i], data["balance_sheet"])
        data["cash_flow"] = convert_to_dataframe(ttp.get_cash_flow_data(sid[i],num_time_periods=40), sym[i], data["cash_flow"])
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
#     symbol = ["larsen-and-toubro"]  

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
#     # res = ttp.get_income_data(symbol[0],num_time_periods=40)
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
#     x = ttp.get_key_ratios(slug_url[0])
#     x = x.T
#     x['Symbol'] = symbol[0]
#     return x

# if __name__ == "__main__":
#     data = load_data1()
#     print(data)