import os
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel
from sqlalchemy import select
from libs.shared.db import engine, get_db
from libs.shared.models import metadata as shared_metadata
from libs.shared.models import users_table
from libs.shared.models import notes_table

app = FastAPI(title="MEMORIA Documents Service")

# Simple storage dir
STORAGE_DIR = os.getenv("DOCUMENTS_STORAGE_DIR", "./data/documents")
os.makedirs(STORAGE_DIR, exist_ok=True)

if "sqlite" in os.getenv("DATABASE_URL", ""):
    shared_metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok"}


class UploadResponse(BaseModel):
    document_id: str
    filename: str


def _ingest_document(document_id: str, path: str):
    # ingestion placeholder: pretend to run OCR and store text into document_texts table
    from libs.shared.db import SessionLocal
    from sqlalchemy import insert
    db = SessionLocal()
    try:
        sample_text = "Extracted text placeholder for document: %s" % os.path.basename(path)
        ins = insert(shared_metadata.tables["document_texts"]).values(document_id=document_id, page_number=1, text=sample_text)
        db.execute(ins)
        db.commit()
    finally:
        db.close()


@app.post("/api/v1/documents", response_model=UploadResponse)
def upload_document(background_tasks: BackgroundTasks, file: UploadFile = File(...), db=Depends(get_db)):
    # create document id and save file
    did = file.filename + ":" + os.urandom(6).hex()
    filepath = os.path.join(STORAGE_DIR, did)
    with open(filepath, "wb") as f:
        f.write(file.file.read())

    # record document metadata (lightweight)
    doc_ins = shared_metadata.tables.get("documents")
    if doc_ins is not None:
        db.execute(doc_ins.insert().values(id=did, user_id=None, filename=file.filename, mime=file.content_type, size=os.path.getsize(filepath), object_key=filepath, ingestion_status="pending"))
        db.commit()

    # enqueue ingestion (background)
    background_tasks.add_task(_ingest_document, did, filepath)
    return {"document_id": did, "filename": file.filename}
