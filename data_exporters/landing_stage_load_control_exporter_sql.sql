-- Docs: https://docs.mage.ai/guides/sql-blocks
-- This SQL block updates the last success timestamp for a specific pipeline in the stage_load_control table.
-- It uses the pipeline name provided in the context to identify the correct record.
UPDATE stock_landing.stage_load_control
SET last_success_timestamp = NOW() AT TIME ZONE 'Asia/Kolkata'
WHERE pipeline_name = '{{ pipeline_name }}';
