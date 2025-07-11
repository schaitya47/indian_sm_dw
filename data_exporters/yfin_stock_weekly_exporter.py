import os
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_postgres(df: dict, **kwargs) -> None:
    """
    Template for exporting data to a PostgreSQL database.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#postgresql
    """

    for key in df:
        schema_name = 'stock_landing'  # Specify the name of the schema to export data to
        
        if key == "info":
            table_name = 'yfin_stock_info_tbls'  # Specify the name of the table to export data to
        elif key == "holders":
            table_name = 'yfin_stock_holders_tbls' 
        elif key == "earn_dates":
            table_name = 'yfin_stock_earning_data_tbls'
        elif key == "earn_est":
            table_name = 'yfin_stock_earning_estimates_tbls' 
        elif key == "growth_est":
            table_name = 'yfin_stock_growth_estimate_tbls'
        elif key == "recom":
            table_name = 'yfin_stock_recomendations_tbls' 
        
        config_path = path.join(get_repo_path(), 'io_config.yaml')
        config_profile = 'default'

        with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
            loader.export(
                df[key],
                schema_name,
                table_name,
                index=False,  # Specifies whether to include index in exported table
                if_exists='replace',  # Specify resolution policy if table name already exists
            )
