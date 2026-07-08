import duckdb

# connect to your existing warehouse and pull the clean, deduped markets
con = duckdb.connect("polymarket.duckdb")
markets = con.sql("""
    SELECT question, yes_price, volume
    FROM latest_prices
""").fetchall()
con.close()

print(f"Pulled {len(markets)} markets from DuckDB")

# turn each market's data into one rich sentence (the "chunk")
documents = []
ids = []

for i, (question, yes_price, volume) in enumerate(markets):
    # combine question + price + volume into one meaningful piece of text
    chunk = (
        f"{question} "
        f"Current probability: {round(yes_price * 100)}%. "
        f"Trading volume: ${round(volume):,}."
    )
    documents.append(chunk)
    ids.append(f"market_{i}")

print(f"Built {len(documents)} chunks. Example:")
print(documents[0])

import chromadb

# create a Chroma database that saves to a folder on disk
client = chromadb.PersistentClient(path="chroma_db")

# a "collection" is like a table in the vector database
collection = client.get_or_create_collection(name="markets")

# add your chunks — Chroma embeds them automatically and stores them
collection.add(
    documents=documents,
    ids=ids
)

print(f"Stored {collection.count()} markets in Chroma")