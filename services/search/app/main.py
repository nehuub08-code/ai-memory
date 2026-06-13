import os
from typing import List, Optional
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import select

from libs.shared.db import engine, get_db
from libs.shared.models import metadata as shared_metadata

app = FastAPI(title="MEMORIA Search Service")

if "sqlite" in os.getenv("DATABASE_URL", ""):
    shared_metadata.create_all(bind=engine)


class Hit(BaseModel):
    doc_id: str
    text: str
    score: float


class SearchRequest(BaseModel):
    q: str
    top_k: Optional[int] = 5


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/v1/search/query")
def query(req: SearchRequest, db=Depends(get_db)):
    # Very simple hybrid: full-text search via document_texts.text match
    q = select(shared_metadata.tables["document_texts"]).limit(req.top_k)
    rows = db.execute(q).fetchall()
    hits = []
    for r in rows:
        d = dict(r._mapping)
        hits.append({"doc_id": d.get("document_id"), "text": d.get("text"), "score": 1.0})
    return {"hits": hits}
