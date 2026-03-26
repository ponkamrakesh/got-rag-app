from fastapi import FastAPI
from pydantic import BaseModel
from rag import generate_answer
from ingest import ingest_pdf

app = FastAPI()

class Query(BaseModel):
    question: str

@app.on_event("startup")
def startup_event():
    print("App Started...!")
    ingest_pdf()

@app.post("/chat")
def chat(query: Query):
    answer = generate_answer(query.question)
    return {"response": answer}
