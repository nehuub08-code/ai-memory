import os
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select

from libs.shared.db import engine, get_db
from libs.shared.models import users_table, metadata as shared_metadata

app = FastAPI(title="MEMORIA User Service")

# Ensure tables exist when running in SQLite/testing
if "sqlite" in os.getenv("DATABASE_URL", ""):
    shared_metadata.create_all(bind=engine)


class UpdateUserRequest(BaseModel):
    name: Optional[str] = None
    settings: Optional[dict] = None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/v1/users/{user_id}")
def get_user(user_id: str, db=Depends(get_db)):
    q = select(users_table).where(users_table.c.id == user_id)
    row = db.execute(q).first()
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    return dict(row._mapping)


@app.patch("/api/v1/users/{user_id}")
def update_user(user_id: str, req: UpdateUserRequest, db=Depends(get_db)):
    q = select(users_table).where(users_table.c.id == user_id)
    row = db.execute(q).first()
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    update_values = {}
    if req.name is not None:
        update_values["name"] = req.name
    if req.settings is not None:
        update_values["settings"] = req.settings
    if update_values:
        db.execute(users_table.update().where(users_table.c.id == user_id).values(**update_values))
        db.commit()
    return {"status": "ok"}
