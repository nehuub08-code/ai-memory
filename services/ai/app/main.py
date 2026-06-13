import os
import requests
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="MEMORIA AI Service")


class QARequest(BaseModel):
    question: str
    top_k: int = 5


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/v1/ai/qa")
def qa(req: QARequest):
    # RAG stub: call local Search service to get top passages and concatenate
    search_url = os.getenv("SEARCH_URL", "http://localhost:8005/api/v1/search/query")
    resp = requests.post(search_url, json={"q": req.question, "top_k": req.top_k}, timeout=10)
    hits = []
    if resp.status_code == 200:
        hits = resp.json().get("hits", [])
    # create a simple synthesized answer
    content = "\n\n".join([h.get("text", "") for h in hits[: req.top_k]])
    answer = f"Synthesis for: {req.question}\n\n{content}"
    return {"answer": answer, "sources": hits}
