import chromadb

# connect to the Chroma database you just built
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_collection(name="markets")

# ask it a question
results = collection.query(
    query_texts=["what markets are about crypto?"],
    n_results=3
)

# show what it retrieved
print("Top 3 markets for 'crypto':\n")
for doc in results["documents"][0]:
    print("-", doc)