import pandas as pd
import logging
from functools import wraps
import inspect
import numpy as np

_logger = logging.getLogger(__name__)

def log_shape_change(df_name):
    """
    This decorator will log the shape change of a pd.DataFrame before and after a transform
    function is applied. Please note that the function to be applied with this decorator should
    take one pd.DataFrame and return a pd.DataFrame. The name of the DataFrame that needs to
    be logged should be given in the `df_name` decorator parameter.

    Note:
        - Only log one dataframe. The name of the dataframe must be indicated in `df_name`.

    Example:

        @log_shape_change(df_name='home_df')
        def remove_low_dom_homes(home_df: pd.DataFrame,
                                 market: str,
                                 channel: str) -> pd.DataFrame:
            # remove home logic
            # ...
            return df

        >>> Before remove_low_dom_homes, home_df shape=(10, 5)
        >>> After remove_low_dom_homes: home_df shape=(5, 5)
    """

    def decorator_log_shape(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func_callargs = inspect.getcallargs(func, *args, **kwargs)

            if df_name not in func_callargs.keys():
                _logger.error(f'{df_name} does not exist.')

            df = func_callargs[df_name]

            if isinstance(df, pd.DataFrame):
                _logger.info(f"Before {func.__name__}, {df_name}.shape={df.shape}")
                df = func(*args, **kwargs)

                if df is not None and isinstance(df, pd.DataFrame):
                    _logger.info(f"After {func.__name__}, {df_name}.shape={df.shape}")
                    return df
                else:
                    _logger.error(f"{func.__name__} did not return any DataFrame")
            else:
                # fall back if df is NOT a pd.DataFrame
                return func(*args, **kwargs)

        return wrapper

    return decorator_log_shape



# run a test:
df = pd.DataFrame(np.array([[123456, 10], 
                            [234567, 20], 
                            [345678, 30]]), 
                    columns=['zpid', 'dom'])

@log_shape_change(df_name='df')
def remove_low_dom_homes(df):
    return df[df.dom > 15]

print(remove_low_dom_homes(df).shape[0] == 2)
