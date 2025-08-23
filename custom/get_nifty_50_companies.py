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

    # This function loads the list of Nifty 50 companies from a PostgreSQL database.
    # It checks the last success timestamp of the pipeline and returns the list of companies
    # if the data is not already loaded within the specified time criteria.
    # The time criteria is set based on the pipeline name.
    # It returns a list of companies and the time difference since the last run.

    # pipeline_name is passed as a pipeline parameter/argument.
    pipeline_name = kwargs.get("pipeline_name")
    """
    Template for loading data from a PostgreSQL database.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#postgresql
    """
    # SQL query to fetch the list of Nifty 50 companies.
    # This query retrieves the 'symbol' column from the 'nifty_50_companies
    query = 'SELECT symbol FROM stock_landing.nifty_50_companies;'

    # SQL query to fetch the last success timestamp of the pipeline.
    # This query retrieves the 'last_success_timestamp' from the 'stage_load_control' table
    # where the 'pipeline_name' matches the specified pipeline name.
    query2 = f"SELECT last_success_timestamp FROM stock_landing.stage_load_control WHERE pipeline_name = '{pipeline_name}'"
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    # Initialize an empty list to store the list of companies and last run timestamp.
    list_of_comp = []
    last_run_ts = []

    # Load the data from PostgreSQL using the specified configuration.
    # The 'ConfigFileLoader' is used to load the configuration settings from 'io_config
    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        list_of_comp = loader.load(query)
        last_run_ts = loader.load(query2)

    # converting dataframe to list
    # Extract the last success timestamp from the loaded data.
    last_run_ts =  last_run_ts['last_success_timestamp'].tolist()

    # calculate the time difference between the current time and the last run timestamp
    time_diff = dt.now() - last_run_ts[0]

    # created time_diff_criteria variable to set the criteria for time difference
    # Set the time difference criteria based on the pipeline name.
    # This determines how often the data should be loaded based on the pipeline's frequency.

    mapping = {
    'yfin_landing_daily': 1,
    'nse_landing_daily': 1,
    'yfin_landing_weekly': 7,
    'yfin_landing_monthly': 30,
    'tick_landing_monthly': 30,
    }

    time_diff_criteria = mapping.get(str(pipeline_name))

    if time_diff_criteria is None:
        raise Exception("Please check the pipeline name.")

    threshold = timedelta(days=time_diff_criteria) - timedelta(hours=1)

    # If the time difference is less than the criteria, return None to indicate no new data to load.
    # Otherwise, return the list of companies and the time difference.
    if time_diff < threshold:
        print("No new data to load, returning existing list of companies.")
        return None 
    else:
        list_of_comp = list_of_comp['symbol'].tolist()
        return [list_of_comp, time_diff_criteria]


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