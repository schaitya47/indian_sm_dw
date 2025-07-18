from utils.nse.nse_data_extractor import NSEMasterData
from datetime import datetime, timedelta

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@custom
def transform_custom(*args, **kwargs):
    nse = NSEMasterData()
    df = nse.download_nifty50_csv()
    df["yfin_symbol"] = df["Symbol"] +".NS"
    df["load_ts"] = datetime.now()
    
    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
