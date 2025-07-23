from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from os import path
from datetime import datetime as dt, timedelta

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@custom
def load_data_from_postgres(*args, **kwargs):
    pipeline_name = kwargs.get("pipeline_name")
    """
    Template for loading data from a PostgreSQL database.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#postgresql
    """
    query = 'SELECT symbol FROM stock_landing.nifty_50_companies;'
    query2 = f"SELECT last_success_timestamp FROM stock_landing.stage_load_control WHERE pipeline_name = '{pipeline_name}'"
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'
    list_of_comp = []
    last_run_ts = []
    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        list_of_comp = loader.load(query)
        last_run_ts = loader.load(query2)

    last_run_ts =  last_run_ts['last_success_timestamp'].tolist()
    time_diff = dt.now() - last_run_ts[0]
    time_diff = time_diff.days
    time_diff_criteria = 0

    if pipeline_name in ["yfin_landing_daily","nse_landing_daily"]:
        time_diff_criteria = 1
    elif pipeline_name == "yfin_landing_weekly":
        time_diff_criteria = 7
    elif pipeline_name in ["yfin_landing_monthly","tick_landing_monthly"]:
        time_diff_criteria = 30
    
    if time_diff < time_diff_criteria:
        print("No new data to load, returning existing list of companies.")
        return None 
    else:
        list_of_comp = list_of_comp['symbol'].tolist()
        return [list_of_comp,time_diff]


# @test
# def test_output(output, *args) -> None:
#     """
#     Template code for testing the output of the block.
#     """
#     assert output is not None, 'The output is undefined'


# if __name__ == '__main__':
#     pipeline_name = 'get_nifty50_companies'
#     query = 'SELECT symbol FROM stock_landing.nifty_50_companies;'
#     query2 = f"SELECT last_success_timestamp FROM stock_landing.stage_load_control WHERE pipeline_name = '{pipeline_name}'"
#     config_path = path.join(get_repo_path(), 'io_config.yaml')
#     config_profile = 'default'
#     list_of_comp = []
#     with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
#         # list_of_comp = loader.load(query)
#         last_run_ts = loader.load(query2)

#     last_run_ts = last_run_ts['last_success_timestamp'].tolist()[0]

#     start_date = last_run_ts
#     enddate = dt.now() 
#     time_diff = enddate - start_date

#     # print("Last run timestamp:",last_run_ts[0])
#     # print(type(last_run_ts[0]))
#     # list_of_comp = list_of_comp['symbol'].tolist()