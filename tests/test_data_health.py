import pandas as pd
import pytest

def test_csv_file_exists():
    """Check that the main dataset CSV exists."""
    import os
    assert os.path.exists("data/raw/synth_prices.csv"), "synth_prices.csv is missing!"

def test_csv_not_empty():
    """Check that the dataset CSV is not empty."""
    df = pd.read_csv("data/raw/synth_prices.csv")
    assert not df.empty, "Dataset is empty!"

def test_columns_exist():
    """Check that required columns are present."""
    df = pd.read_csv("data/raw/synth_prices.csv")
    required_columns = ["date", "price", "volume"]
    for col in required_columns:
        assert col in df.columns, f"Column {col} is missing!"