import os
from datetime import datetime, timedelta
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from passlib.context import CryptContext
from jose import jwt

from libs.shared.db import engine, get_db
from libs.shared.models import users_table, metadata as shared_metadata

# Config
SECRET_KEY = os.getenv("AUTH_SECRET_KEY", "dev-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI(title="MEMORIA Auth Service")


# Ensure tables exist when running in SQLite/testing
if "sqlite" in os.getenv("DATABASE_URL", ""):
    shared_metadata.create_all(bind=engine)


class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/v1/auth/signup", response_model=TokenResponse)
def signup(req: SignupRequest, db=Depends(get_db)):
    # check existing
    q = select(users_table).where(users_table.c.email == req.email)
    existing = db.execute(q).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = get_password_hash(req.password)
    ins = users_table.insert().values(email=req.email, name=req.name, hashed_password=hashed)
    res = db.execute(ins)
    db.commit()

    user_row = db.execute(select(users_table).where(users_table.c.email == req.email)).first()
    user = dict(user_row._mapping)

    access_token = create_access_token({"sub": user["id"], "email": user["email"]})
    return {"access_token": access_token}


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@app.post("/api/v1/auth/login", response_model=TokenResponse)
def login(req: LoginRequest, db=Depends(get_db)):
    q = select(users_table).where(users_table.c.email == req.email)
    row = db.execute(q).first()
    if not row:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    user = dict(row._mapping)
    if not user.get("hashed_password"):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not verify_password(req.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": user["id"], "email": user["email"]})
    return {"access_token": access_token}
