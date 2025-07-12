import requests
import pandas as pd

def download_nifty50_csv(save_path: str = "ind_nifty50list.csv") -> pd.DataFrame:
    url = "https://nsearchives.nseindia.com/content/indices/ind_nifty50list.csv"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/csv",
        "Referer": "https://www.nseindia.com/",
        "Connection": "keep-alive",
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        # Save to file
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"✓ File saved as: {save_path}")

        # Also load as DataFrame
        df = pd.read_csv(save_path)
        return df

    except Exception as e:
        print(f"✗ Failed to download file: {e}")
        return pd.DataFrame()

