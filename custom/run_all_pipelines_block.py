import logging
from mage_ai.orchestration.triggers.api import trigger_pipeline
import time

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@custom
def execute_all_pipelines(*args, **kwargs):

    PIPELINES = [
    'get_nifty50_companies',
    'nse_landing_daily',
    'tick_landing_monthly',
    'yfin_landing_daliy',
    'yfin_landing_monthly', 
    'yfin_landing_weekly'
    # 'dim_date_pipeline',
    # 'dim_source_pipeline',
    # 'dim_stock_pipeline',
    # 'fact_ohlcv_pipeline',
    # 'fact_balance_sheet_pipeline',
    # 'fact_cashflow_pipeline',
    # 'fact_income_pipeline',
    # 'fact_key_ratios_pipeline',
    # 'fact_recommendations_pipeline',
    ]

    logging.basicConfig(
        filename='mage_pipeline_run.log',
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s'
    )

    results = {}
    for pipeline_name in PIPELINES:
        try:
            logging.info(f"Starting pipeline: {pipeline_name}")
            result = trigger_pipeline(pipeline_name)
            time.sleep(5)  # Wait for 5 seconds before triggering the next pipeline
            logging.info(f"Pipeline finished: {pipeline_name} | Result: {result}")
            results[pipeline_name] = result
        except Exception as e:
            logging.error(f"Pipeline {pipeline_name} failed: {e}")
            results[pipeline_name] = f'Failed: {e}'
    return results
