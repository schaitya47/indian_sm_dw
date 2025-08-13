from mage_ai.data_cleaner.transformer_actions.base import BaseAction
from mage_ai.data_cleaner.transformer_actions.constants import ActionType, Axis
from mage_ai.data_cleaner.transformer_actions.utils import build_transformer_action
from pandas import DataFrame

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def execute_transformer_action(df: DataFrame, *args, **kwargs) -> DataFrame:
    """
    Execute Transformer Action: ActionType.CLEAN_COLUMN_NAME

    Docs: https://docs.mage.ai/guides/transformer-blocks#clean-column-names
    """
    action = build_transformer_action(
        df,
        action_type=ActionType.CLEAN_COLUMN_NAME,
        arguments=df.columns,
        axis=Axis.COLUMN,
    )
    df = BaseAction(action).execute(df)
    df['company_name'] = df['long_name']

    # Define key columns as per new table structure
    key_cols = ['symbol', 'company_name', 'industry', 'sector', 'load_ts']
    all_cols = set(df.columns)
    extra_cols = list(all_cols - set(key_cols))

    def make_extra_data(row):
        return {col: row[col] for col in extra_cols if pd.notnull(row[col])}

    import pandas as pd
    df['extra_data'] = df.apply(make_extra_data, axis=1)
    df_target = df[key_cols + ['extra_data']]
    
    return df_target


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
