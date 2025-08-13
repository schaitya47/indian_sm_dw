
from utils.logger_genrator import get_logger
import time
import os
from mage_ai.orchestration.triggers.api import trigger_pipeline
from mage_ai.orchestration.db.models.schedules import PipelineRun

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
    'yfin_landing_weekly',
    'dim_stock_dw',
    'fact_balance_sheet_dw',
    'fact_cashflow_dw',
    'fact_income_dw',
    'fact_key_ratios_dw',
    'fact_ohlcv_dw',
    'fact_recommendations_dw'
    ]

    log_file = os.path.join('C:/Mage_AI/indian_sm_dw/logs', 'mage_pipeline_run.log')
    
    logger = get_logger(log_file)

    logger.info("="*60)
    logger.info("Starting pipeline execution batch")
    logger.info(f"Total pipelines to execute: {len(PIPELINES)}")
    logger.info("="*60)

    results = {}
    for pipeline_name in PIPELINES:
        try:
            logger.info(f"Starting pipeline: {pipeline_name}")
            result = trigger_pipeline(pipeline_name).to_dict()
            run_id = result.get('id') if isinstance(result, dict) else None
            if not run_id:
                raise Exception(f"No run id returned for pipeline {pipeline_name}")

            wait_time = 0
            status = None
            while True:
                run = PipelineRun.get(run_id)
                if run:
                    run.refresh()
                status = run.status.value if run and hasattr(run.status, 'value') else (run.status if run else None)
                logger.info(f"Pipeline Name: {pipeline_name} | Current status: {status}")
                if status and status.lower() in ['completed', 'failed', 'cancelled']:
                    break
                time.sleep(5)
                wait_time += 5
                if wait_time > 1200:
                    raise Exception(f"Timeout waiting for pipeline {pipeline_name} to finish.")

            logger.info(f"Pipeline finished: {pipeline_name} | Status: {status}")
            results[pipeline_name] = status
            if status != 'completed':
                raise Exception(f"Pipeline {pipeline_name} did not complete successfully. Status: {status}")
        except Exception as e:
            logger.error(f"Pipeline {pipeline_name} failed: {e}")
            print(f"Pipeline {pipeline_name} failed: {e}")
            results[pipeline_name] = f'Failed: {e}'
            break

    logger.info("="*60)
    logger.info("Pipeline execution batch completed")
    logger.info(f"Results summary: {results}")
    logger.info("="*60)
    print("Final results:", results)
    return results
