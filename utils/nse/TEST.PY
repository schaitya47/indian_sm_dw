import requests
import pandas as pd
from bs4 import BeautifulSoup
import yfinance as yf
import json
import time
from typing import List, Dict, Optional
import warnings
warnings.filterwarnings('ignore')

def get_nifty50_from_screener_v2() -> Optional[pd.DataFrame]:
        """
        Enhanced Screener.in parsing with multiple methods
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        session = requests.Session()
        session.headers.update(headers)
        try:
            print("Trying Screener.in v2...")
            
            url = "https://www.screener.in/company/NIFTY/"
            response = session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            print(soup.title.string)
            companies = []
            
            # Method 1: Look for company links in the constituents section
            company_links = soup.find_all('a', href=lambda x: x and '/company/' in x)
            print(company_links)
            
            seen_symbols = set()
            for link in company_links:
                href = link.get('href', '')
                if '/company/' in href:
                    parts = href.split('/')
                    if len(parts) >= 3 and parts[1] == 'company':
                        symbol = parts[2]
                        company_name = link.text.strip()
                        
                        # Validate symbol
                        if (symbol and 
                            symbol not in seen_symbols and 
                            not symbol.startswith('NIFTY') and 
                            len(symbol) <= 20 and 
                            symbol.replace('-', '').replace('&', '').isalnum()):
                            
                            seen_symbols.add(symbol)
                            companies.append({
                                'Company': company_name,
                                'NSE_Symbol': symbol,
                                'Yahoo_Symbol': f"{symbol}.NS",
                                'Source': 'Screener.in v2'
                            })
            
            # Keep only first 50 valid companies
            if len(companies) >= 45:
                print(f"✓ Successfully fetched {len(companies)} companies from Screener.in")
                return pd.DataFrame(companies[:50])
                
        except Exception as e:
            print(f"✗ Screener.in v2 failed: {e}")
            return None

x = get_nifty50_from_screener_v2()

print(x)