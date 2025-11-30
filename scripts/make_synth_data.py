### `scripts/make_synth_data.py`

import pandas as pd
import numpy as np
import os

# Create directories if needed
os.makedirs("data/raw", exist_ok=True)

# Set random seed for reproducibility
np.random.seed(42)

# Generate synthetic stock data
n = 100
df = pd.DataFrame({
    "date": pd.date_range(start="2022-01-01", periods=n, freq="D"),
    "price": np.cumsum(np.random.randn(n)) + 100,
    "volume": np.random.randint(100, 1000, size=n)
})

# Save to CSV
df.to_csv("data/raw/synth_prices.csv", index=False)
print("Saved data/raw/synth_prices.csv")