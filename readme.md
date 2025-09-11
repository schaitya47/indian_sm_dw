# Indian Stock Market Data Warehouse (indian_sm_dw)

[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)](https://www.docker.com/)
[![Mage AI](https://img.shields.io/badge/Mage%20AI-6B46C1?style=flat-square)](https://www.mage.ai/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat-square&logo=postgresql&logoColor=white)](https://postgresql.org/)
[![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org/)

A comprehensive ETL data warehouse solution for Indian stock market data using **Mage AI**, **PostgreSQL**, and **Docker**. This project automates the collection, transformation, and storage of stock market data from multiple sources including Yahoo Finance, NSE, and TickerTape.

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Data Sources  │    │   Mage AI ETL    │    │  Data Warehouse │
│                 │    │                  │    │                 │
│ • Yahoo Finance │───▶│ • Data Loaders   │───▶│ • Landing Layer │
│ • NSE           │    │ • Transformers   │    │ • DW Layer      │
│ • TickerTape    │    │ • Data Exporters │    │ • Facts & Dims  │
│ • Screener.in   │    │ • Pipelines      │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   FastAPI       │
                       │   REST API      │
                       └─────────────────┘
```

## 📊 Data Pipeline Structure

### Landing Layer Pipelines
- **Nifty 50 Companies**: Loads company metadata and symbols
- **Daily Stock Data**: OHLCV data from Yahoo Finance and NSE
- **Weekly/Monthly Data**: Aggregated historical data
- **Financial Statements**: Balance sheet, income statement, cash flow
- **Key Ratios**: Financial ratios and metrics
- **Recommendations**: Analyst recommendations

### Data Warehouse Layer
- **Dimension Tables**: Stock metadata, company information
- **Fact Tables**: OHLCV, financial statements, ratios, recommendations
- **Master Pipeline**: Orchestrates the entire ETL workflow

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Git
- At least 4GB RAM recommended

### 1. Clone the Repository
```bash
git clone -b docker_devlop https://github.com/schaitya47/indian_sm_dw.git
cd indian_sm_dw
```

### 2. Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Edit environment variables
# Windows (PowerShell)
notepad .env

# Linux/Mac
nano .env
```

### 3. Environment Configuration
Update `.env` file with your database credentials:
```bash
# Database Configuration
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=indian_sm_dw
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# Docker Configuration
UID=1000
GID=1000

# Optional: Slack/Teams Notifications
MAGE_SLACK_WEBHOOK_URL=your_slack_webhook
MAGE_TEAMS_WEBHOOK_URL=your_teams_webhook
```

### 4. Start the Application
```bash
# Build and start all services
docker compose up --build -d

# Check container status
docker compose ps

# View logs (optional)
docker compose logs -f mage
```

### 5. Access the Applications
- **Mage AI Dashboard**: http://localhost:6789
- **PostgreSQL**: localhost:5432
- **API Documentation**: Check `indian_sm_dw_api` folder

## 🎯 Usage Guide

### Running ETL Pipelines

1. **Access Mage AI Dashboard**: Navigate to http://localhost:6789
2. **Navigate to Pipelines**: Browse available pipelines in the sidebar
3. **Run Individual Pipelines**:
   - `get_nifty50_companies`: Load Nifty 50 company list (run first)
   - `yfin_landing_daily`: Daily stock data from Yahoo Finance
   - `nse_landing_daily`: Daily data from NSE
   - `tick_landing_monthly`: Monthly data from TickerTape
4. **Run Master Pipeline**: `dw_master_pipeline` orchestrates all data flows

### Pipeline Execution Order
```bash
1. get_nifty50_companies          # Load company metadata
2. landing_master_trigger         # Load raw data
3. dw_master_pipeline            # Transform and load to DW
```

### Database Schema
```sql
-- Landing Layer
stock_landing.nifty_50_companies
stock_landing.yfin_stock_daily
stock_landing.nse_stock_daily
stock_landing.tick_stock_balance_sheet_tbls
stock_landing.tick_stock_income_tbls
stock_landing.tick_stock_cash_flow_tbls

-- Data Warehouse Layer
stock_dw.dim_stock
stock_dw.fact_ohlcv
stock_dw.fact_balance_sheet
stock_dw.fact_income
stock_dw.fact_cash_flow
stock_dw.fact_key_ratios
stock_dw.fact_recommendations
```

## 🛠️ Development Setup

### Local Development (without Docker)
```bash
# Create virtual environment
python -m venv mage_env
mage_env\Scripts\activate  # Windows
# source mage_env/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Start PostgreSQL (ensure it's running)
# Update io_config.yaml with local database settings

# Start Mage AI
mage start .
```

### Adding Custom Data Sources
1. Create new data loader in `data_loaders/`
2. Add transformation logic in `transformers/`
3. Create data exporter in `data_exporters/`
4. Build pipeline using Mage AI UI

### Database Connection
```python
# Example connection in Mage blocks
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from os import path

config_path = path.join(get_repo_path(), 'io_config.yaml')
config_profile = 'default'

with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
    df = loader.load('SELECT * FROM stock_landing.nifty_50_companies')
```

## 🌐 Cloud Deployment (GCP)

### GCP Setup
```bash
# Create VM instance
gcloud compute instances create mage-indian-sm-dw \
    --zone=us-central1-a \
    --machine-type=e2-medium \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=50GB \
    --tags=mage-server

# Configure firewall rules
gcloud compute firewall-rules create allow-mage-6789 \
    --network=default \
    --action=ALLOW \
    --rules=tcp:6789 \
    --source-ranges=YOUR_IP/32 \
    --target-tags=mage-server

gcloud compute firewall-rules create allow-postgres-5432 \
    --network=default \
    --action=ALLOW \
    --rules=tcp:5432 \
    --source-ranges=YOUR_IP/32 \
    --target-tags=mage-server
```

### Deployment Steps
```bash
# SSH to instance
gcloud compute ssh mage-indian-sm-dw --zone=us-central1-a

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Clone and deploy
git clone -b docker_devlop https://github.com/schaitya47/indian_sm_dw.git
cd indian_sm_dw
cp .env.example .env
# Edit .env file
sudo docker compose up --build -d
```

## 📋 Management Commands

### Docker Operations
```bash
# Start services
docker compose up -d

# Stop services
docker compose down

# Restart specific service
docker compose restart mage

# View logs
docker compose logs -f mage
docker compose logs -f postgres

# Access container shell
docker compose exec mage bash
docker compose exec postgres psql -U postgres -d indian_sm_dw

# Backup database
docker compose exec postgres pg_dump -U postgres indian_sm_dw > backup.sql

# Restore database
docker compose exec -T postgres psql -U postgres indian_sm_dw < backup.sql
```

### Pipeline Management
```bash
# Run pipeline via CLI (inside mage container)
docker compose exec mage mage run indian_sm_dw get_nifty50_companies

# Schedule pipelines (via Mage AI UI)
# Trigger pipelines (via Mage AI UI or API)
```

## 🔧 Configuration

### Key Configuration Files
- `docker-compose.yml`: Container orchestration
- `Dockerfile`: Mage AI container setup
- `io_config.yaml`: Database and external service configurations
- `metadata.yaml`: Mage AI project settings
- `requirements.txt`: Python dependencies
- `.env`: Environment variables

### External Dependencies
- **Yahoo Finance API**: Stock data and financial information
- **NSE Data**: Indian stock exchange data
- **TickerTape API**: Financial statements and ratios
- **Screener.in**: Additional financial metrics

## 📊 Monitoring & Logs

### Log Locations
```bash
# Application logs
docker compose logs mage

# Pipeline execution logs
./logs/mage_pipeline_run.log

# Database logs
docker compose logs postgres
```

### Health Checks
```bash
# Check database connectivity
docker compose exec postgres pg_isready -U postgres

# Check Mage AI status
curl http://localhost:6789/health
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions:
- Create an issue in this repository
- Check the troubleshooting section below
- Review Mage AI documentation: https://docs.mage.ai/

---

## 🐛 Known Issues & Troubleshooting

### 1. SQL Issues in Mage AI Blocks
- **Problem**: SQL syntax and formatting issues in Mage AI blocks
- **Common Issues**:
  - Don't use comment in SQL block which are used in mage AI. 
  - Check for semi colon that also creates issue in mage AI block.
- **Detailed Solutions**:
  - **Comments**: 
    - **Issue**: SQL comments (`--` or `/* */`) can interfere with Mage AI's SQL parsing
    - **Solution**: Remove all SQL comments from blocks or use alternative documentation methods
    - **Files**: All `.sql` files in `data_loaders/`, `data_exporters/`, `transformers/`
  - **Semicolons**: 
    - **Issue**: Trailing semicolons (`;`) at the end of SQL statements can cause execution errors
    - **Solution**: Remove semicolons from the end of SQL statements in Mage blocks
    - **Example**: Change `SELECT * FROM table;` to `SELECT * FROM table`
- **Best Practices**:
  - Test SQL queries in a database client before adding to Mage blocks
  - Use consistent indentation and formatting
  - Validate table and column names exist in the target database
  - Use parameterized queries for dynamic values

### 2. SSL Certificate Issues with API Calls
- **Problem**: API calls to external services (like TickerTape, Screener.in) fail with SSL certificate verification errors
- **Symptoms**: 
  - `TypeError: 'NoneType' object is not iterable` errors
  - API responses returning None instead of expected data
  - SSL certificate verification failures in logs
- **Solution**: Disable SSL certificate verification in the CustomSession base class
  - **File**: `c:\Mage_AI\mage_env\Lib\site-packages\Base\CustomRequest.py`
  - **Changes made**:
    1. **Lines 1-5**: Add urllib3 import and disable SSL warnings:
       ```python
       import json
       import brotli
       import urllib3
       from requests import Session, session
       from requests.adapters import HTTPAdapter, Retry
       
       # Disable SSL warnings when verify=False is used
       urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
       ```
    2. **Line ~45**: Set `self.session.verify = False` in the `__init__` method after timeout setting
    3. **Lines ~75-80**: Add `verify=False` parameter to both GET requests in `hit_and_get_data` method:
       ```python
       response = self.session.get(url, params=params, headers=self.headers, verify=False)
       response = self.session.get(url, headers=self.headers, verify=False)
       ```
- **Security Note**: This disables SSL certificate verification - acceptable for development/testing but should be re-evaluated for production use

### 3. String Literal Issues in Third-Party Libraries
- **Problem**: Syntax errors due to embedded newlines in string literals
- **Symptoms**: `SyntaxError: unterminated string literal` errors
- **Files Affected**:
  - **File**: `c:\Mage_AI\mage_env\Lib\site-packages\Fundamentals\Screener.py`
  - **Line**: ~502-503
- **Solution**: Replace problematic string handling with safer text extraction methods
  - **Original problematic code**:
    ```python
    raise ValueError(f"Error: setting columns requires Premium Account: {error.text.strip().replace('\n', ' ')}")
    ```
  - **Fixed code**:
    ```python
    # Use get_text with separator to robustly collapse any internal newlines/whitespace
    msg = error.get_text(separator=' ', strip=True)
    raise ValueError(f"Error: setting columns requires Premium Account: {msg}")
    ```
  - Move inline comments to separate lines to avoid string parsing issues

### 4. Regex Escape Issues in Mage AI Server
- **Problem**: Regular expression errors when processing file paths or strings with backslashes
- **Symptoms**: 
  - `re.error: bad escape \M at position 3` or similar regex errors
  - WebSocket server errors during code execution
  - Issues with Windows file paths containing backslashes in replacement strings
- **Root Cause**: Mage AI's `output_display.py` uses `re.sub()` without properly escaping backslashes in replacement strings
- **Solution**: Manually escape backslashes in replacement strings before regex substitution
  - **File**: `c:\Mage_AI\mage_env\Lib\site-packages\mage_ai\server\utils\output_display.py`
  - **Line**: ~202 (in `__interpolate_code_content` function)
  - **Original problematic code**:
    ```python
    content = re.sub(placeholder_pattern, str(replacement), content)
    ```
  - **Fixed code**:
    ```python
    safe_replacement = str(replacement).replace('\\', r'\\')
    content = re.sub(placeholder_pattern, safe_replacement, content)
    ```
- **Explanation**: This fix escapes single backslashes (`\`) to double backslashes (`\\`) to prevent regex interpretation issues
- **Impact**: Prevents regex parsing errors when Windows file paths or other strings contain backslashes

### 5. Common Docker Issues
- **Port Conflicts**: Ensure ports 5432 and 6789 are available
- **Memory Issues**: Increase Docker memory allocation if containers fail to start
- **Volume Permissions**: On Linux, ensure proper UID/GID settings in `.env` file

### 6. Data Source Issues
- **API Rate Limits**: Some data sources may have rate limiting
- **Network Connectivity**: Ensure internet access for external APIs
- **Data Format Changes**: Monitor for changes in external API response formats

