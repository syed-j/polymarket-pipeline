from fastapi import FastAPI
from pydantic import BaseModel
from rag import ask   # reuse your Day 12 RAG engine

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