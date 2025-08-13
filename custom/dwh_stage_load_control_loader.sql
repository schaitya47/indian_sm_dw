SELECT last_success_timestamp 
FROM stock_landing.stage_load_control 
where pipeline_name = '{{ pipeline_name }}'