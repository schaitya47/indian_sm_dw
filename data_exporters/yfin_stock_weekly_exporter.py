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
    schema_name = 'stock_landing'  # Specify the name of the schema to export data to
    primary_key = [""]

    for key in df:
        if key == "holders":
            table_name = 'yfin_stock_holders_tbls' 
            primary_key = ["symbol"]
        elif key == "earn_dates":
            table_name = 'yfin_stock_earning_data_tbls'
            primary_key = ["symbol","earnings_date"]
        elif key == "earn_est":
            table_name = 'yfin_stock_earning_estimates_tbls' 
            primary_key = ["symbol","period"]
        elif key == "growth_est":
            table_name = 'yfin_stock_growth_estimate_tbls'
            primary_key = ["symbol","period"]
        elif key == "recom":
            table_name = 'yfin_stock_recomendations_tbls' 
            primary_key = ["symbol","period"]
        
        config_path = path.join(get_repo_path(), 'io_config.yaml')
        config_profile = 'default'

        with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
            loader.export(
                df[key],
                schema_name,
                table_name,
                index=False,  # Specifies whether to include index in exported table
                if_exists='append',  #Append mode
                unique_conflict_method='update',  #Enables upsert
                unique_constraints= primary_key  #Must match your table's UNIQUE or PRIMARY KEY
            )
