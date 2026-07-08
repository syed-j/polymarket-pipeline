import requests
import pandas as pd
import json
import duckdb
from datetime import datetime, timezone

pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

# --- Job 1: FETCH (paginated to get more than 100) ---
url = "https://gamma-api.polymarket.com/markets"

all_markets = []
for offset in range(0, 500, 100):        # 0, 100, 200, 300, 400 = 5 pages
    params = {
        "active": "true",
        "closed": "false",
        "limit": 100,
        "offset": offset
    }
    response = requests.get(url, params=params)
    page = response.json()
    if not page:                          # stop if a page comes back empty
        break
    all_markets.extend(page)

markets = all_markets
print(f"Fetched {len(markets)} markets from API")

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