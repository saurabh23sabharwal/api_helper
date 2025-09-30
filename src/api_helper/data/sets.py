# src/api_helper/data/sets.py

import pandas as pd
import requests

# ---------- V0.0.0 ----------
__version__ = "0.0.0"

def fetch_api_v0(url: str, params: dict) -> pd.DataFrame:
    """
    V0.0.0: Fetch data from an API and return it as a single pandas DataFrame.

    Parameters
    ----------
    url : str
        API endpoint
    params : dict
        Query parameters

    Returns
    -------
    pd.DataFrame
        API response as a single DataFrame
    """
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    return pd.DataFrame(data)


# ---------- V0.1.0 ----------
__version__ = "0.1.0"

def fetch_api_v1(url: str, params: dict, with_headers: bool = True) -> dict:
    """
    V0.1.0: Fetch data from an API and return multiple DataFrames per key in JSON.

    Parameters
    ----------
    url : str
        API endpoint
    params : dict
        Query parameters
    with_headers : bool, default True
        - True  -> DataFrame keeps original headers
        - False -> DataFrame columns are replaced with integers

    Returns
    -------
    dict
        Dictionary of DataFrames (e.g., {'df1': df_daily, 'df2': df_hourly})
    """
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    result = {}
    for i, key in enumerate(data.keys(), start=1):
        df = pd.DataFrame(data[key])
        if 'time' in df.columns:
            df['time'] = pd.to_datetime(df['time'], unit='s')
        if not with_headers:
            df.columns = range(df.shape[1])
        result[f'df{i}'] = df

    return result
