import duckdb
import matplotlib.pyplot as plt

# Connect to your database
con = duckdb.connect("polymarket.duckdb")

# Pick the markets with the most snapshots (the ones we have the most history for)
top_markets = con.sql("""
    SELECT question
    FROM market_snapshots
    GROUP BY question
    ORDER BY COUNT(*) DESC
    LIMIT 5
""").fetchall()

plt.figure(figsize=(12, 6))

# Draw one line per market
for (question,) in top_markets:
    rows = con.sql(f"""
        SELECT captured_at, yes_price
        FROM market_snapshots
        WHERE question = '{question.replace("'", "''")}'
        ORDER BY captured_at
    """).fetchall()

    times = [r[0] for r in rows]
    prices = [r[1] for r in rows]

    # shorten long questions for the legend
    label = question[:40] + "..." if len(question) > 40 else question
    plt.plot(times, prices, marker="o", label=label)

con.close()

# Make it readable
plt.title("Polymarket: 'Yes' price over time")
plt.xlabel("Time captured")
plt.ylabel("Yes price (implied probability)")
plt.legend(loc="best", fontsize=8)
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Save it as an image AND show it
plt.savefig("analysis/price_chart.png", dpi=150)
plt.show()