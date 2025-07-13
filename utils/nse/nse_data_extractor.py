"""
    * NSE HISTORICAL DATA DOWNLOAD UTILITY *

    Description: This utility is Python Library to get publicly available historic candlestick data
     of stocks, index, its derivatives from the new NSE india website

    Timeframes supported are : 1m, 3m, 5m, 10m, 15m, 30m, 1h, 1d, 1w, 1M.

    Disclaimer : This utility is meant for educational purposes only. Downloading data from NSE
    website requires explicit approval from the exchange. Hence, the usage of this utility is for
    limited purposes only under proper/explicit approvals.

    Requirements : Following packages are to be installed (using pip) prior to using this utility
    - pandas
    - python 3.8 and above

"""

import pandas as pd
import time
import json
import requests
from datetime import datetime, timedelta
import re
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import random

class NSEMasterData:

    def __init__(self):
        self.session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=5,
            backoff_factor=2,
            status_forcelist=[429, 500, 502, 503, 504, 408, 444],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST"]
        )
        
        # Create adapter with retry strategy
        adapter = HTTPAdapter(max_retries=retry_strategy, pool_connections=10, pool_maxsize=10)
        
        # Mount adapter for both HTTP and HTTPS
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Enhanced headers to mimic real browser
        self.session.headers.update({
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'DNT': '1',
            'Upgrade-Insecure-Requests': '1',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Referer': 'https://www.nseindia.com/', 
            "Sec-Ch-Ua": '"Chromium";v="120", "Not=A?Brand";v="99"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"'
        })
        
        self.nse_url = "https://charting.nseindia.com/Charts/GetEQMasters"
        self.nfo_url = "https://charting.nseindia.com/Charts/GetFOMasters"
        self.historical_url = "https://charting.nseindia.com//Charts/symbolhistoricaldata/"
        self.nse_data = None
        self.nfo_data = None
        self.cookies_initialized = False

    def _initialize_cookies(self):
        """Initialize cookies by visiting NSE main website"""
        if not self.cookies_initialized:
            try:
                print("Initializing NSE cookies...")
                response = self.session.get("https://www.nseindia.com", timeout=10)
                if response.status_code == 200:
                    self.cookies_initialized = True
                    print("✓ Cookies initialized successfully")
                    # Add small delay after cookie initialization
                    time.sleep(random.uniform(2, 4))
                else:
                    print(f"⚠ Cookie initialization returned status code: {response.status_code}")
            except Exception as e:
                print(f"⚠ Cookie initialization failed: {e}")

    def search(self, symbol, exchange, match=False):
        """Search for symbols in the specified exchange.

        Args:
            symbol (str): The symbol or part of the symbol to search for.
            exchange (str): The exchange to search in ('NSE' or 'NFO').
            match (bool): If True, performs an exact match. If False, searches for symbols containing the input.

        Returns:
            pandas.DataFrame: A DataFrame containing all matching symbols.
        """
        exchange = exchange.upper()
        if exchange == 'NSE':
            df = self.nse_data
        elif exchange == 'NFO':
            df = self.nfo_data
        else:
            print(f"Invalid exchange '{exchange}'. Please choose 'NSE' or 'NFO'.")
            return pd.DataFrame()

        if df is None:
            print(f"Data for {exchange} not downloaded. Please run download_symbol_master() first.")
            return pd.DataFrame()

        if match:
            result = df[df['Symbol'].str.upper() == symbol.upper()]
        else:
            result = df[df['Symbol'].str.contains(symbol, case=False, na=False)]

        if result.empty:
            print(f"No matching result found for symbol '{symbol}' in {exchange}.")
            return pd.DataFrame()

        return result.reset_index(drop=True)

    def get_nse_symbol_master(self, url, max_retries=3):
        """Get NSE symbol master data with enhanced error handling"""
        for attempt in range(max_retries):
            try:
                print(f"Fetching master data from {url} (attempt {attempt + 1}/{max_retries})")
                
                # Initialize cookies if not done
                self._initialize_cookies()
                
                # Add random delay to avoid rate limiting
                time.sleep(random.uniform(3, 6))
                
                # Make request with longer timeout
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                
                data = response.text.strip()
                if not data:
                    raise ValueError("Empty response received")
                
                # Parse data
                lines = data.splitlines()
                if not lines:
                    raise ValueError("No data lines found")
                
                columns = ['ScripCode', 'Symbol', 'Name', 'Type']
                parsed_data = []
                
                for line in lines:
                    if line.strip():  # Skip empty lines
                        parts = line.split('|')
                        if len(parts) >= 4:  # Ensure we have enough columns
                            parsed_data.append(parts[:4])  # Take only first 4 columns
                
                if not parsed_data:
                    raise ValueError("No valid data rows found")
                
                df = pd.DataFrame(parsed_data, columns=columns)
                print(f"✓ Successfully downloaded {len(df)} records")
                return df
                
            except requests.exceptions.Timeout:
                print(f"✗ Timeout error on attempt {attempt + 1}")
            except requests.exceptions.RequestException as e:
                print(f"✗ Request error on attempt {attempt + 1}: {e}")
            except Exception as e:
                print(f"✗ Unexpected error on attempt {attempt + 1}: {e}")
            
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 10 + random.uniform(5, 15)
                print(f"Waiting {wait_time:.1f} seconds before retry...")
                time.sleep(wait_time)
        
        print(f"✗ Failed to download data from {url} after {max_retries} attempts")
        return pd.DataFrame()

    def download_symbol_master(self):
        """Download NSE and NFO master data with enhanced error handling"""
        print("Starting master data download...")
        
        # Download NSE data
        print("Downloading NSE master data...")
        self.nse_data = self.get_nse_symbol_master(self.nse_url)
        
        if not self.nse_data.empty:
            print(f"✓ NSE data downloaded: {len(self.nse_data)} symbols")
        else:
            print("✗ NSE data download failed")
        
        # Add delay between downloads
        time.sleep(random.uniform(5, 10))
        
        # Download NFO data
        print("Downloading NFO master data...")
        self.nfo_data = self.get_nse_symbol_master(self.nfo_url)
        
        if not self.nfo_data.empty:
            print(f"✓ NFO data downloaded: {len(self.nfo_data)} symbols")
        else:
            print("✗ NFO data download failed")

    def search_symbol(self, symbol, exchange):
        """Search for a symbol in the specified exchange and return the first match."""
        df = self.nse_data if exchange.upper() == 'NSE' else self.nfo_data
        if df is None or df.empty:
            print(f"Data for {exchange} not downloaded. Please run download_symbol_master() first.")
            return None
        
        result = df[df['Symbol'].str.contains(symbol, case=False, na=False)]
        if result.empty:
            print(f"No matching result found for symbol '{symbol}' in {exchange}.")
            return None
        return result.iloc[0]

    def get_history(self, symbol="Nifty 50", exchange="NSE", start=None, end=None, interval='1d', max_retries=3):
        """Get historical data for a symbol with enhanced error handling."""

        def adjust_timestamp(ts):
            if interval in ['30m', '1h']:
                num = 15
            elif interval in ['10m']:
                num = 5
            else:
                num = int(re.match(r'\d+', interval).group())
            if num == 0:
                return (ts - timedelta(minutes=num)).round('min')
            else:
                return (ts - timedelta(minutes=num)).round((str(num) + 'min'))

        symbol_info = self.search_symbol(symbol, exchange)
        if symbol_info is None:
            return pd.DataFrame()

        interval_xref = {
            '1m': ('1', 'I'), '3m': ('3', 'I'), '5m': ('5', 'I'), '10m': ('5', 'I'),
            '15m': ('15', 'I'), '30m': ('15', 'I'), '1h': ('15', 'I'),
            '1d': ('1', 'D'), '1w': ('1', 'W'), '1M': ('1', 'M')
        }

        time_interval, chart_period = interval_xref.get(interval, ('1', 'D'))

        payload = {
            "exch": "N" if exchange.upper() == "NSE" else "D",
            "instrType": "C" if exchange.upper() == "NSE" else "D",
            "ScripCode": int(symbol_info['ScripCode']),
            "ulScripCode": int(symbol_info['ScripCode']),
            "fromDate": int(start.timestamp()) if start else 0,
            "toDate": int(end.timestamp()) if end else int(time.time()),
            "timeInterval": time_interval,
            "chartPeriod": chart_period,
            "chartStart": 0
        }

        for attempt in range(max_retries):
            try:
                print(f"Fetching historical data for {symbol} (attempt {attempt + 1}/{max_retries})")
                
                # Initialize cookies if not done
                self._initialize_cookies()
                
                # Add delay between requests
                time.sleep(random.uniform(3, 7))
                
                # Update headers for JSON request
                self.session.headers.update({
                    'Content-Type': 'application/json',
                    'Accept': 'application/json, text/plain, */*'
                })
                
                response = self.session.post(self.historical_url, 
                                           data=json.dumps(payload), 
                                           timeout=30)
                response.raise_for_status()
                
                data = response.json()

                if not data:
                    print("No data received from the Source - NSE.")
                    return pd.DataFrame()

                df = pd.DataFrame(data)
                df.columns = ['Status', 'TS', 'Open', 'High', 'Low', 'Close', 'Volume']
                df['TS'] = pd.to_datetime(df['TS'], unit='s', utc=True)
                df['TS'] = df['TS'].dt.tz_localize(None)
                df = df[['TS', 'Open', 'High', 'Low', 'Close', 'Volume']]

                # Apply cutoff time only for intraday intervals
                intraday_intervals = ['1m', '3m', '5m', '15m']
                intraday_consolidate_intervals = ['10m','30m', '1h']
                
                if interval in intraday_intervals:
                    cutoff_time = pd.Timestamp('15:30:00').time()
                    df = df[df['TS'].dt.time <= cutoff_time]
                    df['Timestamp'] = df['TS'].apply(adjust_timestamp)
                    df.drop(columns=['TS'], inplace=True)
                    df.set_index('Timestamp', inplace=True, drop=True)
                    print(f"✓ Successfully fetched {len(df)} records for {symbol}")
                    return df
                
                if interval in intraday_consolidate_intervals:
                    cutoff_time = pd.Timestamp('15:30:00').time()
                    df = df[df['TS'].dt.time <= cutoff_time]
                    df['Timestamp'] = df['TS'].apply(adjust_timestamp)
                    df.drop(columns=['TS'], inplace=True)
                    df.set_index('Timestamp', inplace=True, drop=True)
                    
                    agg_parm = ''
                    if interval == '30m':
                        agg_parm = '30min'
                    elif interval == '10m':
                        agg_parm = '10min'
                    else:
                        agg_parm = '60min'
                    
                    # Get the first timestamp to use as custom origin
                    first_ts = df.index.min()
                    offset_td = pd.to_timedelta(first_ts.time().strftime('%H:%M:%S'))
                    df_aggregated = df.resample(agg_parm, origin='start_day', offset=offset_td).agg({
                        'Open': 'first',
                        'High': 'max',
                        'Low': 'min',
                        'Close': 'last',
                        'Volume': 'sum'
                    })
                    df_aggregated.dropna(inplace=True)
                    print(f"✓ Successfully fetched and aggregated {len(df_aggregated)} records for {symbol}")
                    return df_aggregated

                df.rename(columns={'TS': 'Timestamp'}, inplace=True)
                df.set_index('Timestamp', inplace=True, drop=True)
                print(f"✓ Successfully fetched {len(df)} records for {symbol}")
                return df

            except requests.exceptions.Timeout:
                print(f"✗ Timeout error on attempt {attempt + 1}")
            except requests.exceptions.RequestException as e:
                print(f"✗ Request error on attempt {attempt + 1}: {e}")
            except Exception as e:
                print(f"✗ Unexpected error on attempt {attempt + 1}: {e}")
            
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 10 + random.uniform(5, 15)
                print(f"Waiting {wait_time:.1f} seconds before retry...")
                time.sleep(wait_time)

        print(f"✗ Failed to fetch historical data for {symbol} after {max_retries} attempts")
        return pd.DataFrame()

    def download_nifty50_csv(self, save_path: str = "resource/ind_nifty50list.csv") -> pd.DataFrame:
        """Download Nifty 50 CSV with enhanced error handling"""
        url = "https://nsearchives.nseindia.com/content/indices/ind_nifty50list.csv"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/csv",
            "Referer": "https://www.nseindia.com/",
            "Connection": "keep-alive",
        }

        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"Downloading Nifty 50 CSV (attempt {attempt + 1}/{max_retries})")
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()

                # Save to file
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                print(f"✓ File saved as: {save_path}")

                # Also load as DataFrame
                df = pd.read_csv(save_path)
                print(f"✓ Successfully loaded {len(df)} Nifty 50 companies")
                return df

            except Exception as e:
                print(f"✗ Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 5
                    print(f"Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)

        print(f"✗ Failed to download Nifty 50 CSV after {max_retries} attempts")
        return pd.DataFrame()