# API Usage Guide

## Quick Start Examples

### 1. Basic Stock Information

#### Get All Stocks (Paginated)
```bash
curl "http://localhost:8000/api/v1/stocks?page=1&page_size=10"
```

```python
import requests

response = requests.get("http://localhost:8000/api/v1/stocks", 
                       params={"page": 1, "page_size": 10})
stocks = response.json()
print(f"Found {stocks['meta']['total_count']} stocks")
```

#### Search Stocks
```bash
curl "http://localhost:8000/api/v1/stocks/search?q=TCS&limit=5"
```

```python
response = requests.get("http://localhost:8000/api/v1/stocks/search", 
                       params={"q": "TCS", "limit": 5})
results = response.json()
for stock in results['results']:
    print(f"{stock['symbol']}: {stock['company_name']}")
```

#### Get Stock Details
```bash
curl "http://localhost:8000/api/v1/stocks/TCS"
```

```python
response = requests.get("http://localhost:8000/api/v1/stocks/TCS")
stock_info = response.json()
print(f"Latest price: {stock_info.get('latest_price')}")
print(f"Data sources: {stock_info.get('data_sources')}")
```

### 2. Price Data (OHLCV)

#### Get Latest Price
```bash
curl "http://localhost:8000/api/v1/ohlcv/TCS/latest"
```

```python
response = requests.get("http://localhost:8000/api/v1/ohlcv/TCS/latest")
latest = response.json()
print(f"TCS latest close: ₹{latest['close_price']}")
```

#### Get Historical Data
```bash
# Last 30 days
curl "http://localhost:8000/api/v1/ohlcv/TCS?start_date=2024-01-01&end_date=2024-01-31"

# Predefined periods
curl "http://localhost:8000/api/v1/ohlcv/TCS/historical?period=1m"
```

```python
from datetime import datetime, timedelta

# Custom date range
end_date = datetime.now().date()
start_date = end_date - timedelta(days=30)

response = requests.get(f"http://localhost:8000/api/v1/ohlcv/TCS", 
                       params={
                           "start_date": start_date,
                           "end_date": end_date,
                           "page_size": 100
                       })
ohlcv_data = response.json()

# Process the data
for record in ohlcv_data['data']:
    print(f"{record['date']}: Open={record['open_price']}, Close={record['close_price']}")
```

#### Get Price Summary
```bash
curl "http://localhost:8000/api/v1/ohlcv/TCS/summary?days=30"
```

```python
response = requests.get("http://localhost:8000/api/v1/ohlcv/TCS/summary", 
                       params={"days": 30})
summary = response.json()
print(f"30-day change: {summary['change_percent']:.2f}%")
print(f"Min price: ₹{summary['min_price']}")
print(f"Max price: ₹{summary['max_price']}")
```

#### Get Technical Indicators
```bash
curl "http://localhost:8000/api/v1/ohlcv/TCS/technical?days=50"
```

```python
response = requests.get("http://localhost:8000/api/v1/ohlcv/TCS/technical", 
                       params={"days": 50})
indicators = response.json()
print(f"SMA 20: ₹{indicators['sma_20']}")
print(f"SMA 50: ₹{indicators['sma_50']}")
print(f"Trend: {indicators['trend']}")
```

### 3. Industry Analysis

#### Get All Industries
```bash
curl "http://localhost:8000/api/v1/stocks/industries"
```

```python
response = requests.get("http://localhost:8000/api/v1/stocks/industries")
industries = response.json()
print("Available industries:")
for industry in industries['industries']:
    print(f"- {industry}")
```

#### Get Stocks by Industry
```bash
curl "http://localhost:8000/api/v1/stocks/industries/Information%20Technology"
```

```python
response = requests.get("http://localhost:8000/api/v1/stocks/industries/Information Technology")
it_stocks = response.json()
print(f"Found {it_stocks['meta']['total_count']} IT companies")
```

## Advanced Usage Patterns

### 1. Building a Stock Screener

```python
import requests
import pandas as pd

class StockScreener:
    def __init__(self, base_url="http://localhost:8000/api/v1"):
        self.base_url = base_url
    
    def get_all_stocks(self, industry=None):
        """Get all stocks, optionally filtered by industry."""
        if industry:
            response = requests.get(f"{self.base_url}/stocks/industries/{industry}")
            return response.json()['data']
        else:
            all_stocks = []
            page = 1
            while True:
                response = requests.get(f"{self.base_url}/stocks", 
                                      params={"page": page, "page_size": 100})
                data = response.json()
                all_stocks.extend(data['data'])
                if not data['meta']['has_next']:
                    break
                page += 1
            return all_stocks
    
    def get_price_summaries(self, symbols, days=30):
        """Get price summaries for multiple stocks."""
        summaries = {}
        for symbol in symbols:
            try:
                response = requests.get(f"{self.base_url}/ohlcv/{symbol}/summary", 
                                      params={"days": days})
                if response.status_code == 200:
                    summaries[symbol] = response.json()
            except Exception as e:
                print(f"Error getting summary for {symbol}: {e}")
        return summaries
    
    def screen_by_performance(self, min_change_percent=5, days=30):
        """Screen stocks by performance criteria."""
        # Get all stocks
        stocks = self.get_all_stocks()
        symbols = [stock['symbol'] for stock in stocks]
        
        # Get price summaries
        summaries = self.get_price_summaries(symbols, days)
        
        # Filter by criteria
        winners = []
        for symbol, summary in summaries.items():
            if summary.get('change_percent', 0) >= min_change_percent:
                stock_info = next(s for s in stocks if s['symbol'] == symbol)
                winners.append({
                    'symbol': symbol,
                    'company_name': stock_info['company_name'],
                    'industry': stock_info['industry'],
                    'change_percent': summary['change_percent'],
                    'current_price': summary['current_price']
                })
        
        return sorted(winners, key=lambda x: x['change_percent'], reverse=True)

# Usage
screener = StockScreener()
top_performers = screener.screen_by_performance(min_change_percent=10, days=30)
for stock in top_performers[:10]:
    print(f"{stock['symbol']}: +{stock['change_percent']:.2f}% (₹{stock['current_price']})")
```

### 2. Portfolio Tracking

```python
class PortfolioTracker:
    def __init__(self, base_url="http://localhost:8000/api/v1"):
        self.base_url = base_url
        self.holdings = {}
    
    def add_holding(self, symbol, quantity, avg_price):
        """Add a stock holding to the portfolio."""
        self.holdings[symbol] = {
            'quantity': quantity,
            'avg_price': avg_price,
            'investment': quantity * avg_price
        }
    
    def get_portfolio_value(self):
        """Calculate current portfolio value."""
        total_value = 0
        total_investment = 0
        portfolio_data = []
        
        for symbol, holding in self.holdings.items():
            # Get current price
            response = requests.get(f"{self.base_url}/ohlcv/{symbol}/latest")
            if response.status_code == 200:
                current_price = response.json()['close_price']
                current_value = holding['quantity'] * current_price
                gain_loss = current_value - holding['investment']
                gain_loss_percent = (gain_loss / holding['investment']) * 100
                
                portfolio_data.append({
                    'symbol': symbol,
                    'quantity': holding['quantity'],
                    'avg_price': holding['avg_price'],
                    'current_price': current_price,
                    'investment': holding['investment'],
                    'current_value': current_value,
                    'gain_loss': gain_loss,
                    'gain_loss_percent': gain_loss_percent
                })
                
                total_value += current_value
                total_investment += holding['investment']
        
        total_gain_loss = total_value - total_investment
        total_gain_loss_percent = (total_gain_loss / total_investment) * 100
        
        return {
            'holdings': portfolio_data,
            'total_investment': total_investment,
            'total_value': total_value,
            'total_gain_loss': total_gain_loss,
            'total_gain_loss_percent': total_gain_loss_percent
        }

# Usage
portfolio = PortfolioTracker()
portfolio.add_holding('TCS', 100, 3500)
portfolio.add_holding('RELIANCE', 50, 2800)
portfolio.add_holding('INFY', 75, 1600)

portfolio_status = portfolio.get_portfolio_value()
print(f"Total Investment: ₹{portfolio_status['total_investment']:,.2f}")
print(f"Current Value: ₹{portfolio_status['total_value']:,.2f}")
print(f"Gain/Loss: ₹{portfolio_status['total_gain_loss']:,.2f} ({portfolio_status['total_gain_loss_percent']:.2f}%)")
```

### 3. Market Analysis Dashboard

```python
import matplotlib.pyplot as plt
import pandas as pd

class MarketAnalyzer:
    def __init__(self, base_url="http://localhost:8000/api/v1"):
        self.base_url = base_url
    
    def get_sector_performance(self, days=30):
        """Analyze performance by sector."""
        # Get all industries
        response = requests.get(f"{self.base_url}/stocks/industries")
        industries = response.json()['industries']
        
        sector_performance = {}
        
        for industry in industries[:10]:  # Limit to top 10 for demo
            try:
                # Get stocks in this industry
                response = requests.get(f"{self.base_url}/stocks/industries/{industry}")
                stocks = response.json()['data']
                
                if stocks:
                    # Get performance for first few stocks (sample)
                    sample_stocks = stocks[:5]
                    performance_sum = 0
                    count = 0
                    
                    for stock in sample_stocks:
                        response = requests.get(f"{self.base_url}/ohlcv/{stock['symbol']}/summary", 
                                              params={"days": days})
                        if response.status_code == 200:
                            summary = response.json()
                            performance_sum += summary.get('change_percent', 0)
                            count += 1
                    
                    if count > 0:
                        sector_performance[industry] = performance_sum / count
                        
            except Exception as e:
                print(f"Error analyzing {industry}: {e}")
        
        return sector_performance
    
    def plot_sector_performance(self, days=30):
        """Create a bar chart of sector performance."""
        performance = self.get_sector_performance(days)
        
        if performance:
            sectors = list(performance.keys())
            changes = list(performance.values())
            
            plt.figure(figsize=(12, 6))
            colors = ['green' if x > 0 else 'red' for x in changes]
            plt.bar(sectors, changes, color=colors, alpha=0.7)
            plt.title(f'Sector Performance - Last {days} Days')
            plt.xlabel('Sector')
            plt.ylabel('Average Change (%)')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.show()
    
    def get_market_movers(self, days=1, limit=10):
        """Get biggest market movers."""
        # This would require getting all stocks and their performance
        # Simplified version for demo
        top_gainers = []
        top_losers = []
        
        # Get sample of stocks
        response = requests.get(f"{self.base_url}/stocks", params={"page_size": 50})
        stocks = response.json()['data']
        
        for stock in stocks:
            try:
                response = requests.get(f"{self.base_url}/ohlcv/{stock['symbol']}/summary", 
                                      params={"days": days})
                if response.status_code == 200:
                    summary = response.json()
                    change_percent = summary.get('change_percent', 0)
                    
                    stock_data = {
                        'symbol': stock['symbol'],
                        'company_name': stock['company_name'],
                        'change_percent': change_percent,
                        'current_price': summary.get('current_price')
                    }
                    
                    if change_percent > 0:
                        top_gainers.append(stock_data)
                    else:
                        top_losers.append(stock_data)
                        
            except Exception as e:
                continue
        
        top_gainers = sorted(top_gainers, key=lambda x: x['change_percent'], reverse=True)[:limit]
        top_losers = sorted(top_losers, key=lambda x: x['change_percent'])[:limit]
        
        return {
            'top_gainers': top_gainers,
            'top_losers': top_losers
        }

# Usage
analyzer = MarketAnalyzer()

# Sector performance
print("Analyzing sector performance...")
analyzer.plot_sector_performance(days=30)

# Market movers
movers = analyzer.get_market_movers(days=1, limit=5)
print("\nTop Gainers:")
for stock in movers['top_gainers']:
    print(f"{stock['symbol']}: +{stock['change_percent']:.2f}%")

print("\nTop Losers:")
for stock in movers['top_losers']:
    print(f"{stock['symbol']}: {stock['change_percent']:.2f}%")
```

## Integration Examples

### 1. Integration with Popular Libraries

#### Pandas Integration
```python
import pandas as pd
import requests

def get_stock_data_as_dataframe(symbol, days=30):
    """Get stock OHLCV data as pandas DataFrame."""
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    
    response = requests.get(f"http://localhost:8000/api/v1/ohlcv/{symbol}/historical", 
                           params={"period": f"{days}d"})
    
    if response.status_code == 200:
        data = response.json()['data']
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        return df[['open_price', 'high_price', 'low_price', 'close_price', 'volume']]
    return None

# Usage
tcs_data = get_stock_data_as_dataframe('TCS', days=90)
print(tcs_data.head())
print(tcs_data.describe())
```

#### TA-Lib Integration
```python
import talib
import numpy as np

def calculate_technical_indicators(symbol, days=100):
    """Calculate technical indicators using TA-Lib."""
    df = get_stock_data_as_dataframe(symbol, days)
    
    if df is not None:
        # Convert to numpy arrays
        close = df['close_price'].values
        high = df['high_price'].values
        low = df['low_price'].values
        volume = df['volume'].values
        
        # Calculate indicators
        indicators = {
            'sma_20': talib.SMA(close, timeperiod=20),
            'sma_50': talib.SMA(close, timeperiod=50),
            'ema_12': talib.EMA(close, timeperiod=12),
            'ema_26': talib.EMA(close, timeperiod=26),
            'rsi': talib.RSI(close, timeperiod=14),
            'macd': talib.MACD(close),
            'bollinger': talib.BBANDS(close),
            'atr': talib.ATR(high, low, close),
            'adx': talib.ADX(high, low, close)
        }
        
        return indicators
    return None

# Usage
indicators = calculate_technical_indicators('TCS')
if indicators:
    print(f"RSI: {indicators['rsi'][-1]:.2f}")
    print(f"MACD: {indicators['macd'][0][-1]:.2f}")
```

### 2. Real-time Updates with WebSockets

```python
import asyncio
import websockets
import json

class RealTimeStockFeed:
    def __init__(self, api_base="http://localhost:8000/api/v1"):
        self.api_base = api_base
        self.subscriptions = set()
    
    def subscribe(self, symbol):
        """Subscribe to real-time updates for a symbol."""
        self.subscriptions.add(symbol)
    
    async def start_feed(self):
        """Start the real-time feed (simulated)."""
        while True:
            for symbol in self.subscriptions:
                try:
                    response = requests.get(f"{self.api_base}/ohlcv/{symbol}/latest")
                    if response.status_code == 200:
                        data = response.json()
                        print(f"{symbol}: ₹{data['close_price']} at {data['date']}")
                except Exception as e:
                    print(f"Error fetching {symbol}: {e}")
            
            await asyncio.sleep(60)  # Update every minute

# Usage
feed = RealTimeStockFeed()
feed.subscribe('TCS')
feed.subscribe('RELIANCE')
feed.subscribe('INFY')

# Run the feed
# asyncio.run(feed.start_feed())
```

## Best Practices

### 1. Error Handling

```python
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

class StockAPIClient:
    def __init__(self, base_url="http://localhost:8000/api/v1"):
        self.base_url = base_url
        self.session = requests.Session()
        
        # Configure retries
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
    
    def get_stock_data(self, symbol, **kwargs):
        """Get stock data with proper error handling."""
        try:
            response = self.session.get(f"{self.base_url}/stocks/{symbol}", 
                                      params=kwargs, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            print(f"Timeout error for {symbol}")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"Stock {symbol} not found")
            elif e.response.status_code == 429:
                print("Rate limit exceeded")
            else:
                print(f"HTTP error {e.response.status_code}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        return None
```

### 2. Rate Limiting and Caching

```python
import time
from functools import wraps

def rate_limit(calls_per_second=2):
    """Rate limiting decorator."""
    min_interval = 1.0 / calls_per_second
    last_called = [0.0]
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            left_to_wait = min_interval - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            ret = func(*args, **kwargs)
            last_called[0] = time.time()
            return ret
        return wrapper
    return decorator

@rate_limit(calls_per_second=1)
def get_stock_price(symbol):
    """Rate-limited stock price fetch."""
    response = requests.get(f"http://localhost:8000/api/v1/ohlcv/{symbol}/latest")
    return response.json()
```

### 3. Batch Operations

```python
import asyncio
import aiohttp

async def fetch_multiple_stocks_async(symbols):
    """Fetch multiple stocks concurrently."""
    async with aiohttp.ClientSession() as session:
        tasks = []
        for symbol in symbols:
            url = f"http://localhost:8000/api/v1/stocks/{symbol}"
            tasks.append(fetch_stock_data(session, url, symbol))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return dict(zip(symbols, results))

async def fetch_stock_data(session, url, symbol):
    """Fetch individual stock data."""
    try:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            return None
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None

# Usage
symbols = ['TCS', 'RELIANCE', 'INFY', 'WIPRO', 'HDFCBANK']
# results = asyncio.run(fetch_multiple_stocks_async(symbols))
```

This comprehensive API provides all the tools needed to build sophisticated financial applications with robust error handling, performance optimization, and real-time capabilities.
