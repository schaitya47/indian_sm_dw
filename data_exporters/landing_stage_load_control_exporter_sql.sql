-- Docs: https://docs.mage.ai/guides/sql-blocks
UPDATE stock_landing.stage_load_control
SET last_success_timestamp = NOW()
WHERE pipeline_name = '{{ pipeline_name }}';
