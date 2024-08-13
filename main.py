from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

books = {
    1: {
        "title": "1984",
        "author": "George Orwell",
        "published_year": 1949,
        "genre": "Dystopian",
        "isbn": "978-0451524935",
    },
    2: {
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "published_year": 1960,
        "genre": "Fiction",
        "isbn": "978-0060935467",
    }
}

class Book(BaseModel):
    title: str
    author: str
    published_year: int
    genre: str
    isbn: str

class UpdateBook(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    published_year: Optional[int] = None
    genre: Optional[str] = None
    isbn: Optional[str] = None

@app.get('/')
def root():
    return {"message": "Welcome to the Library Management System"}

@app.get('/books/{book_id}')
def get_book(book_id: int):
    if book_id in books:
        return books[book_id]
    return {"Error": "Book not found"}

@app.post('/books/{book_id}')
def create_book(book_id: int, book: Book):
    if book_id in books:
        return {"Error": "Book already exists"}
    books[book_id] = book.dict()
    return books[book_id]

@app.put('/books/{book_id}')
def update_book(book_id: int, book: UpdateBook):
    if book_id not in books:
        return {"Error": "Book does not exist"}
    
    stored_book = books[book_id]
    if book.title is not None:
        stored_book['title'] = book.title
    if book.author is not None:
        stored_book['author'] = book.author
    if book.published_year is not None:
        stored_book['published_year'] = book.published_year
    if book.genre is not None:
        stored_book['genre'] = book.genre
    if book.isbn is not None:
        stored_book['isbn'] = book.isbn

    return stored_book

@app.delete('/books/{book_id}')
def delete_book(book_id: int):
    if book_id not in books:
        return {"Error": "Book not found"}
    del books[book_id]
    return {"Success": "Book successfully deleted"}
