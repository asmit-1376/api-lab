import os
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

import jwt
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pwdlib import PasswordHash
from pydantic import BaseModel, Field

load_dotenv()
SECRET = os.environ["JWT_SECRET"]       # crashes clearly if missing
ALGORITHM = "HS256"
TOKEN_MINUTES = 30

app = FastAPI(title="Auth Demo")
password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

DB_PATH = Path(__file__).parent / "auth.db"


# ---------- database ----------

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


init_db()


# ---------- data shapes ----------

class UserIn(BaseModel):
    username: str = Field(min_length=3)
    password: str = Field(min_length=8)


# ---------- helpers ----------

def create_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=TOKEN_MINUTES),
    }
    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        user_id = int(payload["sub"])
    except (jwt.PyJWTError, KeyError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    conn = get_connection()
    user = conn.execute(
        "SELECT id, username FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    conn.close()
    if user is None:
        raise HTTPException(status_code=401, detail="User no longer exists")
    return dict(user)


# ---------- endpoints ----------

@app.post("/register", status_code=201)
def register(user: UserIn):
    conn = get_connection()
    try:
        cur = conn.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (user.username, password_hash.hash(user.password)),
        )
        conn.commit()
        return {"id": cur.lastrowid, "username": user.username}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="Username already taken")
    finally:
        conn.close()


@app.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM users WHERE username = ?", (form.username,)
    ).fetchone()
    conn.close()

    if row is None or not password_hash.verify(form.password, row["password_hash"]):
        raise HTTPException(status_code=401, detail="Wrong username or password")

    return {"access_token": create_token(row["id"]), "token_type": "bearer"}


@app.get("/me")
def me(current_user: dict = Depends(get_current_user)):
    return current_user