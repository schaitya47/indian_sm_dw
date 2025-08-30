from utils.nse.nse_data_extractor import NSEMasterData
from datetime import datetime as dt, timedelta, timezone

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@custom
def transform_custom(*args, **kwargs):
    # This function is used to download the Nifty 50 companies data from NSE and transform it.
    # It returns a DataFrame with the required columns.
    nse = NSEMasterData()
    df = nse.download_nifty50_csv()
    df["yfin_symbol"] = df["Symbol"] +".NS"
    df["load_ts"] = dt.now(timezone(timedelta(hours=5, minutes=30)))
    
    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
