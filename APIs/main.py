from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel

app = FastAPI()

@app.get("/hello")
def say_hello():
    return {"message": "Hello from my own API!"}    

@app.get("/greet/{name}")
def greet(name: str):
    return {"message": f"Hello, {name}!"}

@app.get("/square/{number}")
def square(number: int):
    return {"number": number, "square": number * number}

@app.get("/add")
def add(a: int, b: int):
    return {"result": a + b}



books = [
    {"id": 1, "title": "Python Basics", "author": "Asha"},
    {"id": 2, "title": "Learning APIs", "author": "Ravi"},
    {"id": 3, "title": "Git for Beginners", "author": "Meera"},
]

@app.get("/books")
def list_books():
    return books

@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.get("/books/author/{author}")
def get_book_author(author : str):
    for i in books:
        if i["author"] == author:
            return i
    raise HTTPException(status_code=404,detail="Book by this author not found")

class BookIn(BaseModel):
    title: str
    author: str

@app.post("/books", status_code=201)
def create_book(book: BookIn):
    new_id = max(b["id"] for b in books) + 1 if books else 1
    new_book = {"id": new_id, **book.model_dump()}
    books.append(new_book)
    return new_book

@app.put("/books/{book_id}")
def replace_book(book_id: int, book: BookIn):
    for index, existing in enumerate(books):
        if existing["id"] == book_id:
            books[index] = {"id": book_id, **book.model_dump()}
            return books[index]
    raise HTTPException(status_code=404, detail="Book not found")

class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None

@app.patch("/books/{book_id}")
def update_book(book_id: int, changes: BookUpdate):
    for book in books:
        if book["id"] == book_id:
            book.update(changes.model_dump(exclude_unset=True))
            return book
    raise HTTPException(status_code=404, detail="Book not found")



@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int):
    for index, book in enumerate(books):
        if book["id"] == book_id:
            books.pop(index)
            return
    raise HTTPException(status_code=404, detail="Book not found")
