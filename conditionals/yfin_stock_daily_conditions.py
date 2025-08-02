if 'condition' not in globals():
    from mage_ai.data_preparation.decorators import condition


@condition
def evaluate_condition(val,*args, **kwargs) -> bool:
    if len(val) == 0:
        return False
    else:
        return True