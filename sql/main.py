import sqlite3
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Books API with SQLite")

# The database file will sit next to this script
DB_PATH = Path(__file__).parent / "books.db"


# ---------- Database helpers ----------

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row          # lets us read rows like dictionaries
    return conn


def fetch_all(sql, params=()):
    conn = get_connection()
    try:
        rows = conn.execute(sql, params).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def execute(sql, params=()):
    conn = get_connection()
    try:
        cur = conn.execute(sql, params)
        conn.commit()
        return cur.lastrowid, cur.rowcount
    finally:
        conn.close()


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL
        )
    """)
    count = conn.execute("SELECT COUNT(*) FROM books").fetchone()[0]
    if count == 0:                           # add starter data only once
        conn.executemany(
            "INSERT INTO books (title, author) VALUES (?, ?)",
            [
                ("Python Basics", "Asha"),
                ("Learning APIs", "Ravi"),
                ("Git for Beginners", "Meera"),
            ],
        )
    conn.commit()
    conn.close()


init_db()


# ---------- Data shapes ----------

class BookIn(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)


class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None


# ---------- Endpoints ----------

@app.get("/books")
def list_books():
    return fetch_all("SELECT * FROM books")


@app.get("/books/author/{author_name}")
def books_by_author(author_name: str):
    results = fetch_all(
        "SELECT * FROM books WHERE LOWER(author) = LOWER(?)", (author_name,)
    )
    if not results:
        raise HTTPException(status_code=404, detail="No books found for this author")
    return results


@app.get("/books/{book_id}")
def get_book(book_id: int):
    results = fetch_all("SELECT * FROM books WHERE id = ?", (book_id,))
    if not results:
        raise HTTPException(status_code=404, detail="Book not found")
    return results[0]


@app.post("/books", status_code=201)
def create_book(book: BookIn):
    new_id, _ = execute(
        "INSERT INTO books (title, author) VALUES (?, ?)",
        (book.title, book.author),
    )
    return {"id": new_id, **book.model_dump()}


@app.put("/books/{book_id}")
def replace_book(book_id: int, book: BookIn):
    _, changed = execute(
        "UPDATE books SET title = ?, author = ? WHERE id = ?",
        (book.title, book.author, book_id),
    )
    if changed == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"id": book_id, **book.model_dump()}


@app.patch("/books/{book_id}")
def update_book(book_id: int, changes: BookUpdate):
    results = fetch_all("SELECT * FROM books WHERE id = ?", (book_id,))
    if not results:
        raise HTTPException(status_code=404, detail="Book not found")

    updated = {**results[0], **changes.model_dump(exclude_unset=True)}
    execute(
        "UPDATE books SET title = ?, author = ? WHERE id = ?",
        (updated["title"], updated["author"], book_id),
    )
    return updated


@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int):
    _, deleted = execute("DELETE FROM books WHERE id = ?", (book_id,))
    if deleted == 0:
        raise HTTPException(status_code=404, detail="Book not found")