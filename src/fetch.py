import requests
import pandas as pd
import json
from datetime import datetime, timezone

pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

# --- Job 1: FETCH ---
url = "https://gamma-api.polymarket.com/markets"
params = {"active": "true", "closed": "false", "limit": 50}
response = requests.get(url, params=params)
markets = response.json()          # a list of market dictionaries

# --- Job 2: CLEAN ---
df = pd.DataFrame(markets)          # blob -> table

# keep only the columns you care about
keep = ["id", "question", "outcomePrices", "volume", "category"]
df = df[[c for c in keep if c in df.columns]]

# pull the "Yes" price out of the ugly string -> a real number
df["yes_price"] = df["outcomePrices"].apply(lambda x: float(json.loads(x)[0]))

# volume is also text -> make it a number
df["volume"] = df["volume"].astype(float)

# stamp when you grabbed it (this makes it a time-series later)
df["captured_at"] = datetime.now(timezone.utc)

# --- Show it ---
print(f"Got {len(df)} markets\n")
print(df.sort_values("yes_price", ascending=False).head())