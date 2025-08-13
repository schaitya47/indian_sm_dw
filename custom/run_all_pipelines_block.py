
import logging
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

    # Ensure logs directory exists
    log_dir = 'C:/Mage_AI/indian_sm_dw/logs'
    os.makedirs(log_dir, exist_ok=True)
    
    # Configure logging with force parameter to reset any existing config
    log_file = os.path.join(log_dir, 'mage_pipeline_run.log')
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filemode='a',
        force=True
    )
    
    # Also add console handler for immediate feedback
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    
    # Get the root logger and add console handler
    logger = logging.getLogger()
    logger.addHandler(console_handler)
    
    logging.info("="*60)
    logging.info("Starting pipeline execution batch")
    logging.info(f"Total pipelines to execute: {len(PIPELINES)}")
    logging.info("="*60)

    results = {}
    for pipeline_name in PIPELINES:
        try:
            logging.info(f"Starting pipeline: {pipeline_name}")
            # print(f"Starting pipeline: {pipeline_name}")
            result = trigger_pipeline(pipeline_name).to_dict()
            # logging.debug(f"Trigger result for {pipeline_name}: {result}")
            run_id = result.get('id') if isinstance(result, dict) else None
            # logging.debug(f"Run ID for {pipeline_name}: {run_id}")
            if not run_id:
                raise Exception(f"No run id returned for pipeline {pipeline_name}")

            # Wait for pipeline to complete
            wait_time = 0   
            status = None

            while True:
                # print(f"run_id: {run_id}")
                run = PipelineRun.get(run_id)
                if run:
                    run.refresh()
                run_details = run.to_dict() if run else {}
                # logging.debug(f"Pipeline run details for {pipeline_name}: {run_details}")
                status = run.status.value if run and hasattr(run.status, 'value') else (run.status if run else None)
                logging.info(f"Pipeline Name: {pipeline_name} | Current status: {status}")
                # logging.debug(f"Polling run_id: {run_id}, status: {status}, wait_time: {wait_time}s")
                if status and status.lower() in ['completed', 'failed', 'cancelled']:
                    break
                time.sleep(5)
                wait_time += 5
                if wait_time > 1200:  # 20 minutes timeout
                    raise Exception(f"Timeout waiting for pipeline {pipeline_name} to finish.")

            logging.info(f"Pipeline finished: {pipeline_name} | Status: {status}")
            results[pipeline_name] = status
            if status != 'completed':
                raise Exception(f"Pipeline {pipeline_name} did not complete successfully. Status: {status}")
        except Exception as e:
            logging.error(f"Pipeline {pipeline_name} failed: {e}")
            print(f"Pipeline {pipeline_name} failed: {e}")
            results[pipeline_name] = f'Failed: {e}'
            break  # Stop execution if any pipeline fails
            
    # Log final results
    logging.info("="*60)
    logging.info("Pipeline execution batch completed")
    logging.info(f"Results summary: {results}")
    logging.info("="*60)
    
    print("Final results:", results)
    return results
