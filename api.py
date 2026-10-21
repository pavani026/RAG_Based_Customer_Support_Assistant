"""FastAPI wrapper for the RAG Customer Support Assistant.

Run from the repo root:
    uvicorn api:app --reload
Then open http://127.0.0.1:8000/docs and try POST /ask
"""
from fastapi import FastAPI
from pydantic import BaseModel

from graph import build_graph
from retrieval import retrieve_docs
from generator import generate_answer

app = FastAPI(title="RAG Customer Support Assistant")
graph = build_graph()


class Query(BaseModel):
    question: str


def api_hitl(query):
    # An API has no terminal, so instead of input() we return a handoff message.
    return ("I couldn't find a reliable answer in the knowledge base. "
            "Your question has been escalated to a human support agent.")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask")
def ask(body: Query):
    state = {
        "query": body.question,
        "retriever": retrieve_docs,
        "generator": generate_answer,
        "hitl": api_hitl,
        "answer": "",
        "escalate": False,
    }
    result = graph.invoke(state)
    return {"answer": result["answer"], "escalated": result["escalate"]}
