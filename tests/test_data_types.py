import pandas as pd
import pytest

def test_column_types():
    """Ensure columns have the expected types."""
    df = pd.read_csv("data/raw/synth_prices.csv", parse_dates=["date"])
    assert pd.api.types.is_datetime64_any_dtype(df["date"]), "date column should be datetime"
    assert pd.api.types.is_float_dtype(df["price"]), "price should be float"
    assert pd.api.types.is_integer_dtype(df["volume"]), "volume should be int"