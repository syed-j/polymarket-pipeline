from fastapi import FastAPI
from pydantic import BaseModel
try:
    from rag import ask          # works when running from inside src/
except ModuleNotFoundError:
    from src.rag import ask       # works inside Docker (running from /app)
app = FastAPI(title="Polymarket RAG Chatbot")

class Query(BaseModel):
    question: str

@app.get("/")
def home():
    return {"status": "Polymarket RAG chatbot is running"}

@app.post("/ask")
def ask_endpoint(query: Query):
    answer = ask(query.question)
    return {"question": query.question, "answer": answer}