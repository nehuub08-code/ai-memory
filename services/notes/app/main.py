import os
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select

from libs.shared.db import engine, get_db
from libs.shared.models import notes_table, metadata as shared_metadata

app = FastAPI(title="MEMORIA Notes Service")

# Ensure tables exist when running in SQLite/testing
if "sqlite" in os.getenv("DATABASE_URL", ""):
    shared_metadata.create_all(bind=engine)


class NoteCreate(BaseModel):
    user_id: str
    title: Optional[str] = None
    body_markdown: Optional[str] = None


class NoteOut(BaseModel):
    id: str
    user_id: str
    title: Optional[str]
    body_markdown: Optional[str]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/v1/notes", response_model=NoteOut)
def create_note(req: NoteCreate, db=Depends(get_db)):
    nid = req.user_id + ":" + str(os.urandom(6).hex())
    ins = notes_table.insert().values(id=nid, user_id=req.user_id, title=req.title, body_markdown=req.body_markdown)
    db.execute(ins)
    db.commit()
    row = db.execute(select(notes_table).where(notes_table.c.id == nid)).first()
    return dict(row._mapping)


@app.get("/api/v1/notes/{note_id}")
def get_note(note_id: str, db=Depends(get_db)):
    row = db.execute(select(notes_table).where(notes_table.c.id == note_id)).first()
    if not row:
        raise HTTPException(status_code=404, detail="Note not found")
    return dict(row._mapping)


@app.get("/api/v1/notes")
def list_notes(user_id: Optional[str] = None, limit: int = 20, db=Depends(get_db)):
    q = select(notes_table)
    if user_id:
        q = q.where(notes_table.c.user_id == user_id)
    q = q.limit(limit)
    rows = db.execute(q).fetchall()
    return [dict(r._mapping) for r in rows]
