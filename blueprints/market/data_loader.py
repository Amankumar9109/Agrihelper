import os
import json
import pandas as pd
from flask import current_app

_cached_df = None

def get_market_dataframe():
    """
    Lazy load and cache the market data pandas DataFrame.
    """
    global _cached_df
    if _cached_df is not None:
        return _cached_df

    data_path = os.path.join(current_app.root_path, 'static', 'data', 'market_data.json')
    if not os.path.exists(data_path):
        # Fallback to empty DataFrame with expected columns
        _cached_df = pd.DataFrame(columns=['State', 'District', 'Market', 'Commodity', 'Min Price', 'Max Price', 'Modal Price'])
        return _cached_df

    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            market_data = json.load(f)
        _cached_df = pd.DataFrame(market_data)
        # Ensure price columns are numeric
        for col in ['Min Price', 'Max Price', 'Modal Price']:
            if col in _cached_df.columns:
                _cached_df[col] = pd.to_numeric(_cached_df[col], errors='coerce')
    except Exception as e:
        print(f"Error loading market data: {e}")
        _cached_df = pd.DataFrame(columns=['State', 'District', 'Market', 'Commodity', 'Min Price', 'Max Price', 'Modal Price'])

    return _cached_df
