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
        
        if key == "income":
            table_name = 'tick_stock_income_tbls'  # Specify the name of the table to export data to
            primary_key = ["symbol","display_period"]   
        elif key == "balance_sheet":
            table_name = 'tick_stock_balance_sheet_tbls' 
            primary_key = ["symbol","display_period"] 
        elif key == "cash_flow":
            table_name = 'tick_stock_cashflow_tbls'
            primary_key = ["symbol","display_period"]       
        elif key == "score_card":
            table_name = 'tick_stock_score_card_tbls'
            primary_key = ["symbol","_name"]
        elif key == "shareholding_pattern":
            table_name = 'tick_stock_shareholding_pattern_tbls' 
            primary_key = ["symbol","_date"]
        elif key == "dividend":
            table_name = 'tick_stock_dividend_history_tbls'
            primary_key = ["id"]
        elif key == "key_ratios":
            table_name = 'tick_stock_key_ratios_tbls'
            primary_key = ["symbol"]
        elif key == 'screener':
            table_name = 'tick_stock_equity_screener_tbls' 
            primary_key = ["info_ticker"]
        
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
