from fastapi import FastAPI
from backend.rag import query_rag

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Westeros AI is alive ⚔️"}

@app.post("/chat")
def chat(q: str):
    return {"response": query_rag(q)}