-- Database initialization script
-- This script sets up the required schemas and extensions

-- Create schemas if they don't exist
CREATE SCHEMA IF NOT EXISTS stock_landing;
CREATE SCHEMA IF NOT EXISTS stock_dw;

-- Grant permissions
GRANT ALL PRIVILEGES ON SCHEMA stock_landing TO postgres;
GRANT ALL PRIVILEGES ON SCHEMA stock_dw TO postgres;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA stock_landing TO postgres;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA stock_dw TO postgres;

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Set default privileges
ALTER DEFAULT PRIVILEGES IN SCHEMA stock_landing GRANT ALL ON TABLES TO postgres;
ALTER DEFAULT PRIVILEGES IN SCHEMA stock_dw GRANT ALL ON TABLES TO postgres;
