from fastapi import FastAPI
from fastapi import HTTPException

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