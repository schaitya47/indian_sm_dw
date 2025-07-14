from Fundamentals import Tickertape

# if 'data_loader' not in globals():
#     from mage_ai.data_preparation.decorators import data_loader
# if 'test' not in globals():
#     from mage_ai.data_preparation.decorators import test


# @data_loader
# def load_data(*args, **kwargs):
#     symbol = ["ADAI"]
#     ttp = Tickertape()

#     res = ttp.get_stock_monthly_data(
#         symbol=symbol,
#         start_date="2020-01-01",
#         end_date="2023-10-01",
#         interval="1d",
#         include_dividends=True,
#         include_splits=True,
#     )
#     print(res)
#     return res

# @test
# def test_output(output, *args) -> None:
#     """
#     Template code for testing the output of the block.
#     """
#     assert output is not None, 'The output is undefined'


def load_data():
    symbol = ["TCS"]
    ttp = Tickertape()
    # fetching income data for the given symbol and returns dataframe with 40 time periods
    # res = ttp.get_income_data(symbol[0],num_time_periods=40)
    # res = ttp.get_balance_sheet_data(symbol[0],num_time_periods=40)
    # res = ttp.get_cash_flow_data(symbol[0],num_time_periods=40)
    # res = ttp.get_score_card(symbol[0])
    res = None
    _,raw_data = ttp.get_ticker(symbol[0])
    sulg_url = raw_data[0].get('slug') if raw_data else None
    if sulg_url:
        res = ttp.get_share_holding_pattern(sulg_url)
    print(res)
    return res

if __name__ == "__main__":
    data = load_data()