import requests
import pandas as pd
import json
import duckdb
from datetime import datetime, timezone

pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

# --- Job 1: FETCH ---
url = "https://gamma-api.polymarket.com/markets"
params = {"active": "true", "closed": "false", "limit": 50}
response = requests.get(url, params=params)
markets = response.json()

# --- Job 2: CLEAN ---
df = pd.DataFrame(markets)

keep = ["id", "question", "outcomePrices", "volume", "category"]
df = df[[c for c in keep if c in df.columns]]

df["yes_price"] = df["outcomePrices"].apply(lambda x: float(json.loads(x)[0]))
df["volume"] = df["volume"].astype(float)
df["captured_at"] = datetime.now(timezone.utc)

# --- Job 3: SAVE into DuckDB ---
con = duckdb.connect("polymarket.duckdb")

con.execute("""
    CREATE TABLE IF NOT EXISTS market_snapshots (
        id VARCHAR,
        question VARCHAR,
        yes_price DOUBLE,
        volume DOUBLE,
        captured_at TIMESTAMP
    )
""")

con.execute("""
    INSERT INTO market_snapshots
    SELECT id, question, yes_price, volume, captured_at FROM df
""")

count = con.execute("SELECT COUNT(*) FROM market_snapshots").fetchone()[0]
print(f"Saved snapshot. Table now holds {count} rows total.")

con.close()