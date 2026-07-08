import duckdb

con = duckdb.connect("polymarket.duckdb")

# what tables exist?
print("TABLES:")
print(con.sql("SHOW TABLES").fetchall())

# how many rows + snapshots?
print("\nROW COUNTS:")
con.sql("SELECT COUNT(*) AS total_rows, COUNT(DISTINCT captured_at) AS snapshots FROM market_snapshots").show()

# how many UNIQUE markets (this is what matters for RAG)?
print("UNIQUE MARKETS:")
con.sql("SELECT COUNT(DISTINCT question) AS unique_markets FROM market_snapshots").show()

# show a few actual questions
print("SAMPLE QUESTIONS:")
con.sql("SELECT DISTINCT question FROM market_snapshots LIMIT 15").show()

con.close()