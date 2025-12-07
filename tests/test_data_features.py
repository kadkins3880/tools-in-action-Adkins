import pandas as pd
import pytest

def test_columns_exist():
    """Check that required columns are present."""
    df = pd.read_csv("data/processed/synth_features.csv")
    required_columns = ["log_return", "sma_5"]
    for col in required_columns:
        assert col in df.columns, f"Column {col} is missing!"

def test_column_types():
    """Ensure columns have the expected types."""
    df = pd.read_csv("data/processed/synth_features.csv")
    assert pd.api.types.is_float_dtype(df["log_return"]), "log_return should be float"
    assert pd.api.types.is_float_dtype(df["sma_5"]), "sma_5 should be float"