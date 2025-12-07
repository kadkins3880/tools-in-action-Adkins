import pandas as pd
import numpy as np
import os

# Create directories if needed
os.makedirs("data/processed", exist_ok=True)

# Load the raw data
df = pd.read_csv("data/raw/synth_prices.csv", parse_dates=["date"])

# Compute log returns
df["log_return"] = np.log(df["price"] / df["price"].shift(1))

# Simple moving average
df["sma_5"] = df["price"].rolling(window=5).mean()

# Day of week (e.g., Monday = 0)
df["weekday"] = df["date"].dt.dayofweek

# Drop first few rows with NaNs from rolling
df = df.dropna().reset_index(drop=True)

# Save to processed
df.to_csv("data/processed/synth_features.csv", index=False)
print("Saved data/processed/synth_features.csv")